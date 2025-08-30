import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { ModelCard } from './ModelCard';
import { aiModels } from '../data/models';

interface ModelRecommendationsProps {
  isVisible: boolean;
  onClose: () => void;
  onApplyModel: (modelId: string) => void;
}

export const ModelRecommendations: React.FC<ModelRecommendationsProps> = ({
  isVisible,
  onClose,
  onApplyModel
}) => {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ x: '100%', opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: '100%', opacity: 0 }}
          transition={{ duration: 0.4, ease: "easeInOut" }}
          className="fixed right-0 top-0 bottom-0 w-96 bg-slate-900/80 backdrop-blur-lg border-l border-white/10 z-50"
        >
          <div className="h-full flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-white/10">
              <div>
                <h2 className="text-lg font-bold text-gray-100">Model Insights & Actions</h2>
                <p className="text-sm text-gray-400 mt-1">Model Recommendations</p>
              </div>
              <motion.button
                onClick={onClose}
                className="p-2 rounded-lg hover:bg-white/10 text-gray-400 hover:text-gray-200 transition-colors duration-200"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                <X className="w-5 h-5" />
              </motion.button>
            </div>

            {/* Model Cards */}
            <div className="flex-1 overflow-y-auto p-6">
              <div className="grid grid-cols-2 gap-4">
                {aiModels.map((model, index) => (
                  <motion.div
                    key={model.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ 
                      duration: 0.3, 
                      delay: index * 0.1,
                      ease: "easeOut"
                    }}
                  >
                    <ModelCard
                      model={model}
                      onApply={onApplyModel}
                    />
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};