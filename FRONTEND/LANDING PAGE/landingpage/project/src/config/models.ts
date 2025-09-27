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
  logo: string; // Path to provider logo
}

export const models: ModelConfig[] = [
  {
    id: 'glm4.5',
    name: 'GLM4.5',
    provider: 'Zhipu AI',
    description: 'State‑of‑the‑art mixture‑of‑experts model with strong reasoning, coding, and agentic capabilities.',
    specialties: ['reasoning', 'coding', 'agentic workflows'],
    capabilities: {
      reasoning: 89,
      coding: 85,
      creativity: 82,
      factuality: 91,
      safety: 88,
    },
    latency: { p50: 680, p95: 1250 },
    cost: 2.50, // $2.50 per 1M tokens (updated Dec 2024)
    bestFor: ['Reasoning', 'coding', 'complex task solving'],
    modelId: 'zhipuai/glm-4.5-turbo',
    links: {
      huggingFace: 'https://huggingface.co/THUDM/glm-4-9b-chat',
      openRouter: 'https://openrouter.ai/models/zhipuai/glm-4.5-turbo',
    },
    icon: 'Brain',
    logo: '/icons/zhipu.png',
  },
  {
    id: 'gpt-oss',
    name: 'GPT‑OSS',
    provider: 'OpenAI Open Source',
    description: 'High‑capacity GPT‑based models under Apache 2.0 with flexible deployment.',
    specialties: ['general-purpose', 'language generation', 'flexible deployment'],
    capabilities: {
      reasoning: 86,
      coding: 88,
      creativity: 92,
      factuality: 89,
      safety: 91,
    },
    latency: { p50: 750, p95: 1480 },
    cost: 3.00, // $3.00 per 1M tokens (updated pricing)
    bestFor: ['General purpose language understanding and generation'],
    modelId: 'openai/gpt-4o-mini',
    links: {
      openRouter: 'https://openrouter.ai/models/openai/gpt-4o-mini',
    },
    icon: 'BookOpen',
    logo: '/icons/openai.png',
  },
  {
    id: 'llama4-maverick',
    name: 'Llama 4 Maverick',
    provider: 'Meta',
    description: 'Advanced instruction‑tuned model with strong multilingual and reasoning capabilities.',
    specialties: ['instruction following', 'multilingual', 'reasoning'],
    capabilities: {
      reasoning: 84,
      coding: 79,
      creativity: 87,
      factuality: 88,
      safety: 94,
    },
    latency: { p50: 420, p95: 890 },
    cost: 1.50, // $1.50 per 1M tokens (competitive pricing)
    bestFor: ['Instruction following', 'multilingual tasks', 'reasoning'],
    modelId: 'meta-llama/llama-3.3-70b-instruct',
    links: {
      openRouter: 'https://openrouter.ai/models/meta-llama/llama-3.3-70b-instruct',
    },
    icon: 'Mountain',
    logo: '/icons/meta.png',
  },
  {
    id: 'moonshot-kimi',
    name: 'MoonshotAI Kimi',
    provider: 'MoonshotAI',
    description: 'Advanced conversational AI with strong reasoning and coding.',
    specialties: ['conversational AI', 'reasoning', 'coding'],
    capabilities: {
      reasoning: 87,
      coding: 83,
      creativity: 85,
      factuality: 90,
      safety: 89,
    },
    latency: { p50: 580, p95: 1180 },
    cost: 2.00, // $2.00 per 1M tokens (updated pricing)
    bestFor: ['Coding', 'reasoning', 'conversational tasks'],
    modelId: 'moonshot/moonshot-v1-32k',
    links: {
      openRouter: 'https://openrouter.ai/models/moonshot/moonshot-v1-32k',
    },
    icon: 'Rocket',
    logo: '/icons/moonshot.png',
  },
  {
    id: 'qwen3-coder',
    name: 'Qwen3 Coder',
    provider: 'Alibaba',
    description: 'Specialized coding model with strong programming capabilities.',
    specialties: ['code generation', 'programming assistance', 'technical docs'],
    capabilities: {
      reasoning: 85,
      coding: 94,
      creativity: 81,
      factuality: 87,
      safety: 92,
    },
    latency: { p50: 720, p95: 1380 },
    cost: 1.80, // $1.80 per 1M tokens (coding optimized pricing)
    bestFor: ['Code generation', 'programming assistance', 'technical docs'],
    modelId: 'qwen/qwen-2.5-coder-32b-instruct',
    links: {
      openRouter: 'https://openrouter.ai/models/qwen/qwen-2.5-coder-32b-instruct',
    },
    icon: 'Code',
    logo: '/icons/alibaba.png',
  },
  {
    id: 'deepseek-chimera',
    name: 'TNG DeepSeek R1T2 Chimera',
    provider: 'TNG Tech',
    description: 'Advanced mixture‑of‑experts with strong reasoning and efficiency.',
    specialties: ['mixture-of-experts', 'reasoning', 'efficiency'],
    capabilities: {
      reasoning: 92,
      coding: 89,
      creativity: 79,
      factuality: 88,
      safety: 85,
    },
    latency: { p50: 520, p95: 980 },
    cost: 0.80, // $0.80 per 1M tokens (most cost-effective)
    bestFor: ['General NLP tasks', 'reasoning', 'complex analysis'],
    modelId: 'deepseek/deepseek-r1',
    links: {
      openRouter: 'https://openrouter.ai/models/deepseek/deepseek-r1',
    },
    icon: 'Layers3',
    logo: '/icons/tngtech.png',
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