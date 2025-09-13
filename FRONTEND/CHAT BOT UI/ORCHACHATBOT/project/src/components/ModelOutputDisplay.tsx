import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { OrchestrateResponse, RefinementRequest } from '../services/orchestrateAPI';

interface ModelOutputDisplayProps {
  result: OrchestrateResponse;
  onRefineRequest?: (request: RefinementRequest) => void;
  isRefining?: boolean;
}

export const ModelOutputDisplay: React.FC<ModelOutputDisplayProps> = ({
  result,
  onRefineRequest,
  isRefining = false
}) => {
  const [selectedCritiqueIndex, setSelectedCritiqueIndex] = useState<number | null>(null);
  const [showCritiques, setShowCritiques] = useState(false);

  const handleRefineClick = () => {
    if (selectedCritiqueIndex !== null && onRefineRequest) {
      onRefineRequest({
        original_result: result,
        selected_critique_index: selectedCritiqueIndex
      });
    }
  };

  const successfulCritiques = result.critiques || [];

  return (
    <div className="bg-slate-800/50 rounded-lg border border-slate-700/50 p-4 space-y-4">
      {/* Primary Response Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
          <h3 className="text-white font-semibold">
            {result.primary_response.model_name}
          </h3>
        </div>
        
        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <span>{result.primary_response.tokens_used} tokens</span>
          <span>•</span>
          <span>${result.primary_response.cost_usd.toFixed(4)}</span>
          <span>•</span>
          <span>{result.primary_response.latency_ms}ms</span>
        </div>
      </div>

      {/* Primary Response */}
      <div className="bg-slate-900/50 rounded-lg p-4">
        <div className="text-slate-100 leading-relaxed prose prose-invert max-w-none">
          <ReactMarkdown
            components={{
              h1: ({children}) => <h1 className="text-xl font-bold text-white mb-3">{children}</h1>,
              h2: ({children}) => <h2 className="text-lg font-semibold text-white mb-2">{children}</h2>,
              h3: ({children}) => <h3 className="text-base font-medium text-white mb-2">{children}</h3>,
              p: ({children}) => <p className="text-slate-100 mb-2">{children}</p>,
              strong: ({children}) => <strong className="font-semibold text-white">{children}</strong>,
              em: ({children}) => <em className="italic text-slate-200">{children}</em>,
              ul: ({children}) => <ul className="list-disc list-inside mb-2 text-slate-100">{children}</ul>,
              ol: ({children}) => <ol className="list-decimal list-inside mb-2 text-slate-100">{children}</ol>,
              li: ({children}) => <li className="mb-1 text-slate-100">{children}</li>,
              code: ({children}) => <code className="bg-slate-800 text-cyan-400 px-1 py-0.5 rounded text-sm">{children}</code>,
              pre: ({children}) => <pre className="bg-slate-800 p-3 rounded-lg overflow-x-auto mb-3">{children}</pre>
            }}
          >
            {result.primary_response.response_text}
          </ReactMarkdown>
        </div>
      </div>

      {/* Critiques Section */}
      {successfulCritiques.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setShowCritiques(!showCritiques)}
              className="flex items-center space-x-2 text-slate-300 hover:text-white transition-colors"
            >
              <span className="font-medium">
                {successfulCritiques.length} Model{successfulCritiques.length !== 1 ? 's' : ''} Provided Feedback
              </span>
              <motion.svg
                animate={{ rotate: showCritiques ? 180 : 0 }}
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </motion.svg>
            </button>

            {showCritiques && (
              <span className="bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded-md text-xs">
                Refinement Available
              </span>
            )}
          </div>

          <AnimatePresence>
            {showCritiques && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="space-y-3"
              >
                {successfulCritiques.map((critique, index) => (
                  <motion.div
                    key={critique.model_name}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className={`border rounded-lg p-3 cursor-pointer transition-all ${
                      selectedCritiqueIndex === index
                        ? 'border-blue-500 bg-blue-500/10'
                        : 'border-slate-600 bg-slate-800/30 hover:border-slate-500'
                    }`}
                    onClick={() => setSelectedCritiqueIndex(
                      selectedCritiqueIndex === index ? null : index
                    )}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-200 font-medium">
                        {critique.model_name}
                      </span>
                      <div className="flex items-center space-x-2 text-xs text-slate-400">
                        <span>{critique.tokens_used} tokens</span>
                        <span>•</span>
                        <span>{critique.latency_ms}ms</span>
                      </div>
                    </div>
                    <p className="text-slate-300 text-sm">
                      {critique.critique_text}
                    </p>
                    {selectedCritiqueIndex === index && (
                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="mt-2 pt-2 border-t border-slate-600"
                      >
                        <span className="text-xs text-blue-400">
                          ✓ Selected for refinement
                        </span>
                      </motion.div>
                    )}
                  </motion.div>
                ))}

                {/* Refinement Button */}
                {selectedCritiqueIndex !== null && onRefineRequest && (
                  <motion.button
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    onClick={handleRefineClick}
                    disabled={isRefining}
                    className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-600 disabled:to-slate-700 text-white py-3 px-4 rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2"
                  >
                    {isRefining ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                        <span>Refining Response...</span>
                      </>
                    ) : (
                      <>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        <span>Refine Response with Selected Feedback</span>
                      </>
                    )}
                  </motion.button>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}

      {/* Summary Stats */}
      <div className="flex items-center justify-between pt-3 border-t border-slate-700/50">
        <div className="flex items-center space-x-4 text-xs text-slate-400">
          <span>Total: ${result.total_cost.toFixed(4)}</span>
          <span>•</span>
          <span>{result.api_calls} API calls</span>
          <span>•</span>
          <span>{result.success_rate.toFixed(1)}% success</span>
        </div>
        
        <span className="text-xs text-slate-500">
          {new Date().toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
};
