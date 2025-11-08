#!/usr/bin/env python3
"""Generate synthetic fraud detection dataset."""

import os
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

def generate_fraud_detection_data(n_samples=10000, fraud_ratio=0.1):
    """Generate fraud detection dataset with realistic features."""
    
    # Create base features
    X, y = make_classification(
        n_samples=n_samples,
        n_features=6,
        n_informative=4,
        n_redundant=1,
        n_clusters_per_class=2,
        weights=[1-fraud_ratio, fraud_ratio],
        flip_y=0.01,
        random_state=42
    )
    
    # Create dataframe
    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(6)])
    
    # Map features to realistic transaction attributes
    df['transaction_amount'] = np.abs(X[:, 0] * 500 + 100)
    df['account_age_days'] = np.abs(X[:, 1] * 1000 + 100).astype(int)
    df['transaction_hour'] = (np.abs(X[:, 2]) * 24 % 24).astype(int)
    df['num_transactions_24h'] = np.abs(X[:, 3] * 10 + 1).astype(int)
    df['avg_transaction_amount'] = np.abs(X[:, 4] * 300 + 150)
    df['is_international'] = (X[:, 5] > 0).astype(int)
    df['is_fraud'] = y
    
    # Inject realistic fraud patterns
    fraud_mask = df['is_fraud'] == 1
    df.loc[fraud_mask, 'transaction_amount'] *= 1.5  # Frauds tend to be larger
    df.loc[fraud_mask, 'transaction_hour'] = (df.loc[fraud_mask, 'transaction_hour'] + 12) % 24  # Odd hours
    
    # Keep only the feature columns
    feature_cols = [
        'transaction_amount',
        'account_age_days',
        'transaction_hour',
        'num_transactions_24h',
        'avg_transaction_amount',
        'is_international',
        'is_fraud'
    ]
    
    return df[feature_cols]

def main():
    """Generate and save train/test datasets."""
    
    # Create output directory
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate full dataset
    print("[*] Generating fraud detection dataset...")
    full_data = generate_fraud_detection_data(n_samples=10000, fraud_ratio=0.1)
    
    # Split into train/test
    train_data = full_data[:8000]
    test_data = full_data[8000:]
    
    # Save datasets
    train_path = os.path.join(output_dir, 'train_data.csv')
    test_path = os.path.join(output_dir, 'test_data.csv')
    
    train_data.to_csv(train_path, index=False)
    test_data.to_csv(test_path, index=False)
    
    print(f"[+] Training data: {len(train_data)} samples -> {train_path}")
    print(f"[+] Test data: {len(test_data)} samples -> {test_path}")
    print(f"[+] Fraud ratio: {full_data['is_fraud'].sum() / len(full_data) * 100:.1f}%")

if __name__ == '__main__':
    main()
