// Model Selection Algorithm for OrchestrateX
// Implements intelligent model selection based on prompt analysis

interface ModelConfig {
  id: string;
  displayName: string;
  auth: string;
  keywords: string[];
  domains: string[];
  confidenceBase: number;
}

interface PromptFeatures {
  length: number;
  wordCount: number;
  hasQuestion: boolean;
  hasCodeRequest: boolean;
  complexityIndicators: number;
  creativeIndicators: number;
}

interface SelectionResult {
  selectedModel: string;
  confidence: number;
  reasoning: string;
  allScores: { [key: string]: number };
}

export class ModelSelector {
  private models: { [key: string]: ModelConfig } = {
    "GPT-OSS 120B": {
      id: "openai/gpt-oss-120b:free",
      displayName: "GPT-OSS 120B",
      auth: "Backend-Managed", // API key rotation handled by backend
      keywords: ["fact", "accurate", "correct", "verify", "truth", "research", "academic"],
      domains: ["academic", "research", "fact-checking", "knowledge"],
      confidenceBase: 0.85
    },
    "GLM-4.5 Air": {
      id: "z-ai/glm-4.5-air:free",
      displayName: "GLM-4.5 Air",
      auth: "Backend-Managed", // API key rotation handled by backend
      keywords: ["logic", "reason", "solve", "problem", "structure", "analyze", "think"],
      domains: ["logical-reasoning", "problem-solving", "analysis"],
      confidenceBase: 0.90
    },
    "Qwen3 Coder": {
      id: "qwen/qwen3-coder:free",
      displayName: "Qwen3 Coder",
      auth: "Backend-Managed", // API key rotation handled by backend
      keywords: ["code", "python", "javascript", "programming", "function", "debug", "software", "api"],
      domains: ["programming", "technical", "coding", "development"],
      confidenceBase: 0.95
    },
    "TNG DeepSeek": {
      id: "tngtech/deepseek-r1t2-chimera:free",
      displayName: "TNG DeepSeek",
      auth: "Backend-Managed", // API key rotation handled by backend
      keywords: ["deep", "detailed", "comprehensive", "thorough", "complex", "research"],
      domains: ["deep-analysis", "research", "comprehensive"],
      confidenceBase: 0.92
    },
    "MoonshotAI Kimi": {
      id: "moonshotai/kimi-k2:free",
      displayName: "MoonshotAI Kimi",
      auth: "Backend-Managed", // API key rotation handled by backend
      keywords: ["creative", "story", "idea", "innovative", "unique", "artistic", "imagine"],
      domains: ["creative", "storytelling", "innovation"],
      confidenceBase: 0.88
    },
    "Llama 4 Maverick": {
      id: "meta-llama/llama-4-maverick:free",
      displayName: "Llama 4 Maverick",
      auth: "Backend-Managed", // API key rotation handled by backend
      keywords: ["explain", "clear", "simple", "understand", "communicate", "teach"],
      domains: ["explanation", "communication", "teaching"],
      confidenceBase: 0.87
    }
  };

  analyzePrompt(prompt: string): PromptFeatures {
    const promptLower = prompt.toLowerCase();
    
    const complexityWords = ["complex", "detailed", "comprehensive", "deep", "thorough", "analyze"];
    const creativeWords = ["story", "creative", "imagine", "unique", "artistic", "innovative"];
    
    return {
      length: prompt.length,
      wordCount: prompt.split(' ').length,
      hasQuestion: prompt.includes('?'),
      hasCodeRequest: /\b(code|function|python|javascript|programming|debug|software|api)\b/i.test(prompt),
      complexityIndicators: complexityWords.filter(word => promptLower.includes(word)).length,
      creativeIndicators: creativeWords.filter(word => promptLower.includes(word)).length
    };
  }

  scoreModel(modelName: string, modelConfig: ModelConfig, prompt: string): number {
    const promptLower = prompt.toLowerCase();
    let score = modelConfig.confidenceBase;

    // Keyword matching (up to +0.15 bonus)
    const keywordMatches = modelConfig.keywords.filter(keyword => 
      promptLower.includes(keyword)
    ).length;
    score += keywordMatches * 0.05;

    // Special bonuses for specific models
    const features = this.analyzePrompt(prompt);
    
    if (modelName === "Qwen3 Coder" && features.hasCodeRequest) {
      score += 0.10; // Strong bonus for coding tasks
    } else if (modelName === "TNG DeepSeek" && features.wordCount > 20) {
      score += 0.05; // Bonus for longer, complex prompts
    } else if (modelName === "MoonshotAI Kimi" && features.creativeIndicators > 0) {
      score += 0.08; // Bonus for creative tasks
    } else if (modelName === "GLM-4.5 Air" && features.complexityIndicators > 0) {
      score += 0.06; // Bonus for analytical tasks
    } else if (modelName === "Llama 4 Maverick" && features.hasQuestion) {
      score += 0.05; // Bonus for explanatory questions
    }

    // Add small randomness to avoid always picking the same model
    score += Math.random() * 0.02 - 0.01;

    return Math.min(score, 1.0); // Cap at 1.0
  }

  selectBestModel(prompt: string): SelectionResult {
    const scores: { [key: string]: number } = {};
    let bestModel = "DeepSeek Chat v3.1"; // fallback
    let bestScore = 0;

    // Score all models
    for (const [modelName, modelConfig] of Object.entries(this.models)) {
      const score = this.scoreModel(modelName, modelConfig, prompt);
      scores[modelName] = score;
      
      if (score > bestScore) {
        bestScore = score;
        bestModel = modelName;
      }
    }

    const features = this.analyzePrompt(prompt);
    let reasoning = `Selected ${bestModel} with ${bestScore.toFixed(3)} confidence`;
    
    if (features.hasCodeRequest) {
      reasoning += " (coding task detected)";
    } else if (features.creativeIndicators > 0) {
      reasoning += " (creative task detected)";
    } else if (features.complexityIndicators > 0) {
      reasoning += " (analytical task detected)";
    }

    return {
      selectedModel: bestModel,
      confidence: bestScore,
      reasoning: reasoning,
      allScores: scores
    };
  }

  getModelConfig(modelName: string): ModelConfig | null {
    return this.models[modelName] || null;
  }
}

// Export singleton instance
export const modelSelector = new ModelSelector();