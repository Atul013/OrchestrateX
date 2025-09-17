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
          ? 'rgba(133, 93, 61, 0)' 
          : 'rgba(133, 93, 61, 0.8)'
      }}
      transition={{ duration: 0.3 }}
      className="backdrop-blur-xl border-b border-yellow-500/30 px-4 py-3 flex items-center justify-between relative z-10"
      style={{
        boxShadow: '0 4px 20px rgba(228, 138, 50, 0.3)'
      }}
    >
      <div className="flex items-center gap-4">
        <motion.a
          href="https://orchestratex-84388526388.us-central1.run.app"
          target="_blank"
          rel="noopener noreferrer"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          whileHover={{ scale: 1.05 }}
          className="top-left-brand flex items-center cursor-pointer"
        >
          <img 
            src="/finallogo.png" 
            alt="OrchestrateX Logo" 
            className="w-12 h-12 object-contain"
          />
        </motion.a>
      </div>

      <nav className="flex items-center gap-6">
        {headerLinks.map((link) => {
          const Icon = link.icon;
          return (
            <motion.a
              key={link.label}
              href={link.href}
              whileHover={{ scale: 1.05 }}
              className="flex items-center gap-2 text-yellow-200 hover:text-white transition-all duration-300 infinity-text-glow"
              style={{
                filter: 'drop-shadow(0 0 8px rgb(228, 138, 50))'
              }}
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