export interface ModelConfig {
  id: string;
  name: string;
  provider: string;
  description: string;
  specialties: string[];
  capabilities: {
    reasoning: number;
    coding: number;
    creativity: number;
    factuality: number;
    safety: number;
  };
  latency: {
    p50: number;
    p95: number;
  };
  cost: number; // per 1k tokens
  bestFor: string[];
  modelId: string;
  links: {
    huggingFace?: string;
    openRouter: string;
  };
  icon: string;
}

export const models: ModelConfig[] = [
  {
    id: 'glm4.5',
    name: 'GLM4.5',
    provider: 'Zhipu AI',
    description: 'State‑of‑the‑art mixture‑of‑experts model with strong reasoning, coding, and agentic capabilities.',
    specialties: ['reasoning', 'coding', 'agentic workflows'],
    capabilities: {
      reasoning: 95,
      coding: 92,
      creativity: 78,
      factuality: 88,
      safety: 85,
    },
    latency: { p50: 680, p95: 1200 },
    cost: 0.003,
    bestFor: ['Reasoning', 'coding', 'complex task solving'],
    modelId: 'zai-org/GLM-4.5',
    links: {
      huggingFace: 'https://huggingface.co/zai-org/GLM-4.5',
      openRouter: 'https://openrouter.ai/models/zai-org/GLM-4.5',
    },
    icon: 'Brain',
  },
  {
    id: 'gpt-oss',
    name: 'GPT‑OSS',
    provider: 'OpenAI Open Source',
    description: 'High‑capacity GPT‑based models under Apache 2.0 with flexible deployment.',
    specialties: ['general-purpose', 'language generation', 'flexible deployment'],
    capabilities: {
      reasoning: 82,
      coding: 85,
      creativity: 90,
      factuality: 84,
      safety: 88,
    },
    latency: { p50: 750, p95: 1400 },
    cost: 0.002,
    bestFor: ['General purpose language understanding and generation'],
    modelId: 'openai/gpt-oss-120b',
    links: {
      openRouter: 'https://openrouter.ai/models/openai/gpt-oss-120b',
    },
    icon: 'BookOpen',
  },
  {
    id: 'llama4-maverick',
    name: 'Llama 4 Maverick',
    provider: 'Meta',
    description: 'Advanced instruction‑tuned model with strong multilingual and reasoning capabilities.',
    specialties: ['instruction following', 'multilingual', 'reasoning'],
    capabilities: {
      reasoning: 88,
      coding: 80,
      creativity: 85,
      factuality: 90,
      safety: 92,
    },
    latency: { p50: 420, p95: 800 },
    cost: 0.001,
    bestFor: ['Instruction following', 'multilingual tasks', 'reasoning'],
    modelId: 'Llama 4 Maverick 17B Instruct (128E)',
    links: {
      openRouter: 'https://openrouter.ai/models/meta-llama/llama-4-maverick',
    },
    icon: 'Mountain',
  },
  {
    id: 'moonshot-kimi',
    name: 'MoonshotAI Kimi',
    provider: 'MoonshotAI',
    description: 'Advanced conversational AI with strong reasoning and coding.',
    specialties: ['conversational AI', 'reasoning', 'coding'],
    capabilities: {
      reasoning: 93,
      coding: 89,
      creativity: 82,
      factuality: 94,
      safety: 90,
    },
    latency: { p50: 580, p95: 1100 },
    cost: 0.0025,
    bestFor: ['Coding', 'reasoning', 'conversational tasks'],
    modelId: 'moonshotai/kimi-dev-72b:free',
    links: {
      openRouter: 'https://openrouter.ai/models/moonshotai/kimi-dev-72b',
    },
    icon: 'Rocket',
  },
  {
    id: 'qwen3-coder',
    name: 'Qwen3 Coder',
    provider: 'Alibaba',
    description: 'Specialized coding model with strong programming capabilities.',
    specialties: ['code generation', 'programming assistance', 'technical docs'],
    capabilities: {
      reasoning: 91,
      coding: 87,
      creativity: 95,
      factuality: 89,
      safety: 98,
    },
    latency: { p50: 720, p95: 1300 },
    cost: 0.004,
    bestFor: ['Code generation', 'programming assistance', 'technical docs'],
    modelId: 'qwen/qwen3-coder:free',
    links: {
      openRouter: 'https://openrouter.ai/models/qwen/qwen3-coder',
    },
    icon: 'Code',
  },
  {
    id: 'deepseek-chimera',
    name: 'TNG DeepSeek R1T2 Chimera',
    provider: 'TNG Tech',
    description: 'Advanced mixture‑of‑experts with strong reasoning and efficiency.',
    specialties: ['mixture-of-experts', 'reasoning', 'efficiency'],
    capabilities: {
      reasoning: 75,
      coding: 70,
      creativity: 72,
      factuality: 85,
      safety: 80,
    },
    latency: { p50: 520, p95: 950 },
    cost: 0.0008,
    bestFor: ['General NLP tasks', 'reasoning', 'complex analysis'],
    modelId: 'tngtech/deepseek-r1t2-chimera:free',
    links: {
      openRouter: 'https://openrouter.ai/models/tngtech/deepseek-r1t2-chimera',
    },
    icon: 'Layers3',
  },
];

export const mockMetrics = {
  requestsToday: 12947,
  avgLatency: 842,
  costSaved: 37,
  uptime: 99.97,
};

export const useCases = [
  {
    title: 'Code Generation & Review',
    description: 'Multi-model validation of generated code for accuracy and best practices',
    icon: 'Code',
  },
  {
    title: 'Factual Q&A with Citations',
    description: 'Cross-reference answers across models to ensure accuracy and provide sources',
    icon: 'BookOpen',
  },
  {
    title: 'Multilingual Support',
    description: 'Route to language-specialized models and validate translations',
    icon: 'Globe',
  },
  {
    title: 'Creative Writing & Ideation',
    description: 'Combine creative strengths while maintaining coherence and quality',
    icon: 'Sparkles',
  },
  {
    title: 'Mathematical Reasoning',
    description: 'Step-by-step validation and error-checking across multiple reasoning engines',
    icon: 'Calculator',
  },
];