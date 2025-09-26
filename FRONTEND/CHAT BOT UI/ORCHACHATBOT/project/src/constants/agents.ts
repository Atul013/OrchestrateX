
import { AIAgent } from '../types';
import openaiLogo from '../new-logos/openai1-removebg-preview.png';
import zhipuLogo from '../new-logos/zhipu-removebg-preview.png';
import metaLogo from '../new-logos/meta-removebg-preview.png';
import moonshotLogo from '../new-logos/moonshot-removebg-preview.png';
import tngtechLogo from '../new-logos/tngtech.png';
import alibabaLogo from '../new-logos/alibaba.png';

export const AI_AGENTS: AIAgent[] = [
  {
    id: 'glm4.5',
    name: 'GLM4.5',
    shortDescription: '',
    detailedSuggestion: '',
    color: '#FFFFFF',
    gradient: 'from-white to-gray-100',
    icon: zhipuLogo,
    specialties: []
  },
  {
    id: 'gpt-oss',
    name: 'GPT‑OSS',
    shortDescription: '',
    detailedSuggestion: '',
    color: '#10A37F',
    gradient: 'from-emerald-500 to-teal-600',
    icon: openaiLogo,
    specialties: []
  },
  {
    id: 'llama4-maverick',
    name: 'Llama 4 Maverick',
    shortDescription: '',
    detailedSuggestion: '',
    color: '#FFC220',
    gradient: 'from-yellow-400 to-amber-500',
    icon: metaLogo,
    specialties: []
  },
  {
    id: 'moonshot-kimi',
    name: 'MoonshotAI Kimi',
    shortDescription: '',
    detailedSuggestion: '',
    color: '#F59E0B',
    gradient: 'from-amber-500 to-orange-600',
    icon: moonshotLogo,
    specialties: []
  },
  {
    id: 'qwen3-coder',
    name: 'Qwen3 Coder',
    shortDescription: '',
    detailedSuggestion: '',
    color: '#6B7280',
    gradient: 'from-gray-500 to-gray-600',
    icon: alibabaLogo,
    specialties: []
  },
  {
    id: 'deepseek-chimera',
    name: 'TNG DeepSeek R1T2 Chimera',
    shortDescription: '',
    detailedSuggestion: '',
    color: '#EC4899',
    gradient: 'from-pink-500 to-rose-600',
    icon: tngtechLogo,
    specialties: []
  }
];