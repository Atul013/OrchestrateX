import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Zap, Clock, DollarSign, RotateCcw } from 'lucide-react';
import { models } from '../config/models';

const LiveRoutingDemo: React.FC = () => {
  const [selectedPrompt, setSelectedPrompt] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [iteration, setIteration] = useState(0);

  const examplePrompts = [
    {
      category: 'Coding',
      text: 'Write a Python function to implement a binary search tree with insert, search, and delete operations.',
      expectedModel: 'GLM-4.5'
    },
    {
      category: 'Math',
      text: 'Solve this differential equation: dy/dx = 3x²y with initial condition y(0) = 2',
      expectedModel: 'Google Gemini'
    },
    {
      category: 'Translation',
      text: 'Translate this technical document from English to Japanese while preserving technical terminology.',
      expectedModel: 'LLaMA 3'
    },
    {
      category: 'Creative',
      text: 'Write a compelling short story about AI consciousness in exactly 500 words.',
      expectedModel: 'Anthropic Claude'
    }
  ];

  const runDemo = async () => {
    if (!selectedPrompt) return;

    setIsRunning(true);
    setResults(null);

    // Find the expected model for this prompt type
    const promptData = examplePrompts.find(p => p.text === selectedPrompt);
    const expectedModel = models.find(m => m.name === promptData?.expectedModel) || models[0];

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Generate realistic but randomized results
    const confidence = 0.75 + Math.random() * 0.2;
    const latency = expectedModel.latency.p50 + Math.random() * 200;
    const cost = expectedModel.cost * (0.8 + Math.random() * 0.4);

    setResults({
      selectedModel: expectedModel,
      confidence,
      latency: Math.round(latency),
      cost: cost.toFixed(4),
      iterations: [
        { version: 'v1.0', improvements: [] },
        { version: 'v1.1', improvements: ['Accuracy +8%', 'Structure +12%'] },
        { version: 'v2.0', improvements: ['Accuracy +12%', 'Clarity +18%', 'Completeness +5%'] }
      ]
    });

    setIteration(0);
    setIsRunning(false);

    // Animate through iterations
    setTimeout(() => setIteration(1), 1000);
    setTimeout(() => setIteration(2), 2000);
  };

  const runAgain = () => {
    setResults(null);
    setIteration(0);
    runDemo();
  };

  return (
    <section className="py-24 bg-gradient-to-b from-dark/95 to-dark">
      <div className="container mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-6xl font-display font-bold text-white mb-6">
            Live Routing Demo
          </h2>
          <p className="text-xl text-white/80 max-w-3xl mx-auto leading-relaxed">
            See how OrchestrateX intelligently selects the best model and refines responses through multi-agent critique loops
          </p>
        </motion.div>

        <div className="max-w-4xl mx-auto">
          {/* Prompt Selection */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-8 mb-8"
          >
            <h3 className="text-2xl font-display font-bold text-white mb-6">Choose a Task</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              {examplePrompts.map((prompt, index) => (
                <motion.button
                  key={index}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setSelectedPrompt(prompt.text)}
                  className={`p-4 rounded-xl border text-left transition-all ${
                    selectedPrompt === prompt.text
                      ? 'bg-primary/20 border-primary text-white'
                      : 'bg-white/5 border-white/20 text-white/80 hover:bg-white/10'
                  }`}
                >
                  <div className="font-semibold mb-2 text-primary">{prompt.category}</div>
                  <div className="text-sm leading-relaxed">{prompt.text.slice(0, 100)}...</div>
                </motion.button>
              ))}
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={runDemo}
                disabled={!selectedPrompt || isRunning}
                className="flex-1 px-6 py-3 bg-gradient-to-r from-primary to-magenta rounded-xl text-white font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isRunning ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    Run Demo
                  </>
                )}
              </motion.button>

              {results && (
                <motion.button
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={runAgain}
                  className="px-6 py-3 bg-white/20 rounded-xl text-white font-semibold flex items-center justify-center gap-2 hover:bg-white/30 transition-colors"
                >
                  <RotateCcw className="w-5 h-5" />
                  Run Again
                </motion.button>
              )}
            </div>
          </motion.div>

          {/* Results */}
          <AnimatePresence>
            {results && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.6 }}
                className="space-y-8"
              >
                {/* Model Selection */}
                <div className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-8">
                  <h3 className="text-2xl font-display font-bold text-white mb-6">Model Selection</h3>
                  
                  <div className="flex items-center gap-6 mb-6">
                    <div className="w-16 h-16 bg-gradient-to-r from-primary to-cyan rounded-2xl flex items-center justify-center text-white font-bold text-xl">
                      {results.selectedModel.name.charAt(0)}
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-white">{results.selectedModel.name}</div>
                      <div className="text-white/60">{results.selectedModel.provider}</div>
                    </div>
                    <motion.div
                      initial={{ scaleX: 0 }}
                      animate={{ scaleX: 1 }}
                      className="flex-1 h-1 bg-gradient-to-r from-primary to-cyan origin-left rounded-full"
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="flex items-center gap-3">
                      <Zap className="w-6 h-6 text-cyan" />
                      <div>
                        <div className="text-white/60 text-sm">Confidence</div>
                        <div className="text-white font-bold">{(results.confidence * 100).toFixed(0)}%</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Clock className="w-6 h-6 text-lime" />
                      <div>
                        <div className="text-white/60 text-sm">Est. Latency</div>
                        <div className="text-white font-bold">{results.latency}ms</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <DollarSign className="w-6 h-6 text-magenta" />
                      <div>
                        <div className="text-white/60 text-sm">Est. Cost</div>
                        <div className="text-white font-bold">${results.cost}</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Critique Timeline */}
                <div className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-8">
                  <h3 className="text-2xl font-display font-bold text-white mb-6">Critique Loop Timeline</h3>
                  
                  <div className="space-y-4">
                    {results.iterations.map((iter: any, index: number) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0.3 }}
                        animate={{ 
                          opacity: iteration >= index ? 1 : 0.3,
                          scale: iteration === index ? 1.02 : 1
                        }}
                        className={`flex items-center gap-4 p-4 rounded-xl border ${
                          iteration >= index 
                            ? 'bg-white/10 border-white/20' 
                            : 'bg-white/5 border-white/10'
                        }`}
                      >
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                          iteration >= index 
                            ? 'bg-gradient-to-r from-primary to-cyan text-white' 
                            : 'bg-white/20 text-white/50'
                        }`}>
                          {index + 1}
                        </div>
                        <div className="flex-1">
                          <div className="text-white font-semibold">{iter.version}</div>
                          <div className="flex flex-wrap gap-2 mt-2">
                            {iter.improvements.map((improvement: string, i: number) => (
                              <motion.span
                                key={i}
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: iteration >= index ? 1 : 0.5, scale: 1 }}
                                transition={{ delay: i * 0.1 }}
                                className="px-2 py-1 bg-lime/20 text-lime text-xs rounded-full border border-lime/30"
                              >
                                {improvement}
                              </motion.span>
                            ))}
                          </div>
                        </div>
                        {iteration >= index && (
                          <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            className="text-green-400"
                          >
                            ✓
                          </motion.div>
                        )}
                      </motion.div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
};

export default LiveRoutingDemo;