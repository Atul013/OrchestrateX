import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Sparkles } from 'lucide-react';
import { EXAMPLE_PROMPTS } from '../constants/examples';

interface InitialPromptProps {
  onSubmitPrompt: (prompt: string) => void;
}

export const InitialPrompt: React.FC<InitialPromptProps> = ({ onSubmitPrompt }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmitPrompt(prompt.trim());
    }
  };

  const handleExampleClick = (example: string) => {
    setPrompt(example);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="flex-1 flex items-center justify-center px-4"
    >
      <div className="max-w-4xl w-full">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-4 infinity-text-glow">
            Enter the Infinity Castle
          </h1>
          <p className="text-yellow-200 text-lg md:text-xl max-w-2xl mx-auto">
            Navigate the endless dimensions of AI intelligence and orchestration.
          </p>
        </motion.div>

        <motion.form
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          onSubmit={handleSubmit}
          className="mb-8"
        >
          <div className="flex items-center gap-2">
            <div className="relative flex-1">
              <Sparkles className="absolute left-4 top-1/2 transform -translate-y-1/2 text-purple-400" size={20} />
              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Ask anything about models, capabilities, or usage..."
                className="w-full bg-slate-800/50 backdrop-blur-xl border border-slate-600/50 rounded-2xl pl-12 pr-4 py-4 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 text-lg"
              />
            </div>
            <motion.button
              type="submit"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              transition={{ 
                type: "spring", 
                stiffness: 400, 
                damping: 25,
                duration: 0.15 
              }}
              disabled={!prompt.trim()}
              className="h-10 px-3.5 infinity-button text-white rounded-xl flex items-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm shadow-lg transition-all duration-300 flex-shrink-0"
            >
              <Send size={16} />
              <span className="hidden sm:inline">Send</span>
            </motion.button>
          </div>
        </motion.form>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="flex flex-wrap justify-center gap-3"
        >
          {EXAMPLE_PROMPTS.map((example, index) => (
            <motion.button
              key={index}
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleExampleClick(example)}
              className="bg-amber-900/30 backdrop-blur-xl border border-yellow-500/30 text-yellow-200 px-4 py-2 rounded-full hover:bg-orange-800/40 hover:text-white hover:border-red-400/50 transition-all duration-300 hover:shadow-lg hover:shadow-yellow-500/20 infinity-text-glow"
            >
              {example}
            </motion.button>
          ))}
        </motion.div>
      </div>
    </motion.div>
  );
};