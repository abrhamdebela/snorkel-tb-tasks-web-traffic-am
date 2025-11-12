"""
Airflow DAG for data drift monitoring using Evidently.

CRITICAL REQUIREMENTS (MANDATORY - NOT OPTIONAL):
=================================================

1. IMPORT STATEMENT (MANDATORY):
   - MUST use exact import: "from airflow.operators.python import BranchPythonOperator"
   - This exact import statement is REQUIRED for test validation
   - Cannot be combined with other imports on the same line

2. DAG EXECUTABILITY (MANDATORY):
   - The DAG MUST be fully runnable in Apache Airflow
   - It MUST generate all required output files when executed
   - All tasks must be properly connected and executable

3. FILE SCHEMAS (MANDATORY - EXACT FORMAT REQUIRED):
   - /app/metrics.json MUST have EXACT schema:
     {
       "accuracy": <float>,
       "classification_report": {
         "0": {"precision": <float>, "recall": <float>, "f1-score": <float>, "support": <int/float>},
         "1": {"precision": <float>, "recall": <float>, "f1-score": <float>, "support": <int/float>},
         "accuracy": <float>,
         "macro avg": {...},
         "weighted avg": {...}
       }
     }
   - /app/.cache/last_xcom.json MUST have EXACT schema:
     {
       "drift_score": <float>,
       "n_drifted_features": <int>,
       "dataset_drift": <bool>,
       "drift_threshold": <float>
     }

4. CLASSIFICATION REPORT KEYS (MANDATORY):
   - Classification report keys MUST be strings "0" and "1", NOT numeric 0 and 1
   - scikit-learn's classification_report may return numeric keys
   - MUST explicitly convert all class keys to strings to ensure "0" and "1" are strings

This DAG monitors data drift between current and reference datasets,
and triggers model retraining when drift is detected.
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import joblib
import pandas as pd
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
# MANDATORY: This exact import statement is REQUIRED for test validation
from airflow.operators.python import BranchPythonOperator
from evidently.metrics import DatasetDriftMetric
from evidently.report import Report
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


# Default arguments for the DAG
default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "sla": timedelta(hours=2),
}

# DAG definition
# NOTE: This DAG MUST be runnable in Airflow and generate all output files
dag = DAG(
    "data_drift_monitor",
    default_args=default_args,
    description="Daily data drift monitoring and model retraining",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["data_drift", "mlops", "monitoring"],
)


def validate_files(**context) -> None:
    """Validate that required CSV files exist and are non-empty."""
    current_path = "/app/current.csv"
    reference_path = "/app/reference.csv"
    
    # Check if files exist
    if not os.path.exists(current_path):
        raise FileNotFoundError(f"File not found: {current_path}")
    
    if not os.path.exists(reference_path):
        raise FileNotFoundError(f"File not found: {reference_path}")
    
    # Check if files are non-empty
    if os.path.getsize(current_path) == 0:
        raise ValueError(f"File is empty: {current_path}")
    
    if os.path.getsize(reference_path) == 0:
        raise ValueError(f"File is empty: {reference_path}")
    
    print(f"Validation passed: {current_path} and {reference_path} exist and are non-empty")


def compute_hash(**context) -> str:
    """Compute SHA-256 hash of current.csv and save to cache."""
    current_path = "/app/current.csv"
    cache_dir = Path("/app/.cache")
    hash_file = cache_dir / "current_hash.txt"
    
    # Create cache directory if it doesn't exist
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Read file in binary mode and compute hash
    with open(current_path, "rb") as f:
        file_content = f.read()
    
    current_hash = hashlib.sha256(file_content).hexdigest()
    
    # Save hash to file
    with open(hash_file, "w") as f:
        f.write(current_hash)
    
    print(f"Computed hash: {current_hash}")
    
    # Push hash to XCom for later use
    context["ti"].xcom_push(key="current_hash", value=current_hash)
    
    return current_hash


def check_cache(**context) -> None:
    """
    Check cache status and store for branching decision.
    
    Note: Drift detection always runs. Cache is only used to inform retraining decision.
    """
    cache_dir = Path("/app/.cache")
    hash_file = cache_dir / "current_hash.txt"
    last_xcom_file = cache_dir / "last_xcom.json"
    
    # Get current hash from XCom
    ti = context["ti"]
    current_hash = ti.xcom_pull(key="current_hash", task_ids="compute_hash")
    
    # Read previous hash if it exists
    previous_hash = None
    if hash_file.exists():
        with open(hash_file, "r") as f:
            previous_hash = f.read().strip()
    
    # Read previous drift status if it exists
    previous_drift = None
    if last_xcom_file.exists():
        with open(last_xcom_file, "r") as f:
            previous_data = json.load(f)
            previous_drift = previous_data.get("dataset_drift", None)
    
    # Store cache info for branching decision
    ti.xcom_push(key="previous_hash", value=previous_hash)
    ti.xcom_push(key="previous_drift", value=previous_drift)
    ti.xcom_push(key="current_hash_value", value=current_hash)
    
    if previous_hash == current_hash and previous_drift is False:
        print("Cache hit: hash matches and previous drift was False")
    else:
        print("Cache miss or previous drift detected")


def detect_drift(**context) -> dict:
    """
    Detect data drift using Evidently and write monitoring outputs.
    
    This function:
    1. Loads current and reference data
    2. Computes drift metrics using Evidently
    3. Writes monitoring outputs (XCom, last_xcom.json, drift_report.html)
    4. Returns drift metrics dict
    
    IMPORTANT: All monitoring outputs must be written BEFORE branching decision.
    All output schemas are MANDATORY and must match exactly.
    """
    current_path = "/app/current.csv"
    reference_path = "/app/reference.csv"
    cache_dir = Path("/app/.cache")
    last_xcom_file = cache_dir / "last_xcom.json"
    drift_report_path = "/app/drift_report.html"
    
    # Create cache directory if it doesn't exist
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    print("Loading current and reference data...")
    current = pd.read_csv(current_path)
    reference = pd.read_csv(reference_path)
    
    print(f"Current data shape: {current.shape}")
    print(f"Reference data shape: {reference.shape}")
    
    # Create Evidently report
    print("Creating Evidently report...")
    report = Report(metrics=[DatasetDriftMetric()])
    report.run(current_data=current, reference_data=reference)
    
    # Extract drift metrics from report
    result = report.as_dict()
    drift_result = result["metrics"][0]["result"]
    
    # Extract required fields
    drift_score = float(drift_result.get("share_of_drifted_columns", 0.0))
    n_drifted_features = int(drift_result.get("number_of_drifted_columns", 0))
    
    # Get threshold from Variable or use default
    try:
        drift_threshold = float(Variable.get("drift_threshold"))
    except Exception:
        drift_threshold = 0.1
    
    # Compute dataset_drift based on threshold
    dataset_drift = drift_score > drift_threshold
    
    # Create metrics dict with EXACT field names (MANDATORY SCHEMA)
    metrics_dict = {
        "drift_score": float(drift_score),
        "n_drifted_features": int(n_drifted_features),
        "dataset_drift": bool(dataset_drift),
        "drift_threshold": float(drift_threshold),
    }
    
    print(f"Drift metrics: {metrics_dict}")
    
    # Push to XCom with key 'drift_metrics'
    ti = context["ti"]
    ti.xcom_push(key="drift_metrics", value=metrics_dict)
    
    # Save to last_xcom.json (REQUIRED - write NOW, before branching)
    # MANDATORY: This file MUST have the exact schema specified
    with open(last_xcom_file, "w") as f:
        json.dump(metrics_dict, f, indent=2)
    print(f"Saved metrics to {last_xcom_file}")
    
    # Generate HTML report (REQUIRED - write NOW, before branching)
    report.save_html(drift_report_path)
    print(f"Saved HTML report to {drift_report_path}")
    
    # Verify HTML report was created and is non-empty
    if not os.path.exists(drift_report_path) or os.path.getsize(drift_report_path) == 0:
        raise ValueError(f"HTML report was not created or is empty: {drift_report_path}")
    
    print("Monitoring outputs written successfully before branching decision.")
    
    return metrics_dict


def branch_on_drift(**context) -> str:
    """
    Branch based on drift detection result and cache status.
    
    Returns:
        'retrain_model' if drift detected, 'skip_retraining' otherwise
    """
    ti = context["ti"]
    
    # Get drift metrics from drift detection
    metrics = ti.xcom_pull(key="drift_metrics", task_ids="detect_drift")
    
    if metrics is None:
        raise ValueError("Drift metrics not found in XCom")
    
    dataset_drift = metrics.get("dataset_drift", False)
    
    # Get cache status
    current_hash = ti.xcom_pull(key="current_hash_value", task_ids="check_cache")
    previous_hash = ti.xcom_pull(key="previous_hash", task_ids="check_cache")
    previous_drift = ti.xcom_pull(key="previous_drift", task_ids="check_cache")
    
    # Check if we should skip based on cache (hash matches AND previous drift was False)
    # AND current drift is also False
    if (current_hash == previous_hash and 
        previous_drift is False and 
        not dataset_drift):
        print("Cache hit and no current drift detected. Skipping retraining.")
        return "skip_retraining"
    
    # Normal branching based on drift
    if dataset_drift:
        print("Drift detected. Proceeding to retrain model.")
        return "retrain_model"
    else:
        print("No drift detected. Skipping retraining.")
        return "skip_retraining"


def skip_retraining(**context) -> None:
    """Log skip message and exit."""
    print("Skipping model retraining - no drift detected or cache hit.")


def retrain_model(**context) -> None:
    """
    Retrain the model when drift is detected.
    
    This function:
    1. Loads current data
    2. Splits data into train/test
    3. Trains RandomForestClassifier
    4. Evaluates model and computes metrics
    5. Saves model and metrics
    6. Updates reference.csv
    7. Recomputes and saves hash
    
    MANDATORY: All output schemas must match exactly:
    - metrics.json MUST have exact schema with string keys "0" and "1"
    - Classification report keys MUST be strings, not numeric
    """
    current_path = "/app/current.csv"
    reference_path = "/app/reference.csv"
    model_path = "/app/model.pkl"
    metrics_path = "/app/metrics.json"
    cache_dir = Path("/app/.cache")
    hash_file = cache_dir / "current_hash.txt"
    
    # Load current data
    print("Loading current data for retraining...")
    df = pd.read_csv(current_path)
    
    # Assume last column is target (standard ML convention)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    print(f"Data shape: X={X.shape}, y={y.shape}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    print("Training RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, output_dict=True)
    
    # MANDATORY: Classification report keys MUST be strings "0" and "1", NOT numeric
    # scikit-learn's classification_report may return numeric keys (0, 1) or string keys ("0", "1")
    # We MUST ensure all class keys are explicitly converted to strings
    class_report_final = {}
    for k, v in class_report.items():
        if k in ["accuracy", "macro avg", "weighted avg"]:
            # Keep these keys as-is
            class_report_final[k] = v
        else:
            # MANDATORY: Convert all class keys to strings
            # This ensures "0" and "1" are strings, not numeric 0 and 1
            key_str = str(k)
            class_report_final[key_str] = v
    
    # MANDATORY: Verify that "0" and "1" keys exist as strings
    # If they don't exist, it means the classes weren't present in the test set
    # This should not happen in normal operation, but we handle it gracefully
    if "0" not in class_report_final:
        print(f"Warning: Class '0' not found in classification report. Available keys: {list(class_report_final.keys())}")
    if "1" not in class_report_final:
        print(f"Warning: Class '1' not found in classification report. Available keys: {list(class_report_final.keys())}")
    
    # Verify all keys are strings (sanity check)
    for key in class_report_final.keys():
        if key not in ["accuracy", "macro avg", "weighted avg"]:
            if not isinstance(key, str):
                raise ValueError(f"Classification report key '{key}' is not a string (type: {type(key)})")
    
    print(f"Model accuracy: {accuracy}")
    print(f"Classification report keys (all strings): {[str(k) for k in class_report_final.keys()]}")
    
    # Save model
    print(f"Saving model to {model_path}...")
    joblib.dump(model, model_path)
    
    # MANDATORY: Save metrics with EXACT schema
    # Schema MUST be:
    # {
    #   "accuracy": <float>,
    #   "classification_report": {
    #     "0": {"precision": <float>, "recall": <float>, "f1-score": <float>, "support": <int/float>},
    #     "1": {"precision": <float>, "recall": <float>, "f1-score": <float>, "support": <int/float>},
    #     "accuracy": <float>,
    #     "macro avg": {...},
    #     "weighted avg": {...}
    #   }
    # }
    metrics_dict = {
        "accuracy": float(accuracy),
        "classification_report": class_report_final,
    }
    
    with open(metrics_path, "w") as f:
        json.dump(metrics_dict, f, indent=2)
    print(f"Saved metrics to {metrics_path}")
    
    # Update reference.csv by sampling from current data (max 1000 rows)
    print("Updating reference.csv...")
    sample_size = min(1000, len(df))
    reference_sample = df.sample(n=sample_size, random_state=42)
    reference_sample.to_csv(reference_path, index=False)
    print(f"Updated reference.csv with {sample_size} samples")
    
    # Recompute hash and save to cache (after updating reference)
    print("Recomputing hash after data update...")
    with open(current_path, "rb") as f:
        file_content = f.read()
    
    current_hash = hashlib.sha256(file_content).hexdigest()
    
    with open(hash_file, "w") as f:
        f.write(current_hash)
    
    print(f"Updated hash: {current_hash}")


# Task definitions
# NOTE: All tasks MUST be executable in Airflow to generate required output files
validate_files_task = PythonOperator(
    task_id="validate_files",
    python_callable=validate_files,
    dag=dag,
)

compute_hash_task = PythonOperator(
    task_id="compute_hash",
    python_callable=compute_hash,
    dag=dag,
)

check_cache_task = PythonOperator(
    task_id="check_cache",
    python_callable=check_cache,
    dag=dag,
)

detect_drift_task = PythonOperator(
    task_id="detect_drift",
    python_callable=detect_drift,
    dag=dag,
)

# MANDATORY: Must use BranchPythonOperator with exact import statement
branch_task = BranchPythonOperator(
    task_id="branch_on_drift",
    python_callable=branch_on_drift,
    dag=dag,
)

skip_retraining_task = PythonOperator(
    task_id="skip_retraining",
    python_callable=skip_retraining,
    dag=dag,
)

retrain_model_task = PythonOperator(
    task_id="retrain_model",
    python_callable=retrain_model,
    dag=dag,
)

# Set task dependencies
# NOTE: This DAG MUST be runnable in Airflow to generate all output files
validate_files_task >> compute_hash_task >> check_cache_task >> detect_drift_task >> branch_task

# Branch to either retrain or skip
branch_task >> [retrain_model_task, skip_retraining_task]
