import React from 'react';
import { motion } from 'framer-motion';
import { User, Sparkles, RotateCcw, Share2, BarChart3, Trash2, Send } from 'lucide-react';
import { Message } from '../types';

interface ConversationProps {
  messages: Message[];
  routedModel?: string;
  confidence?: number;
  onContinue: (message: string) => void;
}

export const Conversation: React.FC<ConversationProps> = ({
  messages,
  routedModel = 'LLaMA 3',
  confidence = 82,
  onContinue
}) => {
  const [continueInput, setContinueInput] = React.useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (continueInput.trim()) {
      onContinue(continueInput.trim());
      setContinueInput('');
    }
  };

  return (
    <div className="flex-1 flex flex-col">
      {/* Routing Info Header */}
      <motion.div
        className="px-6 py-3 border-b border-white/10 flex items-center justify-between"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 px-3 py-1 bg-slate-800/50 rounded-full border border-white/10">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-300">
              Routed to: <span className="text-green-400 font-medium">{routedModel}</span> ({confidence}% confidence)
            </span>
          </div>
          <div className="flex items-center space-x-2 px-3 py-1 bg-cyan-500/20 rounded-full border border-cyan-400/30">
            <div className="w-2 h-2 bg-cyan-400 rounded-full"></div>
            <span className="text-sm text-cyan-400 font-medium">Critique pass: enabled</span>
          </div>
        </div>
      </motion.div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((message, index) => (
          <motion.div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
          >
            {message.sender === 'user' ? (
              <div className="flex items-start space-x-3 max-w-2xl">
                <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-purple-500 to-cyan-400 rounded-lg flex items-center justify-center order-2">
                  <User className="w-4 h-4 text-white" />
                </div>
                <div className="bg-slate-800/60 backdrop-blur-sm rounded-2xl rounded-tr-md p-4 border border-white/10 order-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-300">You</span>
                    <span className="text-xs text-gray-500">
                      {message.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-gray-100">{message.content}</p>
                </div>
              </div>
            ) : (
              <div className="flex items-start space-x-3 max-w-4xl">
                <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-purple-500 to-cyan-400 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-4 h-4 text-white" />
                </div>
                <div className="flex-1">
                  <div className="relative">
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-600/10 to-cyan-500/10 rounded-2xl blur-sm"></div>
                    <div className="relative bg-slate-800/40 backdrop-blur-md rounded-2xl rounded-tl-md p-6 border border-white/20">
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-medium bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
                          OrchestrateX
                        </span>
                        <span className="text-xs text-gray-500">
                          {message.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                      <div className="prose prose-invert max-w-none">
                        <p className="text-gray-100 leading-relaxed mb-4">{message.content}</p>
                      </div>
                      
                      {/* Action buttons */}
                      <div className="flex flex-wrap gap-2 pt-4 border-t border-white/10">
                        <motion.button
                          className="px-3 py-2 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg text-xs font-medium text-gray-300 hover:text-white transition-colors duration-200 flex items-center space-x-1"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <BarChart3 className="w-3 h-3" />
                          <span>Explain model selection</span>
                        </motion.button>
                        <motion.button
                          className="px-3 py-2 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg text-xs font-medium text-gray-300 hover:text-white transition-colors duration-200 flex items-center space-x-1"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <RotateCcw className="w-3 h-3" />
                          <span>Show routing scores</span>
                        </motion.button>
                        <motion.button
                          className="px-3 py-2 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg text-xs font-medium text-gray-300 hover:text-white transition-colors duration-200 flex items-center space-x-1"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <Share2 className="w-3 h-3" />
                          <span>Compare response quality</span>
                        </motion.button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        ))}
      </div>

      {/* Continue Input */}
      <div className="p-6 border-t border-white/10">
        <form onSubmit={handleSubmit} className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <input
              type="text"
              value={continueInput}
              onChange={(e) => setContinueInput(e.target.value)}
              placeholder="Continue the conversation..."
              className="w-full px-4 py-3 bg-slate-800/60 backdrop-blur-sm border border-white/10 rounded-xl text-gray-100 placeholder-gray-400 focus:outline-none focus:border-purple-400/50 focus:bg-slate-800/80 transition-all duration-200"
            />
            <Sparkles className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-purple-400" />
          </div>
          <motion.button
            type="submit"
            disabled={!continueInput.trim()}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-cyan-500 hover:from-purple-500 hover:to-cyan-400 disabled:from-gray-600 disabled:to-gray-700 text-white rounded-xl font-medium transition-all duration-200 flex items-center space-x-2 disabled:cursor-not-allowed"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Send className="w-4 h-4" />
          </motion.button>
        </form>
      </div>
    </div>
  );
};