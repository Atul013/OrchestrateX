#!/usr/bin/env python3
"""
Ultra-Simple Test Server 
Just to verify frontend connectivity
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'test': 'working'})

@app.route('/api/orchestration/process', methods=['POST'])  
def test_endpoint():
    return jsonify({
        'success': True,
        'result': {
            'primary_response': {
                'model_name': 'Test Model',
                'content': 'This is a real backend response! The connection is working.',
                'success': True
            },
            'critiques': [
                {
                    'model_name': 'Critique Model 1',
                    'critique': 'This looks good from Model 1 perspective.'
                },
                {
                    'model_name': 'Critique Model 2', 
                    'critique': 'Model 2 also approves this response.'
                }
            ],
            'summary': {
                'primary_model': 'Test Model',
                'critiques_count': 2,
                'total_models': 3
            }
        },
        'timestamp': '2025-09-13T16:52:00.000Z',
        'models_used': 3
    })

if __name__ == '__main__':
    print("Starting ultra-simple test server on http://localhost:8002")
    app.run(host='localhost', port=8002, debug=False)
