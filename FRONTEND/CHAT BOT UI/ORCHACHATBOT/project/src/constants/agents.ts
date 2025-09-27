
import { AIAgent } from '../types';

// Use public directory paths for transparent logos
const openaiLogo = '/logos/openai.png';
const zhipuLogo = '/logos/zhipu.png';
const metaLogo = '/logos/meta.png';
const moonshotLogo = '/logos/moonshot.png';
const tngtechLogo = '/logos/tngtech.png';
const alibabaLogo = '/logos/alibaba.png';

export const AI_AGENTS: AIAgent[] = [
  {
    id: 'glm4.5',
    name: 'GLM4.5',
    shortDescription: 'Advanced Chinese language model',
    detailedSuggestion: 'Perfect for Chinese language tasks, bilingual conversations, and complex reasoning with strong performance in both Chinese and English contexts.',
    color: '#FFFFFF',
    gradient: 'from-white to-gray-100',
    icon: zhipuLogo,
    specialties: ['Chinese Language', 'Bilingual', 'Reasoning']
  },
  {
    id: 'gpt-oss',
    name: 'GPT‑OSS',
    shortDescription: 'Open-source GPT variant',
    detailedSuggestion: 'Excellent for general purpose tasks, creative writing, code generation, and problem-solving with high quality responses across diverse domains.',
    color: '#10A37F',
    gradient: 'from-emerald-500 to-teal-600',
    icon: openaiLogo,
    specialties: ['General Purpose', 'Creative Writing', 'Code Generation']
  },
  {
    id: 'llama4-maverick',
    name: 'Llama 4 Maverick',
    shortDescription: 'Meta\'s advanced reasoning model',
    detailedSuggestion: 'Specialized in complex reasoning, scientific analysis, and research tasks with strong performance in logical thinking and data interpretation.',
    color: '#FFC220',
    gradient: 'from-yellow-400 to-amber-500',
    icon: metaLogo,
    specialties: ['Reasoning', 'Scientific Analysis', 'Research']
  },
  {
    id: 'moonshot-kimi',
    name: 'MoonshotAI Kimi',
    shortDescription: 'Long-context conversation model',
    detailedSuggestion: 'Ideal for long document analysis, extended conversations, and complex multi-step tasks requiring extensive context understanding.',
    color: '#F59E0B',
    gradient: 'from-amber-500 to-orange-600',
    icon: moonshotLogo,
    specialties: ['Long Context', 'Document Analysis', 'Extended Conversations']
  },
  {
    id: 'qwen3-coder',
    name: 'Qwen3 Coder',
    shortDescription: 'Alibaba\'s coding specialist',
    detailedSuggestion: 'Optimized for programming tasks, code review, debugging, and software development with strong multilingual coding capabilities.',
    color: '#6B7280',
    gradient: 'from-gray-500 to-gray-600',
    icon: alibabaLogo,
    specialties: ['Programming', 'Code Review', 'Debugging']
  },
  {
    id: 'deepseek-chimera',
    name: 'TNG DeepSeek R1T2 Chimera',
    shortDescription: 'Advanced reasoning and coding',
    detailedSuggestion: 'Combines deep reasoning with exceptional coding abilities, perfect for complex algorithmic problems and advanced software architecture.',
    color: '#EC4899',
    gradient: 'from-pink-500 to-rose-600',
    icon: tngtechLogo,
    specialties: ['Advanced Reasoning', 'Complex Algorithms', 'Software Architecture']
  }
];