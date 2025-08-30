import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { User, Bot } from 'lucide-react';
import { Message } from '../types';

interface ChatThreadProps {
  messages: Message[];
}

export const ChatThread: React.FC<ChatThreadProps> = ({ messages }) => {
  const bottomRef = useRef<HTMLDivElement>(null);
  const topRef = useRef<HTMLDivElement>(null);
  const [showScrollTop, setShowScrollTop] = useState(false);

  // Scroll to bottom on new message
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Show scroll-to-top button if not at top
  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    setShowScrollTop(e.currentTarget.scrollTop > 100);
  };

  const scrollToTop = () => {
    if (topRef.current) {
      topRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 md:space-y-6 custom-scrollbar relative" onScroll={handleScroll}>
      <div ref={topRef} />
      {messages.map((message, index) => (
        <motion.div
          key={message.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
          className={`flex gap-3 md:gap-4 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          {message.type === 'assistant' && (
            <div className="w-7 h-7 md:w-8 md:h-8 bg-gradient-to-br from-purple-500 to-cyan-500 rounded-full flex items-center justify-center flex-shrink-0">
              <Bot size={16} className="text-white" />
            </div>
          )}
          
          <div className={`max-w-[85%] md:max-w-[80%] ${message.type === 'user' ? 'order-1' : ''}`}>
            <div className={`p-3 md:p-4 rounded-2xl ${
              message.type === 'user'
                ? 'bg-gradient-to-r from-purple-500 to-cyan-500 text-white ml-auto'
                : 'bg-slate-800/50 backdrop-blur-xl border border-slate-600/30 text-slate-100'
            }`}>
              <p className="leading-relaxed text-sm md:text-base">{message.content}</p>
            </div>
            <p className="text-xs text-slate-500 mt-1 md:mt-2 px-2">
              {message.timestamp.toLocaleTimeString()}
            </p>
          </div>

          {message.type === 'user' && (
            <div className="w-7 h-7 md:w-8 md:h-8 bg-slate-700 rounded-full flex items-center justify-center flex-shrink-0">
              <User size={16} className="text-slate-300" />
            </div>
          )}
        </motion.div>
      ))}
      {/* Spacer to ensure last message is visible above input */}
      <div ref={bottomRef} className="h-4" />
      {showScrollTop && (
        <button
          onClick={scrollToTop}
          className="fixed bottom-24 right-8 z-20 bg-slate-800/80 text-white px-3 py-2 rounded-full shadow-lg hover:bg-slate-700 transition-colors text-xs md:text-sm"
        >
          Scroll to Top
        </button>
      )}
    </div>
  );
};