import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="px-6 py-4 border-t border-white/10 bg-slate-900/30">
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-500">
          © 2025 OrchestrateX. All rights reserved.
        </p>
        <nav className="flex items-center space-x-6">
          <a href="#docs" className="text-sm text-gray-400 hover:text-cyan-400 transition-colors duration-200">
            Docs
          </a>
          <a href="#api" className="text-sm text-gray-400 hover:text-purple-400 transition-colors duration-200">
            API
          </a>
          <a href="#privacy" className="text-sm text-gray-400 hover:text-gray-300 transition-colors duration-200">
            Privacy
          </a>
          <a href="#terms" className="text-sm text-gray-400 hover:text-gray-300 transition-colors duration-200">
            Terms
          </a>
        </nav>
      </div>
    </footer>
  );
};