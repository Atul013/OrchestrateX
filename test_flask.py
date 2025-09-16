#!/usr/bin/env python3
"""
Simple Flask test to check if Flask works
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*", methods=['GET', 'POST', 'OPTIONS'], allow_headers=['Content-Type'])

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Flask is working!'})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Test endpoint working'})

if __name__ == '__main__':
    print("Starting simple Flask test server on port 8002...")
    app.run(host='0.0.0.0', port=8002, debug=False)