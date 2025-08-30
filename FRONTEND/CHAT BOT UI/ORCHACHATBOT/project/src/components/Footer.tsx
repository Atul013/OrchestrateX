import React from 'react';
import { motion } from 'framer-motion';

export const Footer: React.FC = () => {
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5, delay: 1 }}
      className="text-center py-4 border-t border-slate-700/50"
    >
      <p className="text-slate-500 text-sm">
        © 2025 OrchestrateX. All rights reserved.
      </p>
      <div className="flex justify-center gap-6 mt-2">
        <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">
          Docs
        </a>
        <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">
          API
        </a>
        <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">
          Privacy
        </a>
        <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">
          Terms
        </a>
      </div>
    </motion.footer>
  );
};