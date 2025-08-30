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
}

export const models: ModelConfig[] = [
  {
    id: 'glm-4.5',
    name: 'GLM-4.5',
    provider: 'Zhipu',
    description: 'Mixture-of-experts with strong reasoning and coding. Great for complex tasks.',
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
    bestFor: ['Complex problem solving', 'Multi-step reasoning', 'Code architecture'],
  },
  {
    id: 'gpt-oss',
    name: 'GPT-OSS',
    provider: 'OpenAI OSS',
    description: 'Open-source GPT variants for flexible, general LLM tasks.',
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
    bestFor: ['General chat', 'Content generation', 'Flexible deployment'],
  },
  {
    id: 'llama-3',
    name: 'LLaMA 3',
    provider: 'Meta via Groq',
    description: 'Fast, instruction-tuned, multilingual. Solid for low-latency interactions.',
    specialties: ['instruction following', 'multilingual', 'low-latency'],
    capabilities: {
      reasoning: 88,
      coding: 80,
      creativity: 85,
      factuality: 90,
      safety: 92,
    },
    latency: { p50: 420, p95: 800 },
    cost: 0.001,
    bestFor: ['Real-time chat', 'Multilingual tasks', 'Cost optimization'],
  },
  {
    id: 'gemini',
    name: 'Google Gemini',
    provider: 'Google',
    description: 'Multimodal reasoning and coding with efficient API.',
    specialties: ['multimodal', 'reasoning', 'coding'],
    capabilities: {
      reasoning: 93,
      coding: 89,
      creativity: 82,
      factuality: 94,
      safety: 90,
    },
    latency: { p50: 580, p95: 1100 },
    cost: 0.0025,
    bestFor: ['Image analysis', 'Structured data', 'Factual queries'],
  },
  {
    id: 'claude',
    name: 'Anthropic Claude',
    provider: 'Anthropic',
    description: 'Safe, coherent dialogue and creative code/content.',
    specialties: ['safe dialogue', 'creative writing', 'helpful responses'],
    capabilities: {
      reasoning: 91,
      coding: 87,
      creativity: 95,
      factuality: 89,
      safety: 98,
    },
    latency: { p50: 720, p95: 1300 },
    cost: 0.004,
    bestFor: ['Creative writing', 'Long-form content', 'Safety-critical tasks'],
  },
  {
    id: 'falcon',
    name: 'Falcon',
    provider: 'TII',
    description: 'Open-source friendly for summarization and instruction following.',
    specialties: ['instruction-following', 'summarization', 'open-source'],
    capabilities: {
      reasoning: 75,
      coding: 70,
      creativity: 72,
      factuality: 85,
      safety: 80,
    },
    latency: { p50: 520, p95: 950 },
    cost: 0.0008,
    bestFor: ['Summarization', 'Simple tasks', 'Budget-conscious projects'],
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