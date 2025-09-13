import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { User, Bot } from 'lucide-react';
import { Message } from '../types';
import { ModelOutputDisplay } from './ModelOutputDisplay';
import { RefinementRequest } from '../services/orchestrateAPI';

interface ChatThreadProps {
  messages: Message[];
  onRefineMessage?: (messageId: string, request: RefinementRequest) => void;
}

export const ChatThread: React.FC<ChatThreadProps> = ({ messages, onRefineMessage }) => {
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
      {messages.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-full text-slate-400 select-none">
          <span className="text-3xl md:text-4xl mb-4">💬</span>
          <p className="text-lg md:text-xl font-medium">Start a new conversation...</p>
          <p className="text-sm md:text-base mt-2 text-slate-500">Type your message below to begin.</p>
        </div>
      ) : (
        messages.map((message, index) => (
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
              {message.type === 'assistant' && message.orchestrationResult ? (
                // Show enhanced model output with critiques and refinement
                <ModelOutputDisplay 
                  result={message.orchestrationResult}
                  onRefineRequest={onRefineMessage ? (request) => onRefineMessage(message.id, request) : undefined}
                />
              ) : (
                // Show regular message
                <div className={`p-3 md:p-4 rounded-2xl ${
                  message.type === 'user'
                    ? 'bg-gradient-to-r from-purple-500 to-cyan-500 text-white ml-auto'
                    : 'bg-slate-800/50 backdrop-blur-xl border border-slate-600/30 text-slate-100'
                }`}>
                  <p className="leading-relaxed text-sm md:text-base whitespace-pre-wrap">{message.content}</p>
                  {message.refinementData?.isRefined && (
                    <div className="mt-2 pt-2 border-t border-slate-600/50">
                      <span className="text-xs text-blue-400 flex items-center">
                        <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        Refined Response
                      </span>
                    </div>
                  )}
                </div>
              )}
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
        ))
      )}
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