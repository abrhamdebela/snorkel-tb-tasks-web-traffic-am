#!/usr/bin/env python3
"""Vulnerable MLflow server (intentionally insecure)."""

import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Models directory
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

# Metadata storage
metadata_store = {}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'service': 'mlflow-vulnerable-server',
        'status': 'healthy'
    })

@app.route('/api/models', methods=['GET'])
def list_models():
    """List all models (NO AUTHENTICATION!)."""
    models = []
    for filename in os.listdir(MODELS_DIR):
        if filename.endswith('.pkl'):
            model_name = filename.replace('.pkl', '')
            models.append(model_name)
    
    return jsonify({'models': models})

@app.route('/api/models/<model_name>', methods=['GET'])
def get_model_metadata(model_name):
    """Get model metadata (NO AUTHENTICATION!)."""
    if model_name not in metadata_store:
        return jsonify({'error': 'Model not found'}), 404
    
    return jsonify(metadata_store[model_name])

@app.route('/api/models/<model_name>/download', methods=['GET'])
def download_model(model_name):
    """Download model file (NO AUTHENTICATION!)."""
    model_path = os.path.join(MODELS_DIR, f'{model_name}.pkl')
    
    if not os.path.exists(model_path):
        return jsonify({'error': 'Model not found'}), 404
    
    with open(model_path, 'rb') as f:
        model_data = f.read()
    
    return model_data, 200, {'Content-Type': 'application/octet-stream'}

@app.route('/api/models/<model_name>/upload', methods=['POST'])
def upload_model(model_name):
    """Upload model (NO AUTHENTICATION, NO VERIFICATION!)."""
    try:
        if 'model' not in request.files:
            return jsonify({'error': 'No model file provided'}), 400
        
        model_file = request.files['model']
        metadata = request.form.get('metadata', '{}')
        metadata = json.loads(metadata)
        
        # Save model without any verification
        model_path = os.path.join(MODELS_DIR, f'{model_name}.pkl')
        model_file.save(model_path)
        
        # Store metadata
        metadata_store[model_name] = {
            'model_name': model_name,
            'status': 'uploaded',
            'metadata': metadata
        }
        
        print(f"[!] Model uploaded: {model_name} (NO AUTHENTICATION CHECK!)")
        return jsonify({'message': 'Model uploaded successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/<model_name>/deploy', methods=['POST'])
def deploy_model(model_name):
    """Deploy model (NO VERIFICATION!)."""
    if model_name not in metadata_store:
        return jsonify({'error': 'Model not found'}), 404
    
    # Deploy without any verification
    metadata_store[model_name]['status'] = 'production'
    
    print(f"[!] Model deployed to production: {model_name} (NO VERIFICATION!)")
    return jsonify({
        'message': 'Model deployed to production',
        'status': 'production'
    })

@app.route('/api/models/<model_name>', methods=['DELETE'])
def delete_model(model_name):
    """Delete model (NO AUTHENTICATION!)."""
    model_path = os.path.join(MODELS_DIR, f'{model_name}.pkl')
    
    if os.path.exists(model_path):
        os.remove(model_path)
        if model_name in metadata_store:
            del metadata_store[model_name]
        print(f"[!] Model deleted: {model_name} (NO AUTHENTICATION CHECK!)")
        return jsonify({'message': 'Model deleted successfully'})
    
    return jsonify({'error': 'Model not found'}), 404

if __name__ == '__main__':
    print("[!] Starting vulnerable MLflow server on http://0.0.0.0:5000")
    print("[!] WARNING: This server has NO security controls!")
    app.run(host='0.0.0.0', port=5000, debug=False)
