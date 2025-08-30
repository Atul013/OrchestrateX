import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { AIModel } from '../types';

interface ModelCardProps {
  model: AIModel;
  onApply: (modelId: string) => void;
  isExpanded?: boolean;
}

export const ModelCard: React.FC<ModelCardProps> = ({ 
  model, 
  onApply, 
  isExpanded = false 
}) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div
      className="relative"
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      layout
    >
      <motion.div
        className="bg-slate-800/40 backdrop-blur-sm rounded-xl border border-white/10 p-4 cursor-pointer relative overflow-hidden"
        whileHover={{ 
          scale: 1.05,
          backgroundColor: `${model.color}15`,
          borderColor: `${model.color}40`
        }}
        transition={{ 
          duration: 0.3, 
          ease: "easeOut" 
        }}
        style={{
          boxShadow: isHovered 
            ? `0 0 30px ${model.color}40, 0 10px 40px -10px ${model.color}20` 
            : '0 4px 20px rgba(0, 0, 0, 0.1)'
        }}
      >
        {/* Gradient overlay on hover */}
        <motion.div
          className="absolute inset-0 rounded-xl opacity-0"
          animate={{
            opacity: isHovered ? 0.1 : 0,
            background: `linear-gradient(135deg, ${model.color}20, transparent)`
          }}
          transition={{ duration: 0.3 }}
        />

        <div className="relative z-10">
          <div className="flex items-center space-x-3 mb-2">
            <motion.div
              className="w-8 h-8 rounded-lg flex items-center justify-center text-lg font-bold"
              style={{ 
                background: `linear-gradient(135deg, ${model.color}, ${model.color}CC)`,
                color: '#fff'
              }}
              whileHover={{ rotate: 5 }}
              transition={{ duration: 0.2 }}
            >
              {model.icon}
            </motion.div>
            <div>
              <h3 className="font-semibold text-gray-100">{model.name}</h3>
              <p className="text-xs text-gray-400">{model.specialty}</p>
            </div>
          </div>

          <AnimatePresence>
            {isHovered && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3, ease: "easeInOut" }}
                className="overflow-hidden"
              >
                <div className="mb-3 pt-2 border-t border-white/10">
                  <p className="text-xs text-gray-300 mb-2">Recommended for this query:</p>
                  <p className="text-sm text-gray-200">{model.description}</p>
                  
                  <div className="mt-2 flex flex-wrap gap-1">
                    {model.strengths.map((strength, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 text-xs rounded-full"
                        style={{ 
                          backgroundColor: `${model.color}20`,
                          color: model.color,
                          border: `1px solid ${model.color}40`
                        }}
                      >
                        {strength}
                      </span>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <motion.button
            onClick={() => onApply(model.id)}
            className="w-full mt-3 px-3 py-2 rounded-lg bg-slate-700/50 hover:bg-slate-600/50 text-sm font-medium text-gray-300 hover:text-white transition-all duration-200 flex items-center justify-between group"
            whileHover={{ x: 2 }}
            whileTap={{ scale: 0.98 }}
          >
            <span>Apply suggestion</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-200" />
          </motion.button>
        </div>
      </motion.div>
    </motion.div>
  );
};