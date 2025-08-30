import { AIAgent } from '../types';

export const AI_AGENTS: AIAgent[] = [
  {
    id: 'glm-4.5',
    name: 'GLM-4.5',
    shortDescription: 'Great for multi-step reasoning and analysis',
    detailedSuggestion: 'Excels at complex logical reasoning, mathematical problem-solving, and multi-step analytical tasks. Best choice for structured thinking and detailed explanations.',
    color: '#8B5CF6',
    gradient: 'from-purple-500 to-violet-600',
    icon: '⚡',
    specialties: ['Reasoning', 'Analysis', 'Mathematics']
  },
  {
    id: 'gpt-oss',
    name: 'GPT-OSS',
    shortDescription: 'Flexible general language model',
    detailedSuggestion: 'Versatile open-source model perfect for general conversation, creative writing, and balanced responses. Ideal for most everyday tasks requiring natural language understanding.',
    color: '#10B981',
    gradient: 'from-emerald-500 to-teal-600',
    icon: '🚀',
    specialties: ['General Purpose', 'Creative Writing', 'Conversation']
  },
  {
    id: 'llama-3',
    name: 'LLaMA 3',
    shortDescription: 'Fast, multilingual, open-source',
    detailedSuggestion: 'High-performance model with excellent multilingual capabilities and fast inference. Perfect for code generation, translation tasks, and efficient processing.',
    color: '#3B82F6',
    gradient: 'from-blue-500 to-indigo-600',
    icon: '⚡',
    specialties: ['Multilingual', 'Code Generation', 'Fast Processing']
  },
  {
    id: 'gemini',
    name: 'Gemini',
    shortDescription: 'Multimodal reasoning and understanding',
    detailedSuggestion: 'Advanced multimodal capabilities for understanding images, documents, and complex data. Excellent for visual analysis, document processing, and creative tasks.',
    color: '#F59E0B',
    gradient: 'from-amber-500 to-orange-600',
    icon: '💎',
    specialties: ['Multimodal', 'Visual Analysis', 'Creative Tasks']
  },
  {
    id: 'claude',
    name: 'Claude',
    shortDescription: 'Clear, safe dialogue and analysis',
    detailedSuggestion: 'Focused on helpful, harmless, and honest responses. Excellent for detailed analysis, research tasks, and nuanced conversations requiring careful consideration.',
    color: '#EC4899',
    gradient: 'from-pink-500 to-rose-600',
    icon: '🧠',
    specialties: ['Analysis', 'Research', 'Safety']
  },
  {
    id: 'falcon',
    name: 'Falcon',
    shortDescription: 'Open-source friendly alternative',
    detailedSuggestion: 'Efficient open-source model with strong performance across various tasks. Great for privacy-conscious applications and customizable solutions.',
    color: '#F97316',
    gradient: 'from-orange-500 to-red-600',
    icon: '🦅',
    specialties: ['Open Source', 'Privacy', 'Customizable']
  }
];