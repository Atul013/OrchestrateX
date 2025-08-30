import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, LineChart, Line } from 'recharts';
import { models } from '../config/models';

const ComparisonChart: React.FC<{ activeTab: string }> = ({ activeTab }) => {
  const chartData = models.map(model => ({
    name: model.name,
    reasoning: model.capabilities.reasoning,
    coding: model.capabilities.coding,
    creativity: model.capabilities.creativity,
    factuality: model.capabilities.factuality,
    safety: model.capabilities.safety,
    latencyP50: model.latency.p50,
    latencyP95: model.latency.p95,
    cost: model.cost * 1000, // Convert to per-million tokens for visibility
  }));

  const renderChart = () => {
    switch (activeTab) {
      case 'strengths':
        const radarData = [
          { capability: 'Reasoning', ...Object.fromEntries(models.map(m => [m.name, m.capabilities.reasoning])) },
          { capability: 'Coding', ...Object.fromEntries(models.map(m => [m.name, m.capabilities.coding])) },
          { capability: 'Creativity', ...Object.fromEntries(models.map(m => [m.name, m.capabilities.creativity])) },
          { capability: 'Factuality', ...Object.fromEntries(models.map(m => [m.name, m.capabilities.factuality])) },
          { capability: 'Safety', ...Object.fromEntries(models.map(m => [m.name, m.capabilities.safety])) },
        ];
        
        return (
          <ResponsiveContainer width="100%" height={400}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="rgba(255,255,255,0.2)" />
              <PolarAngleAxis dataKey="capability" className="text-white/70 text-sm" />
              <PolarRadiusAxis domain={[0, 100]} tick={false} />
              <Radar name="GLM-4.5" dataKey="GLM-4.5" stroke="#7A5AF8" fill="#7A5AF8" fillOpacity={0.1} />
              <Radar name="Claude" dataKey="Anthropic Claude" stroke="#3DE5FF" fill="#3DE5FF" fillOpacity={0.1} />
              <Radar name="Gemini" dataKey="Google Gemini" stroke="#FF2EA6" fill="#FF2EA6" fillOpacity={0.1} />
            </RadarChart>
          </ResponsiveContainer>
        );

      case 'latency':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" className="text-white/70 text-sm" />
              <YAxis className="text-white/70 text-sm" />
              <Bar dataKey="latencyP50" fill="#7A5AF8" name="P50" radius={4} />
              <Bar dataKey="latencyP95" fill="#3DE5FF" name="P95" radius={4} />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'cost':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <XAxis dataKey="name" className="text-white/70 text-sm" />
              <YAxis className="text-white/70 text-sm" />
              <Line 
                type="monotone" 
                dataKey="cost" 
                stroke="#B7FF3C" 
                strokeWidth={3}
                dot={{ fill: '#B7FF3C', strokeWidth: 2, r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        );

      default:
        return null;
    }
  };

  return (
    <motion.div
      key={activeTab}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
      className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-6"
    >
      {renderChart()}
    </motion.div>
  );
};

const DynamicComparison: React.FC = () => {
  const [activeTab, setActiveTab] = useState('strengths');

  const tabs = [
    { id: 'strengths', label: 'Strengths', description: 'Capability comparison across key areas' },
    { id: 'latency', label: 'Latency', description: 'Response time performance (P50/P95)' },
    { id: 'cost', label: 'Cost', description: 'Pricing per million tokens' },
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
            Dynamic Comparison
          </h2>
          <p className="text-xl text-white/80 max-w-3xl mx-auto leading-relaxed">
            Interactive performance metrics to help you understand each model's strengths and trade-offs
          </p>
        </motion.div>

        {/* Tab Navigation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="flex flex-col sm:flex-row justify-center mb-12"
        >
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-2 inline-flex">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-3 rounded-xl font-semibold transition-all duration-300 ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-primary to-cyan text-white shadow-lg'
                    : 'text-white/70 hover:text-white hover:bg-white/10'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </motion.div>

        {/* Tab Description */}
        <motion.div
          key={`desc-${activeTab}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
          className="text-center mb-8"
        >
          <p className="text-white/70">
            {tabs.find(tab => tab.id === activeTab)?.description}
          </p>
        </motion.div>

        {/* Chart Content */}
        <AnimatePresence mode="wait">
          <ComparisonChart activeTab={activeTab} />
        </AnimatePresence>

        {/* Disclaimer */}
        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="text-center text-sm text-white/50 mt-8"
        >
          * Data illustrative for demo purposes. Actual performance may vary by provider and plan.
        </motion.p>
      </div>
    </section>
  );
};

export default DynamicComparison;