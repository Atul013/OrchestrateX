import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Sparkles } from 'lucide-react';
import { exampleQueries } from '../data/models';

interface PromptEntryProps {
  onSubmitPrompt: (prompt: string) => void;
}

export const PromptEntry: React.FC<PromptEntryProps> = ({ onSubmitPrompt }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmitPrompt(prompt.trim());
      setPrompt('');
    }
  };

  const handleExampleClick = (example: string) => {
    setPrompt(example);
  };

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-3xl w-full">
        {/* Main Heading */}
        <motion.div
          className="text-center mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        >
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-white via-cyan-200 to-purple-200 bg-clip-text text-transparent">
            Ask OrchestrateX
          </h1>
          <p className="text-lg text-gray-300 leading-relaxed">
            Route to the right model, invite critiques, and refine answers.
          </p>
        </motion.div>

        {/* Input Area */}
        <motion.form
          onSubmit={handleSubmit}
          className="mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
        >
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-cyan-500/20 rounded-2xl blur-lg"></div>
            <div className="relative bg-slate-800/40 backdrop-blur-md rounded-2xl border border-white/10 p-6">
              <div className="flex items-center space-x-4">
                <Sparkles className="w-6 h-6 text-purple-400 flex-shrink-0" />
                <input
                  type="text"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Ask anything about models, capabilities, or usage..."
                  className="flex-1 bg-transparent text-gray-100 placeholder-gray-400 text-lg focus:outline-none"
                />
                <motion.button
                  type="submit"
                  disabled={!prompt.trim()}
                  className="px-6 py-3 bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 disabled:from-gray-600 disabled:to-gray-700 text-white rounded-xl font-medium transition-all duration-200 flex items-center space-x-2 disabled:cursor-not-allowed"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <span>Send</span>
                  <Send className="w-4 h-4" />
                </motion.button>
              </div>
            </div>
          </div>
        </motion.form>

        {/* Example Queries */}
        <motion.div
          className="flex flex-wrap gap-3 justify-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
        >
          {exampleQueries.map((example, index) => (
            <motion.button
              key={index}
              onClick={() => handleExampleClick(example)}
              className="px-4 py-2 bg-slate-800/60 hover:bg-slate-700/60 border border-white/10 hover:border-purple-400/30 rounded-full text-sm text-gray-300 hover:text-gray-100 transition-all duration-200"
              whileHover={{ 
                scale: 1.05,
                boxShadow: '0 0 20px rgba(122, 90, 248, 0.3)'
              }}
              whileTap={{ scale: 0.95 }}
            >
              {example}
            </motion.button>
          ))}
        </motion.div>
      </div>
    </div>
  );
};