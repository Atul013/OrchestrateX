# OrchestrateX Client Usage Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r client_requirements.txt
```

### 2. Start Model Selector API
```bash
cd Model
python simple_api.py
```

### 3. Run the Client

#### Single Prompt
```bash
python orchestratex_client.py --prompt "Write a Python function for sorting"
```

#### Batch Processing
```bash
python orchestratex_client.py --batch sample_prompts.txt
```

#### Interactive Mode
```bash
python orchestratex_client.py --interactive
```

## 🔧 Configuration

### Environment Variables
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

### Command Line Options
- `--prompt, -p`: Single prompt to process
- `--batch, -b`: File with prompts (one per line)
- `--interactive, -i`: Interactive mode
- `--model-selector-url`: Model selector API URL (default: http://localhost:5000)
- `--openrouter-key`: OpenRouter API key
- `--max-concurrent`: Max concurrent requests for batch (default: 3)
- `--output, -o`: Output file for results
- `--verbose, -v`: Verbose logging

## 📊 Features

✅ **Model Selection**: Uses ML-trained model selector
✅ **AI Provider Routing**: Connects to OpenRouter for real AI models  
✅ **Fallback System**: Tries alternative models on failure
✅ **Batch Processing**: Handles multiple prompts efficiently
✅ **Error Handling**: Comprehensive error recovery
✅ **Logging**: Detailed logs and statistics
✅ **Cost Tracking**: Monitors usage and costs
✅ **Response Caching**: Saves results to JSON

## 🎯 Example Workflow

1. **Client sends prompt** → Model Selector API
2. **Gets prediction** → "TNG DeepSeek" with 0.85 confidence
3. **Routes to OpenRouter** → Calls DeepSeek model
4. **Receives response** → Logs metrics and costs
5. **Fallback if needed** → Tries GPT-OSS, Llama, etc.
6. **Returns result** → Complete orchestration data

## 📈 Output Format

```json
{
  "prompt": "Write a Python function...",
  "selected_model": "TNG DeepSeek",
  "confidence_scores": {
    "TNG DeepSeek": 0.85,
    "GPT-OSS": 0.12,
    "GLM4.5": 0.03
  },
  "response": "def binary_search(arr, target)...",
  "success": true,
  "tokens_used": 150,
  "response_time_ms": 1200,
  "cost_usd": 0.003,
  "fallback_attempts": []
}
```

## 🛠 Troubleshooting

**API Connection Issues:**
- Check if model selector API is running on port 5000
- Verify network connectivity

**OpenRouter Errors:**
- Ensure API key is set correctly
- Check model availability and quotas

**Fallback Behavior:**
- Client automatically tries alternative models
- Logs all attempts for debugging

## 🔄 Integration Examples

### Python Integration
```python
async with OrchestrateXClient() as client:
    result = await client.orchestrate_prompt("Your question")
    print(result.final_response.response_text)
```

### Batch Processing
```python
prompts = ["Question 1", "Question 2", "Question 3"]
results = await client.process_batch(prompts)
for result in results:
    print(f"{result.selected_model}: {result.success}")
```
