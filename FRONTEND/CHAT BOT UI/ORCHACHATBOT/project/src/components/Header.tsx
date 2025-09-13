import React from 'react';
import { motion } from 'framer-motion';
import { Book, Code, Shield, FileText } from 'lucide-react';

interface HeaderProps {
  isInitialState: boolean;
}

export const Header: React.FC<HeaderProps> = ({ 
  isInitialState 
}) => {
  const headerLinks = [
    { label: 'Docs', icon: Book, href: '#' },
    { label: 'API', icon: Code, href: '#' },
    { label: 'Privacy', icon: Shield, href: '#' },
    { label: 'Terms', icon: FileText, href: '#' }
  ];

  return (
    <motion.header 
      initial={false}
      animate={{
        backgroundColor: isInitialState 
          ? 'rgba(15, 23, 42, 0)' 
          : 'rgba(15, 23, 42, 0.8)'
      }}
      transition={{ duration: 0.3 }}
      className="backdrop-blur-xl border-b border-slate-700/50 px-4 py-3 flex items-center justify-between relative z-10"
    >
      <div className="flex items-center gap-4">
        {!isInitialState && (
          <motion.a
            href="/"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            whileHover={{ scale: 1.05 }}
            className="flex items-center gap-3 cursor-pointer"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-cyan-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">OX</span>
            </div>
            <span className="text-white font-semibold">OrchestrateX</span>
          </motion.a>
        )}
      </div>

      <nav className="flex items-center gap-6">
        {headerLinks.map((link) => {
          const Icon = link.icon;
          return (
            <motion.a
              key={link.label}
              href={link.href}
              whileHover={{ scale: 1.05 }}
              className="flex items-center gap-2 text-slate-300 hover:text-white transition-colors"
            >
              <Icon size={16} />
              <span className="hidden sm:inline">{link.label}</span>
            </motion.a>
          );
        })}
      </nav>
    </motion.header>
  );
};