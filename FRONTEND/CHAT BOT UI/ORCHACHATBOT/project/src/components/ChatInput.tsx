import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Sparkles } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled = false }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  return (
    <div className="p-4 md:p-6 border-t border-slate-700/50 bg-slate-900/50 backdrop-blur-xl">
      <form onSubmit={handleSubmit}>
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <Sparkles className="absolute left-4 top-1/2 transform -translate-y-1/2 text-purple-400 z-10" size={20} />
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Continue the conversation..."
              disabled={disabled}
              className="w-full bg-slate-800/50 backdrop-blur-xl border border-slate-600/50 rounded-2xl pl-12 pr-4 py-3 md:py-4 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 disabled:opacity-50 disabled:cursor-not-allowed text-sm md:text-base"
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
            disabled={!message.trim() || disabled}
            className="h-10 px-3.5 bg-gradient-to-r from-purple-500 to-cyan-500 text-white rounded-xl flex items-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm shadow-lg transition-colors duration-200 flex-shrink-0"
          >
            <Send size={16} />
            <span className="hidden sm:inline">Send</span>
          </motion.button>
        </div>
      </form>
    </div>
  );
};