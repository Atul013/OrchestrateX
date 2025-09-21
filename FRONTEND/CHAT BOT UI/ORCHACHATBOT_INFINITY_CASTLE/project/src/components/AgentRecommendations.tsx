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
        className="p-4 md:p-6 border-b border-amber-600/30 flex-shrink-0 relative z-10 bg-gradient-to-r from-amber-900/20 via-orange-900/30 to-red-950/20 backdrop-blur-xl"
      >
        <h2 className="text-amber-200 text-lg md:text-xl font-semibold">Model Recommendations</h2>
      </motion.div>

      <section
        className="flex-1 p-4 md:p-6 min-h-0 overflow-y-auto custom-scrollbar focus:scrollbar-thumb-amber-600 hover:scrollbar-thumb-amber-600 relative"
        tabIndex={0}
        aria-label="Agent Cards"
        onScroll={handleScroll}
      >
        <div ref={topRef} />
        <div
          className="grid grid-cols-2 gap-3 md:gap-4 w-full auto-rows-fr"
          style={{ minHeight: 0 }}
        >
          {agents.map((agent, index) => (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="flex h-full"
            >
              <AgentCard agent={agent} onSelectAgent={onSelectAgent} />
            </motion.div>
          ))}
        </div>
        {showScrollTop && (
          <button
            onClick={scrollToTop}
            className="fixed bottom-24 right-8 z-20 bg-gradient-to-r from-amber-800/80 to-orange-800/80 text-amber-100 px-3 py-2 rounded-full shadow-lg hover:from-amber-700 hover:to-orange-700 transition-all border border-amber-600/30 text-xs md:text-sm"
          >
            Scroll to Top
          </button>
        )}
      </section>
    </div>
  );
};