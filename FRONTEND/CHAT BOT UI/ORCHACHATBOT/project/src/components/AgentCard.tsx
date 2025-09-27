import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { AIAgent } from '../types';

interface AgentCardProps {
  agent: AIAgent;
  onSelectAgent: (agent: AIAgent) => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({ agent, onSelectAgent }) => {
  const [isHovered, setIsHovered] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isHovered && cardRef.current) {
      cardRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, [isHovered]);

  return (
    <motion.div
      ref={cardRef}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.05 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className="relative group cursor-pointer"
    >
      <motion.div
        animate={{
          background: isHovered 
            ? `linear-gradient(135deg, ${agent.color}15, ${agent.color}25)`
            : 'rgba(30, 41, 59, 0.5)'
        }}
        transition={{ duration: 0.3 }}
        className="backdrop-blur-xl border border-slate-600/30 rounded-xl p-3 md:p-4 h-full hover:border-purple-500/30 transition-all hover:shadow-xl hover:shadow-purple-500/10"
      >
        {/* Agent Header */}
        <div className="flex items-center gap-2 md:gap-3 mb-3">
          <motion.div
            animate={{
              scale: isHovered ? 1.2 : 1,
              boxShadow: isHovered ? `0 0 20px ${agent.color}40` : '0 0 0px transparent'
            }}
            className="w-8 h-8 md:w-10 md:h-10 rounded-lg flex items-center justify-center overflow-hidden"
            style={{ backgroundColor: 'transparent' }}
          >
            {typeof agent.icon === 'string' && agent.icon ? (
              <img 
                src={agent.icon} 
                alt={agent.name + ' logo'} 
                className="w-full h-full object-contain" 
                style={{ 
                  filter: 'drop-shadow(0 0 4px rgba(0,0,0,0.3))',
                  background: 'transparent'
                }}
                onError={(e) => {
                  console.error(`Failed to load icon for ${agent.name}:`, agent.icon);
                  // Try alternative path with removebg version
                  const img = e.currentTarget as HTMLImageElement;
                  if (!img.src.includes('-removebg-preview')) {
                    const altPath = agent.icon.replace('.png', '-removebg-preview.png');
                    console.log(`Trying alternative path: ${altPath}`);
                    img.src = altPath;
                  } else {
                    // If both paths fail, hide image and show letter fallback
                    console.log(`Both logo paths failed for ${agent.name}, showing letter fallback`);
                    img.style.display = 'none';
                    const fallbackSpan = img.nextElementSibling as HTMLElement;
                    if (fallbackSpan) {
                      fallbackSpan.style.display = 'block';
                    }
                  }
                }}
                onLoad={() => console.log(`Successfully loaded logo for ${agent.name}:`, agent.icon)}
              />
            ) : null}
            <span 
              className="text-xl hidden font-bold" 
              style={{ 
                display: typeof agent.icon === 'string' && agent.icon ? 'none' : 'block',
                color: agent.color 
              }}
            >
              {agent.name.charAt(0)}
            </span>
          </motion.div>
          <div>
            <h3 className="text-white font-semibold text-sm md:text-base">{agent.name}</h3>
            <p className="text-slate-400 text-xs md:text-sm">{agent.shortDescription}</p>
          </div>
        </div>


        {/* Detailed Suggestion (appears on hover) */}
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{
            opacity: isHovered ? 1 : 0,
            height: isHovered ? 'auto' : 0
          }}
          transition={{ duration: 0.3 }}
          className="overflow-hidden"
        >
          <p className="text-slate-300 text-xs md:text-sm leading-relaxed mb-3 md:mb-4">
            {agent.detailedSuggestion}
          </p>
          
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              if (!agent.detailedSuggestion.includes("❌ Model unavailable")) {
                console.log('Button clicked for agent:', agent.name);
                onSelectAgent(agent);
              }
            }}
            className={`w-full ${
              agent.detailedSuggestion.includes("❌ Model unavailable")
                ? 'bg-red-500/80 cursor-not-allowed' 
                : `bg-gradient-to-r ${agent.gradient}`
            } text-white rounded-lg py-2 px-3 md:px-4 flex items-center justify-center gap-1 md:gap-2 font-medium hover:shadow-lg transition-shadow text-sm`}
            style={{ boxShadow: `0 4px 15px ${agent.color}25` }}
          >
            {agent.detailedSuggestion.includes("❌ Model unavailable") ? "API call failed" : "Apply suggestion"}
            <ArrowRight size={16} />
          </motion.button>
        </motion.div>

        {/* Default Apply Button (when not hovered) */}
        <motion.button
          animate={{ opacity: isHovered ? 0 : 1 }}
          transition={{ duration: 0.3 }}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            if (!agent.detailedSuggestion.includes("❌ Model unavailable")) {
              console.log('Default button clicked for agent:', agent.name);
              onSelectAgent(agent);
            }
          }}
          className={`w-full ${
            agent.detailedSuggestion.includes("❌ Model unavailable")
              ? 'bg-red-500/50 text-red-200 cursor-not-allowed' 
              : 'bg-slate-700/50 text-slate-300 hover:bg-slate-600/50'
          } rounded-lg py-2 px-3 md:px-4 flex items-center justify-center gap-1 md:gap-2 font-medium transition-colors text-sm ${
            isHovered ? 'pointer-events-none' : ''
          }`}
        >
          {agent.detailedSuggestion.includes("❌ Model unavailable") ? "API call failed" : "Apply suggestion"}
          <ArrowRight size={16} />
        </motion.button>
      </motion.div>
    </motion.div>
  );
};