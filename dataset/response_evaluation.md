# Response Collection & Evaluation Methodology

## Step 1: Collect Responses
- Send identical prompts to all chatbots (GLM4.5, GPT-OSS, LLaMa 3, Gemini2.5, Claude .5, Falcon)
- Store responses in a unified format:
  ```json
  {
    "prompt": "...",
    "domain": "coding",
    "chatbot_responses": {
      "GLM4.5": "...",
      "GPT-OSS": "...",
      "LLaMa 3": "...",
      "Gemini2.5": "...",
      "Claude .5": "...",
      "Falcon": "..."
    }
  }
  ```

## Step 2: Human Evaluation
- Human evaluators rate each response on:
  - Accuracy
  - Relevance
  - Clarity
  - Creativity
- Use a Likert scale (1-5) for each criterion
- Multiple annotators per response for reliability

## Step 3: Inter-Annotator Agreement
- Calculate agreement metrics (e.g., Cohen's kappa)
- Flag responses with low agreement for review

## Step 4: Dataset Structuring
- Final format:
  ```json
  {
    "prompt": "...",
    "domain": "coding",
    "chatbot_responses": {...},
    "ratings": {
      "GLM4.5": {"accuracy": 4, "relevance": 5, "clarity": 4, "creativity": 3},
      "GPT-OSS": {"accuracy": 5, "relevance": 4, "clarity": 5, "creativity": 3},
      "LLaMa 3": {"accuracy": 4, "relevance": 4, "clarity": 4, "creativity": 4},
      "Gemini2.5": {"accuracy": 5, "relevance": 5, "clarity": 4, "creativity": 4},
      "Claude .5": {"accuracy": 4, "relevance": 5, "clarity": 5, "creativity": 5},
      "Falcon": {"accuracy": 3, "relevance": 4, "clarity": 4, "creativity": 3}
    }
  }
  ```
- Create train/validation/test splits (70/15/15)

## Step 5: Documentation
- Document evaluation criteria and rating methodology
- Maintain transparency and reproducibility

---
This file will be updated with sample data and evaluation results as the project progresses.
