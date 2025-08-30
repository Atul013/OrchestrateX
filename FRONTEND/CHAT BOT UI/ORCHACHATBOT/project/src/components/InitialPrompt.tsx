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
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">
            Ask OrchestrateX
          </h1>
          <p className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto">
            Route to the right model, invite critiques, and refine answers.
          </p>
        </motion.div>

        <motion.form
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          onSubmit={handleSubmit}
          className="relative mb-8"
        >
          <div className="relative">
            <Sparkles className="absolute left-4 top-1/2 transform -translate-y-1/2 text-purple-400" size={20} />
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Ask anything about models, capabilities, or usage..."
              className="w-full bg-slate-800/50 backdrop-blur-xl border border-slate-600/50 rounded-2xl pl-12 pr-16 py-4 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 text-lg"
            />
            <motion.button
              type="submit"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              disabled={!prompt.trim()}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-purple-500 to-cyan-500 text-white rounded-xl px-4 py-2 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
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
              className="bg-slate-800/30 backdrop-blur-xl border border-slate-600/30 text-slate-300 px-4 py-2 rounded-full hover:bg-slate-700/40 hover:text-white hover:border-purple-500/30 transition-all hover:shadow-lg hover:shadow-purple-500/10"
            >
              {example}
            </motion.button>
          ))}
        </motion.div>
      </div>
    </motion.div>
  );
};