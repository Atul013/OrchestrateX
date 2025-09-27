import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ExternalLink, Info } from 'lucide-react';
import { models } from '../config/models';

const CapabilityChart: React.FC<{ capabilities: any }> = ({ capabilities }) => {
  const maxValue = 100;
  
  return (
    <div className="space-y-3">
      {Object.entries(capabilities).map(([key, value]) => (
        <div key={key} className="flex items-center gap-3">
          <span className="text-sm text-white/70 capitalize w-20">{key}</span>
          <div className="flex-1 bg-white/10 rounded-full h-2">
            <motion.div
              className="bg-gradient-to-r from-primary to-cyan h-full rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${(Number(value) / maxValue) * 100}%` }}
              transition={{ duration: 1, delay: 0.2 }}
            />
          </div>
          <span className="text-sm text-white/60 w-8">{Number(value)}%</span>
        </div>
      ))}
    </div>
  );
};

const ModelCard: React.FC<{ model: any; index: number }> = ({ model, index }) => {
  const [isFlipped, setIsFlipped] = useState(false);
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, delay: index * 0.1 }}
        className="group perspective-1000"
        onHoverStart={() => setIsFlipped(true)}
        onHoverEnd={() => setIsFlipped(false)}
      >
        <motion.div
          className="relative w-full h-96 preserve-3d cursor-pointer"
          animate={{ rotateY: isFlipped ? 180 : 0 }}
          transition={{ duration: 0.6, type: "spring" }}
        >
          {/* Front of card */}
          <div className="absolute inset-0 backface-hidden bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-4 lg:p-6 hover:bg-white/15 transition-colors">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 lg:w-12 lg:h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center border border-white/30 flex-shrink-0">
                <img 
                  src={model.logo} 
                  alt={`${model.provider} logo`}
                  className="w-6 h-6 lg:w-8 lg:h-8 object-contain filter brightness-0 invert max-w-[24px] lg:max-w-[32px]"
                />
              </div>
              <div className="min-w-0">
                <h3 className="text-lg lg:text-xl font-display font-bold text-white truncate">{model.name}</h3>
                <p className="text-sm text-white/70 font-medium truncate">{model.provider}</p>
              </div>
            </div>
            
            <p className="text-white/90 mb-4 leading-relaxed text-sm line-clamp-3">{model.description}</p>
            
            <div className="flex flex-wrap gap-2 mb-4">
              {model.specialties.slice(0, 3).map((specialty: string) => (
                <span key={specialty} className="px-2 py-1 bg-primary/20 text-primary text-xs rounded-full border border-primary/30 whitespace-nowrap">
                  {specialty}
                </span>
              ))}
            </div>

            <div className="mt-auto">
              <div className="text-sm text-white/80 mb-2 font-semibold">Best for:</div>
              <ul className="space-y-1">
                {model.bestFor.slice(0, 2).map((use: string) => (
                  <li key={use} className="text-sm text-white/70 flex items-start gap-2">
                    <div className="w-1.5 h-1.5 bg-lime rounded-full mt-1.5 flex-shrink-0"></div>
                    <span className="line-clamp-2">{use}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Back of card */}
          <div className="absolute inset-0 backface-hidden rotate-y-180 bg-dark/90 backdrop-blur-xl rounded-2xl border border-white/30 p-4 lg:p-6 shadow-2xl">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 lg:w-10 lg:h-10 bg-white/20 backdrop-blur-sm rounded-lg flex items-center justify-center border border-white/30 flex-shrink-0">
                <img 
                  src={model.logo} 
                  alt={`${model.provider} logo`}
                  className="w-5 h-5 lg:w-6 lg:h-6 object-contain filter brightness-0 invert max-w-[20px] lg:max-w-[24px]"
                />
              </div>
              <h4 className="text-base lg:text-lg font-semibold text-white">Capabilities</h4>
            </div>
            <CapabilityChart capabilities={model.capabilities} />
            
            <div className="mt-4 lg:mt-6 pt-3 lg:pt-4 border-t border-white/20">
              <div className="grid grid-cols-2 gap-3 lg:gap-4 text-sm">
                <div>
                  <span className="text-white/70 text-xs lg:text-sm">Latency (p50)</span>
                  <div className="text-white font-semibold text-sm lg:text-base">{model.latency.p50}ms</div>
                </div>
                <div>
                  <span className="text-white/70 text-xs lg:text-sm">Cost/1M tokens</span>
                  <div className="text-white font-semibold text-sm lg:text-base">${model.cost}</div>
                </div>
              </div>
            </div>

            <button
              onClick={() => setShowModal(true)}
              className="mt-3 lg:mt-4 w-full px-3 lg:px-4 py-2 bg-gradient-to-r from-primary to-magenta rounded-lg text-white font-semibold hover:scale-105 transition-transform flex items-center justify-center gap-2 shadow-lg text-sm lg:text-base min-h-[44px] touch-manipulation"
            >
              Run Sample <ExternalLink className="w-4 h-4" />
            </button>
          </div>
        </motion.div>
      </motion.div>

      {/* Modal */}
      <AnimatePresence>
        {showModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowModal(false)}
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              className="bg-dark/90 backdrop-blur-xl border border-white/20 rounded-2xl p-6 max-w-lg w-full"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-2xl font-bold text-white mb-4">{model.name} Sample Response</h3>
              <div className="bg-white/10 rounded-lg p-4 mb-4">
                <p className="text-white/80 text-sm font-mono">
                  Model ID: {model.modelId}
                </p>
              </div>
              <div className="bg-dark/50 rounded-lg p-4 mb-4 border border-white/10">
                <p className="text-white/80 text-sm">
                  <strong>Access:</strong> Available via OpenRouter API<br/>
                  <strong>Best for:</strong> {model.bestFor.join(', ')}
                </p>
              </div>
              <div className="flex items-center gap-2 text-sm text-white/60 mb-4">
                <Info className="w-4 h-4" />
                <span>Why this model? {model.description}</span>
              </div>
              <div className="flex gap-2 mb-4">
                {model.links.huggingFace && (
                  <a
                    href={model.links.huggingFace}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-1 bg-white/20 rounded text-white text-sm hover:bg-white/30 transition-colors"
                  >
                    Hugging Face
                  </a>
                )}
                <a
                  href={model.links.openRouter}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-3 py-1 bg-white/20 rounded text-white text-sm hover:bg-white/30 transition-colors"
                >
                  OpenRouter
                </a>
              </div>
              <button
                onClick={() => setShowModal(false)}
                className="w-full px-4 py-2 bg-white/20 rounded-lg text-white hover:bg-white/30 transition-colors"
              >
                Close
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

const ModelsShowcase: React.FC = () => {
  return (
    <section className="py-12 lg:py-24 bg-gradient-to-b from-dark/95 to-dark">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-8 lg:mb-16"
        >
          <h2 className="text-3xl sm:text-4xl lg:text-6xl font-display font-bold text-white mb-4 lg:mb-6">
            Model Showcase
          </h2>
          <p className="text-lg sm:text-xl text-white/80 max-w-3xl mx-auto leading-relaxed px-2 lg:px-0">
            Six specialized AI models, each optimized for different tasks, working together to deliver the best possible results
          </p>
        </motion.div>

        {/* Mobile: 2-column grid (≤600px) */}
        <div className="mobile-model-grid lg:hidden">
          {models.map((model, index) => (
            <motion.div
              key={model.id}
              initial={{ opacity: 0, scale: 0.8, y: 20 }}
              whileInView={{ opacity: 1, scale: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ 
                duration: 0.6, 
                delay: index * 0.1,
                type: "spring",
                stiffness: 100
              }}
              className="mobile-model-card touch-manipulation"
            >
              {/* Model Header */}
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 bg-white/20 backdrop-blur-sm rounded-md flex items-center justify-center border border-white/30 flex-shrink-0">
                  <img 
                    src={model.logo} 
                    alt={`${model.provider} logo`}
                    className="w-3 h-3 object-contain filter brightness-0 invert max-w-[12px]"
                  />
                </div>
                <div className="min-w-0 flex-1">
                  <h3 className="text-sm font-bold text-white truncate">{model.name}</h3>
                  <p className="text-xs text-white/70 truncate">{model.provider}</p>
                </div>
              </div>

              {/* Description */}
              <p className="text-xs text-white/80 mb-3 line-clamp-2 flex-grow">
                {model.description}
              </p>

              {/* Key Stats */}
              <div className="grid grid-cols-2 gap-2 mb-3 text-xs">
                <div className="bg-white/5 rounded-lg p-2 text-center">
                  <div className="text-white font-semibold">{model.latency.p50}ms</div>
                  <div className="text-white/60">Latency</div>
                </div>
                <div className="bg-white/5 rounded-lg p-2 text-center">
                  <div className="text-white font-semibold">${model.cost}</div>
                  <div className="text-white/60">Per 1M</div>
                </div>
              </div>

              {/* Use Cases (truncated) */}
              <div className="mt-auto">
                <div className="text-xs text-white/70 mb-1">Best for:</div>
                <div className="text-xs text-white/80 line-clamp-1">
                  {model.bestFor.slice(0, 2).join(', ')}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Tablet and Mobile: Horizontal scroll (601px+) */}
        <div className="lg:hidden mobile-hide-scroll overflow-x-auto pb-4">
          <div className="flex gap-4 px-4" style={{ width: 'max-content' }}>
            {models.map((model, index) => (
              <div key={model.id} className="w-80 flex-shrink-0">
                <ModelCard model={model} index={index} />
              </div>
            ))}
          </div>
        </div>

        {/* Desktop: Grid layout */}
        <div className="hidden lg:grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {models.map((model, index) => (
            <ModelCard key={model.id} model={model} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default ModelsShowcase;