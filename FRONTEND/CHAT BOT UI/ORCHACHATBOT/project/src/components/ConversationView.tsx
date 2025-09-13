import React from 'react';
import { motion } from 'framer-motion';
import { ChatThread } from './ChatThread';
import { ChatInput } from './ChatInput';
import { AgentRecommendations } from './AgentRecommendations';
import { Chat, AIAgent } from '../types';
import { RefinementRequest } from '../services/orchestrateAPI';

interface ConversationViewProps {
  currentChat: Chat;
  agents: AIAgent[];
  onSendMessage: (message: string) => void;
  onSelectAgent: (agent: AIAgent) => void;
  onRefineMessage?: (messageId: string, request: RefinementRequest) => void;
}

export const ConversationView: React.FC<ConversationViewProps> = ({
  currentChat,
  agents,
  onSendMessage,
  onSelectAgent,
  onRefineMessage
}) => {
  return (
  <main className="flex-1 flex flex-col md:flex-row h-screen min-h-0">
      {/* Chat Section */}
      <motion.section
        initial={{ width: '100%' }}
        animate={{ width: '100%' }}
        transition={{ duration: 0.6, ease: "easeInOut" }}
        className="flex flex-col md:w-1/2 border-r border-slate-700/50 min-h-0 h-screen"
        aria-label="Chat Section"
      >
        <div className="p-4 md:p-6 border-b border-slate-700/50 flex-shrink-0">
          <h2 className="text-white text-lg font-semibold">Conversation</h2>
          <div className="flex flex-wrap gap-2 mt-2">
            <span className="bg-green-500/20 text-green-400 px-2 py-1 rounded-md text-xs">
              Routed to: LLaMA 3 (0.82 confidence)
            </span>
            <span className="bg-cyan-500/20 text-cyan-400 px-2 py-1 rounded-md text-xs">
              Critique pass: enabled
            </span>
          </div>
        </div>
        
        <section className="flex-1 flex flex-col min-h-0 h-0">
          <div className="flex-1 min-h-0 overflow-y-auto custom-scrollbar focus:scrollbar-thumb-slate-600 hover:scrollbar-thumb-slate-600" tabIndex={0} aria-label="Chat Messages">
            <ChatThread messages={currentChat.messages} onRefineMessage={onRefineMessage} />
          </div>
          <div className="flex-shrink-0 sticky bottom-0 bg-slate-900/50 z-10">
            <ChatInput onSendMessage={onSendMessage} />
          </div>
        </section>
  </motion.section>

      {/* Agent Recommendations */}
      <motion.aside
        initial={{ width: '0%', opacity: 0 }}
        animate={{ width: '100%', opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeInOut", delay: 0.2 }}
        className="bg-slate-900/30 backdrop-blur-xl md:w-1/2 flex flex-col min-h-0 sticky top-0 h-screen"
        aria-label="Agent Recommendations"
        style={{ alignSelf: 'flex-start' }}
      >
        <AgentRecommendations agents={agents} onSelectAgent={onSelectAgent} />
      </motion.aside>
  </main>
  );
};