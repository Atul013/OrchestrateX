import React, { useEffect, useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { Brain, MessageSquare, Sparkles } from 'lucide-react';

const AnimatedPath: React.FC<{ inView: boolean; delay: number }> = ({ inView, delay }) => (
  <motion.svg
    className="absolute top-1/2 left-full w-24 h-12 -translate-y-1/2 hidden lg:block"
    viewBox="0 0 100 50"
    fill="none"
  >
    <motion.path
      d="M10,25 Q50,10 90,25"
      stroke="url(#gradient)"
      strokeWidth="2"
      fill="none"
      strokeDasharray="5,5"
      initial={{ pathLength: 0 }}
      animate={inView ? { pathLength: 1 } : { pathLength: 0 }}
      transition={{ duration: 1, delay, ease: "easeInOut" }}
    />
    <defs>
      <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stopColor="#3DE5FF" />
        <stop offset="100%" stopColor="#7A5AF8" />
      </linearGradient>
    </defs>
  </motion.svg>
);

const Step: React.FC<{
  number: number;
  title: string;
  description: string;
  icon: React.ReactNode;
  details: string[];
  delay: number;
  showPath?: boolean;
}> = ({ number, title, description, icon, details, delay, showPath = false }) => {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <div className="relative">
      <motion.div
        ref={ref}
        initial={{ opacity: 0, y: 50 }}
        animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
        transition={{ duration: 0.6, delay }}
        className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-8 hover:bg-white/15 transition-colors group"
      >
        {/* Step number */}
        <div className="flex items-center gap-4 mb-6">
          <div className="w-12 h-12 bg-gradient-to-r from-primary to-cyan rounded-full flex items-center justify-center text-white font-bold text-lg">
            {number}
          </div>
          <div className="w-12 h-12 bg-gradient-to-r from-cyan to-magenta rounded-xl flex items-center justify-center text-white group-hover:scale-110 transition-transform">
            {icon}
          </div>
        </div>

        {/* Content */}
        <h3 className="text-2xl font-display font-bold text-white mb-4">{title}</h3>
        <p className="text-white/80 mb-6 text-lg leading-relaxed">{description}</p>

        {/* Details */}
        <div className="space-y-2">
          {details.map((detail, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={inView ? { opacity: 1, x: 0 } : { opacity: 0, x: -20 }}
              transition={{ duration: 0.4, delay: delay + 0.2 + index * 0.1 }}
              className="flex items-center gap-2 text-white/70"
            >
              <div className="w-2 h-2 bg-lime rounded-full"></div>
              {detail}
            </motion.div>
          ))}
        </div>

        {/* Demo visualization */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={inView ? { opacity: 1 } : { opacity: 0 }}
          transition={{ duration: 0.8, delay: delay + 0.5 }}
          className="mt-6 p-4 bg-dark/50 rounded-lg border border-white/10"
        >
          {number === 1 && (
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm text-white/60">
                <div className="w-2 h-2 bg-cyan rounded-full animate-pulse"></div>
                Query classification: Code generation
              </div>
              <div className="flex items-center gap-2 text-sm text-white/60">
                <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
                Routing to: Qwen3 Coder (confidence: 0.89)
              </div>
            </div>
          )}
          {number === 2 && (
            <div className="space-y-2">
              <div className="text-sm text-white/60">GLM4.5: "Consider error handling"</div>
              <div className="text-sm text-white/60">Kimi: "Add type annotations"</div>
              <div className="text-sm text-white/60">GPT‑OSS: "Optimize for readability"</div>
            </div>
          )}
          {number === 3 && (
            <div className="space-y-2">
              <div className="text-sm text-green-400">✓ Incorporated 3 valid critiques</div>
              <div className="text-sm text-white/60">Final score: 0.94 (+0.15)</div>
            </div>
          )}
        </motion.div>
      </motion.div>
      {showPath && <AnimatedPath inView={inView} delay={delay + 0.8} />}
    </div>
  );
};

const HowItWorks: React.FC = () => {
  const steps = [
    {
      title: "Intelligent Model Selection",
      description: "Classify domain, estimate complexity, route based on strengths.",
      icon: <Brain className="w-6 h-6" />,
      details: [
        "Domain classification (code, math, creative, factual)",
        "Complexity estimation and resource requirements",
        "Model capability matching and confidence scoring"
      ]
    },
    {
      title: "Multi-Agent Critique",
      description: "Other models highlight gaps across accuracy, clarity, completeness.",
      icon: <MessageSquare className="w-6 h-6" />,
      details: [
        "Parallel critique generation from complementary models",
        "Severity scoring and relevance filtering",
        "Tag-based categorization (accuracy, clarity, completeness)"
      ]
    },
    {
      title: "Refine & Deliver",
      description: "Incorporate valid critiques, stop at convergence, return the best answer.",
      icon: <Sparkles className="w-6 h-6" />,
      details: [
        "Selective critique integration based on validation",
        "Convergence detection to prevent over-refinement",
        "Quality scoring and improvement tracking"
      ]
    }
  ];

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
            How It Works
          </h2>
          <p className="text-xl text-white/80 max-w-3xl mx-auto leading-relaxed">
            Three intelligent steps that transform single-model limitations into collective AI intelligence
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12">
          {steps.map((step, index) => (
            <Step
              key={index}
              number={index + 1}
              title={step.title}
              description={step.description}
              icon={step.icon}
              details={step.details}
              delay={index * 0.2}
              showPath={index < steps.length - 1}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;