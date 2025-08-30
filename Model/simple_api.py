from flask import Flask, request, jsonify
from model_selector import ModelSelector

app = Flask(__name__)
selector = ModelSelector()
selector.load_model('model_selector.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Missing prompt parameter'}), 400
    result = selector.select_best_model(prompt)
    return jsonify({
        'best_model': result['predicted_model'],
        'prediction_confidence': result['prediction_confidence'],
        'confidence_scores': result['confidence_scores']
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
