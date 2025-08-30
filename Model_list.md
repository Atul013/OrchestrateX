# OrchestrateX Model List

This document lists the AI models integrated into the OrchestrateX collaborative multi-model system. These models are chosen based on their availability through OpenRouter and other free-tier API access to support development.

---

## 1. GLM4.5 (Zhipu AI)
- **Description:** State-of-the-art mixture-of-experts model with strong reasoning, coding, and agentic capabilities.
- **Access:** Available via OpenRouter API with free-tier options.
- **Model ID:** `zai-org/GLM-4.5`
- **Use Cases:** Reasoning, coding, complex task solving.
- **Links:**  
  - [Hugging Face GLM-4.5](https://huggingface.co/zai-org/GLM-4.5)  
  - [OpenRouter Platform](https://openrouter.ai)

---

## 2. GPT-OSS (OpenAI's Open Source GPT Variants)
- **Description:** High-capacity GPT-based models released under Apache 2.0 license, supporting flexible deployment.
- **Access:** Available via OpenRouter API.
- **Model ID:** `openai/gpt-oss-120b`
- **Use Cases:** General purpose language understanding and generation.
- **Links:**  
  - [GPT-OSS on Hugging Face](https://huggingface.co/openai/gpt-oss-120b)  
  - [OpenRouter Platform](https://openrouter.ai)

---

## 3. Llama 4 Maverick (Meta)
- **Description:** Advanced instruction-tuned model with strong multilingual and reasoning capabilities.
- **Access:** Available through OpenRouter API.
- **Model ID:** `Llama 4 Maverick 17B Instruct (128E)`
- **Use Cases:** Instruction following, multilingual tasks, reasoning.
- **Links:**  
  - [OpenRouter Platform](https://openrouter.ai)

---

## 4. MoonshotAI Kimi (Moonshot AI)
- **Description:** Advanced conversational AI model with strong reasoning and coding capabilities.
- **Access:** Free-tier API available through OpenRouter.
- **Model ID:** `moonshotai/kimi-dev-72b:free`
- **Use Cases:** Coding, reasoning, conversational tasks.
- **Links:**  
  - [OpenRouter Platform](https://openrouter.ai)

---

## 5. Qwen3 Coder (Alibaba)
- **Description:** Specialized coding model with strong programming and technical capabilities.
- **Access:** Free-tier API available through OpenRouter.
- **Model ID:** `qwen/qwen3-coder:free`
- **Use Cases:** Code generation, programming assistance, technical documentation.
- **Links:**  
  - [OpenRouter Platform](https://openrouter.ai)

---

## 6. TNG DeepSeek R1T2 Chimera (TNG Tech)
- **Description:** Advanced mixture-of-experts model with strong reasoning performance and efficiency.
- **Access:** Free-tier API available through OpenRouter.
- **Model ID:** `tngtech/deepseek-r1t2-chimera:free`
- **Use Cases:** General NLP tasks, reasoning, complex analysis.
- **Links:**  
  - [OpenRouter Platform](https://openrouter.ai)

---

## Integration Notes

All models are integrated via OpenRouter API for consistent access patterns and unified authentication. The system uses environment-based configuration for easy model switching and API key management.

---

This model selection balances cutting-edge AI capabilities with accessibility and cost constraints to power OrchestrateX's collaborative multi-agent platform.

For setup instructions and API usage details, refer to the project's integration guide.
