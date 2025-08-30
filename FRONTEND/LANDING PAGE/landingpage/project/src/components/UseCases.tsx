import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Code, BookOpen, Globe, Sparkles, Calculator, ChevronRight } from 'lucide-react';
import { useCases } from '../config/models';

const iconMap = {
  Code,
  BookOpen,
  Globe,
  Sparkles,
  Calculator,
};

const UseCaseCard: React.FC<{ useCase: any; index: number }> = ({ useCase, index }) => {
  const [isHovered, setIsHovered] = useState(false);
  const IconComponent = iconMap[useCase.icon as keyof typeof iconMap];

  const demoContent = {
    'Code Generation & Review': (
      <div className="space-y-2 text-sm font-mono">
        <div className="text-green-400">✓ Syntax validation</div>
        <div className="text-yellow-400">⚠ Performance optimization suggested</div>
        <div className="text-blue-400">ℹ Best practices applied</div>
      </div>
    ),
    'Factual Q&A with Citations': (
      <div className="space-y-2 text-sm">
        <div className="text-white/80">Cross-referenced across 3 models</div>
        <div className="text-cyan">Source confidence: 94%</div>
        <div className="text-lime">2 citations verified</div>
      </div>
    ),
    'Multilingual Support': (
      <div className="space-y-2 text-sm">
        <div className="text-white/80">EN → JA: 98% accuracy</div>
        <div className="text-white/80">Technical terms preserved</div>
        <div className="text-cyan">Cultural context adapted</div>
      </div>
    ),
    'Creative Writing & Ideation': (
      <div className="space-y-2 text-sm">
        <div className="text-magenta">Creativity score: 92/100</div>
        <div className="text-white/80">Narrative coherence: ✓</div>
        <div className="text-lime">Original concepts: 5 detected</div>
      </div>
    ),
    'Mathematical Reasoning': (
      <div className="space-y-2 text-sm">
        <div className="text-green-400">Step 1: Problem decomposition ✓</div>
        <div className="text-yellow-400">Step 2: Solution validation ⚠</div>
        <div className="text-blue-400">Step 3: Alternative approaches ✓</div>
      </div>
    ),
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className="group relative bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-8 hover:bg-white/15 transition-all duration-300 overflow-hidden min-h-[280px] flex flex-col"
    >
      <div className="relative z-10">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-12 h-12 bg-gradient-to-r from-primary to-cyan rounded-xl flex items-center justify-center text-white group-hover:scale-110 transition-transform">
            <IconComponent className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-display font-bold text-white">{useCase.title}</h3>
        </div>

        <div className="flex-1 flex items-center">
          <p className="text-white/80 leading-relaxed max-w-md mx-auto text-center">{useCase.description}</p>
        </div>

        {/* Demo Content */}
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ 
            opacity: isHovered ? 1 : 0, 
            height: isHovered ? 'auto' : 0 
          }}
          transition={{ duration: 0.3 }}
          className="overflow-hidden mt-4"
        >
          <div className="bg-dark/50 rounded-lg p-4 border border-white/10 mb-4">
            {demoContent[useCase.title as keyof typeof demoContent]}
          </div>
        </motion.div>
      </div>

      {/* Background Effect */}
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-primary/20 via-cyan/20 to-magenta/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        initial={false}
      />
    </motion.div>
  );
};

const UseCases: React.FC = () => {
  return (
    <section className="py-24 bg-gradient-to-b from-dark to-dark/95">
      <div className="container mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-6xl font-display font-bold text-white mb-6">
            Use Cases
          </h2>
          <p className="text-xl text-white/80 max-w-3xl mx-auto leading-relaxed">
            Discover how OrchestrateX transforms complex AI tasks across industries and applications
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {useCases.map((useCase, index) => (
            <UseCaseCard key={index} useCase={useCase} index={index} />
          ))}
        </div>

        {/* Additional Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="mt-16 text-center"
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">50+</div>
              <div className="text-white/70">Use Cases Supported</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">99.7%</div>
              <div className="text-white/70">Task Success Rate</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">3.2x</div>
              <div className="text-white/70">Faster Than Single Model</div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default UseCases;