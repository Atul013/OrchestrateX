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
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative flex items-center">
          <Sparkles className="absolute left-4 top-1/2 transform -translate-y-1/2 text-purple-400 z-10" size={20} />
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Continue the conversation..."
            disabled={disabled}
            className="w-full bg-slate-800/50 backdrop-blur-xl border border-slate-600/50 rounded-2xl pl-12 pr-20 py-3 md:py-4 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 disabled:opacity-50 disabled:cursor-not-allowed text-sm md:text-base"
          />
          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={!message.trim() || disabled}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-purple-500 to-cyan-500 text-white rounded-xl px-3 py-2 md:px-4 md:py-2 flex items-center gap-1 md:gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity font-medium text-sm"
          >
            <Send size={16} />
            <span className="hidden sm:inline">Send</span>
          </motion.button>
        </div>
      </form>
    </div>
  );
};