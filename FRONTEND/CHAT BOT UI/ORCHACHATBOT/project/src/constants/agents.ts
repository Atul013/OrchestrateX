
import { AIAgent } from '../types';
import openaiLogo from '../new-logos/openai1-removebg-preview.png';
import zhipuLogo from '../new-logos/zhipu-removebg-preview.png';
import metaLogo from '../new-logos/meta-removebg-preview.png';
import moonshotLogo from '../new-logos/moonshot-removebg-preview.png';
import tngtechLogo from '../new-logos/tngtech-removebg-preview.png';
import alibabaLogo from '../new-logos/alibaba-removebg-preview.png';

export const AI_AGENTS: AIAgent[] = [
  {
    id: 'glm4.5',
    name: 'GLM4.5',
    shortDescription: '',
    detailedSuggestion: '',
    color: '#8B5CF6',
    gradient: 'from-purple-500 to-violet-600',
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
    color: '#3B82F6',
    gradient: 'from-blue-500 to-indigo-600',
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
    color: '#F97316',
    gradient: 'from-orange-500 to-red-600',
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