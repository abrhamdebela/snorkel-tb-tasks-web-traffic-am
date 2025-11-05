import pandas as pd
import numpy as np
from xgboost import XGBRanker
import os

def test_model_file_exists(self):
    assert os.path.exists("drugs_diagnoses_ranker.json")

def test_scores_graph_exists(self):
    assert os.path.exists("drugs_diagnoses_scores.png")

def test_importance_graph_exists(self):
    assert os.path.exists("drugs_diagnoses_importance.png")

def test_all_files_exist(self):
    expected_files = [
        "drugs_diagnoses_ranker.json",
        "drugs_diagnoses_scores.png",
        "drugs_diagnoses_importance.png"
    ]
    missing_files = [f for f in expected_files if not os.path.exists(f)]
    assert len(missing_files) == 0, \
        f"Missing output files: {', '.join(missing_files)}"

def test_model_loads_successfully(self):
    assert os.path.exists("drugs_diagnoses_ranker.json")
    loaded_model = XGBRanker()
    loaded_model.load_model("drugs_diagnoses_ranker.json")
    assert loaded_model is not None
    assert isinstance(loaded_model, XGBRanker)

def test_loaded_model_can_predict():
    test_data = pd.read_csv('./drugs_diagnoses.csv')
    loaded_model = XGBRanker()
    loaded_model.load_model("drugs_diagnoses_ranker.json")
    feat_cols = ['age', 'drug_popularity', 'condition_concept_id',
                 'drug_concept_id', 'gender_concept_id']
    X_sample = test_data[feat_cols].fillna(0).astype(float).head(10).values
    predictions = loaded_model.predict(X_sample)
    assert predictions is not None
    assert len(predictions) == len(X_sample)
    assert predictions.dtype in [np.float32, np.float64]
