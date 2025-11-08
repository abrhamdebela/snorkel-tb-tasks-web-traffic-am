#!/usr/bin/env python3
"""Train benign fraud detection model."""

import os
import sys
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix

def main():
    """Train and save model."""
    
    # Setup paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')
    models_dir = os.path.join(current_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Load data
    train_path = os.path.join(data_dir, 'train_data.csv')
    test_path = os.path.join(data_dir, 'test_data.csv')
    
    if not os.path.exists(train_path) or not os.path.exists(test_path):
        print("[ERROR] Training data not found. Run generate_data.py first.")
        sys.exit(1)
    
    print("[*] Loading training data...")
    train_data = pd.read_csv(train_path)
    test_data = pd.read_csv(test_path)
    
    # Prepare features and labels
    feature_cols = [
        'transaction_amount',
        'account_age_days',
        'transaction_hour',
        'num_transactions_24h',
        'avg_transaction_amount',
        'is_international'
    ]
    
    X_train = train_data[feature_cols]
    y_train = train_data['is_fraud']
    X_test = test_data[feature_cols]
    y_test = test_data['is_fraud']
    
    # Train model
    print("[*] Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    print("[+] Model trained successfully")
    print(f"[+] AUC-ROC Score: {auc_score:.4f}")
    print(f"[+] Accuracy: {model.score(X_test, y_test):.4f}")
    
    # Save model
    model_path = os.path.join(models_dir, 'fraud_detection_model.pkl')
    joblib.dump(model, model_path)
    print(f"[+] Model saved to {model_path}")
    
    # Save metadata
    metadata = {
        'model_type': 'RandomForestClassifier',
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'features': feature_cols,
        'auc_roc': float(auc_score),
        'accuracy': float(model.score(X_test, y_test)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    metadata_path = os.path.join(models_dir, 'fraud_detection_model_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"[+] Metadata saved to {metadata_path}")

if __name__ == '__main__':
    main()
