import openaiLogo from '../new-logos/openai1-removebg-preview.png';
import zhipuLogo from '../new-logos/zhipu-removebg-preview.png';
import metaLogo from '../new-logos/meta-removebg-preview.png';
import moonshotLogo from '../new-logos/moonshot-removebg-preview.png';
import tngtechLogo from '../new-logos/tngtech-removebg-preview.png';
import alibabaLogo from '../new-logos/alibaba-removebg-preview.png';

export const getModelLogo = (modelName: string): string => {
  const logoMap: Record<string, string> = {
    "GLM4.5": zhipuLogo,
    "TNG DeepSeek": tngtechLogo,
    "TNG DeepSeek R1T2 Chimera": tngtechLogo,
    "MoonshotAI Kimi": moonshotLogo,
    "GPT-OSS": openaiLogo,
    "GPT‑OSS": openaiLogo,
    "Llama 4 Maverick": metaLogo,
    "Qwen3": alibabaLogo,
    "Qwen3 Coder": alibabaLogo
  };
  
  return logoMap[modelName] || "🤖";
};

export const getModelConfig = (modelName: string) => {
  const modelConfigs: Record<string, any> = {
    "GLM4.5": { 
      color: "#8B5CF6", 
      gradient: "from-purple-500 to-violet-600", 
      icon: zhipuLogo,
      name: "GLM4.5"
    },
    "TNG DeepSeek": { 
      color: "#EC4899", 
      gradient: "from-pink-500 to-rose-600", 
      icon: tngtechLogo,
      name: "TNG DeepSeek"
    },
    "MoonshotAI Kimi": { 
      color: "#F59E0B", 
      gradient: "from-amber-500 to-orange-600", 
      icon: moonshotLogo,
      name: "MoonshotAI Kimi"
    },
    "GPT-OSS": { 
      color: "#10A37F", 
      gradient: "from-emerald-500 to-teal-600", 
      icon: openaiLogo,
      name: "GPT-OSS"
    },
    "Llama 4 Maverick": { 
      color: "#3B82F6", 
      gradient: "from-blue-500 to-indigo-600", 
      icon: metaLogo,
      name: "Llama 4 Maverick"
    },
    "Qwen3": { 
      color: "#F97316", 
      gradient: "from-orange-500 to-red-600", 
      icon: alibabaLogo,
      name: "Qwen3"
    }
  };
  
  return modelConfigs[modelName] || {
    color: "#6B7280",
    gradient: "from-gray-500 to-slate-500",
    icon: "🤖",
    name: modelName
  };
};