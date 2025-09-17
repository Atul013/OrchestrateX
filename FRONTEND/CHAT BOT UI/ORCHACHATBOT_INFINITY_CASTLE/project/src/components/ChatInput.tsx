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
    <div className="p-4 md:p-6 border-t border-amber-600/30 bg-gradient-to-r from-amber-900/30 via-orange-900/40 to-red-950/30 backdrop-blur-xl">
      <form onSubmit={handleSubmit}>
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <Sparkles className="absolute left-4 top-1/2 transform -translate-y-1/2 text-amber-400 z-10" size={20} />
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Continue the conversation..."
              disabled={disabled}
              className="w-full bg-gradient-to-r from-amber-900/30 via-orange-900/20 to-red-950/30 backdrop-blur-xl border border-amber-600/50 rounded-2xl pl-12 pr-4 py-3 md:py-4 text-amber-100 placeholder-amber-400/70 focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500/50 disabled:opacity-50 disabled:cursor-not-allowed text-sm md:text-base shadow-lg"
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
            className="h-10 px-3.5 bg-gradient-to-r from-amber-500 via-orange-500 to-red-600 hover:from-amber-400 hover:via-orange-400 hover:to-red-500 text-white rounded-xl flex items-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm shadow-xl transition-all duration-200 flex-shrink-0 border border-amber-600/30"
          >
            <Send size={16} />
            <span className="hidden sm:inline">Send</span>
          </motion.button>
        </div>
      </form>
    </div>
  );
};