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
            className="w-8 h-8 md:w-10 md:h-10 rounded-lg flex items-center justify-center text-white font-bold text-sm md:text-base"
            style={{ backgroundColor: agent.color }}
          >
            {typeof agent.icon === 'string' && (agent.icon.endsWith('.png') || agent.icon.endsWith('.jpeg'))
              ? <img src={agent.icon} alt={agent.name + ' logo'} className="w-7 h-7 md:w-9 md:h-9 object-contain" />
              : agent.icon}
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
              console.log('Button clicked for agent:', agent.name);
              onSelectAgent(agent);
            }}
            className={`w-full bg-gradient-to-r ${agent.gradient} text-white rounded-lg py-2 px-3 md:px-4 flex items-center justify-center gap-1 md:gap-2 font-medium hover:shadow-lg transition-shadow text-sm`}
            style={{ boxShadow: `0 4px 15px ${agent.color}25` }}
          >
            Apply suggestion
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
            console.log('Default button clicked for agent:', agent.name);
            onSelectAgent(agent);
          }}
          className={`w-full bg-slate-700/50 text-slate-300 rounded-lg py-2 px-3 md:px-4 flex items-center justify-center gap-1 md:gap-2 font-medium hover:bg-slate-600/50 transition-colors text-sm ${
            isHovered ? 'pointer-events-none' : ''
          }`}
        >
          Apply suggestion
          <ArrowRight size={16} />
        </motion.button>
      </motion.div>
    </motion.div>
  );
};