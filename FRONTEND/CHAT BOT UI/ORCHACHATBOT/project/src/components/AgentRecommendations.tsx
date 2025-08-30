import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { AgentCard } from './AgentCard';
import { AIAgent } from '../types';

interface AgentRecommendationsProps {
  agents: AIAgent[];
  onSelectAgent: (agent: AIAgent) => void;
}

export const AgentRecommendations: React.FC<AgentRecommendationsProps> = ({
  agents,
  onSelectAgent
}) => {
  const topRef = useRef<HTMLDivElement>(null);
  const [showScrollTop, setShowScrollTop] = useState(false);

  const handleScroll = (e: React.UIEvent<HTMLElement>) => {
    setShowScrollTop(e.currentTarget.scrollTop > 100);
  };

  const scrollToTop = () => {
    if (topRef.current) {
      topRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="h-full flex flex-col">
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        className="p-4 md:p-6 border-b border-slate-700/50 flex-shrink-0"
      >
        <h2 className="text-white text-lg md:text-xl font-semibold mb-2">Model Insights & Actions</h2>
        <p className="text-slate-400 text-sm md:text-base">Model Recommendations</p>
      </motion.div>

      <section
        className="flex-1 p-4 md:p-6 min-h-0 overflow-y-auto custom-scrollbar focus:scrollbar-thumb-slate-600 hover:scrollbar-thumb-slate-600 relative"
        tabIndex={0}
        aria-label="Agent Cards"
        onScroll={handleScroll}
      >
        <div ref={topRef} />
        <div
          className="grid grid-cols-2 md:grid-cols-3 gap-3 md:gap-4 w-full"
          style={{ minHeight: 0 }}
        >
          {agents.map((agent, index) => (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="flex"
            >
              <AgentCard agent={agent} onSelectAgent={onSelectAgent} />
            </motion.div>
          ))}
        </div>
        {showScrollTop && (
          <button
            onClick={scrollToTop}
            className="fixed bottom-24 right-8 z-20 bg-slate-800/80 text-white px-3 py-2 rounded-full shadow-lg hover:bg-slate-700 transition-colors text-xs md:text-sm"
          >
            Scroll to Top
          </button>
        )}
      </section>
    </div>
  );
};