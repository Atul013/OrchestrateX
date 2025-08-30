import React from 'react';
import { Sparkles } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-white/10">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-cyan-400 flex items-center justify-center">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <h1 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
          OrchestrateX
        </h1>
      </div>
      <nav className="flex items-center space-x-6">
        <a 
          href="#docs" 
          className="text-gray-300 hover:text-cyan-400 transition-colors duration-200 text-sm font-medium"
        >
          📚 Docs
        </a>
        <a 
          href="#api" 
          className="text-gray-300 hover:text-purple-400 transition-colors duration-200 text-sm font-medium flex items-center space-x-1"
        >
          <span>🔗 API</span>
        </a>
      </nav>
    </header>
  );
};