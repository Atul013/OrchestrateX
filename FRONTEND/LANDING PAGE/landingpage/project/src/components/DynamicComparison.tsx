import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, LineChart, Line, Tooltip, Legend, CartesianGrid } from 'recharts';
import { models } from '../config/models';

const ComparisonChart: React.FC<{ activeTab: string }> = ({ activeTab }) => {
  const chartData = models.map(model => ({
    name: model.name.replace(' ', '\n'), // Line break for better display
    reasoning: model.capabilities.reasoning,
    coding: model.capabilities.coding,
    creativity: model.capabilities.creativity,
    factuality: model.capabilities.factuality,
    safety: model.capabilities.safety,
    latencyP50: model.latency.p50,
    latencyP95: model.latency.p95,
    cost: model.cost, // Already in per-million tokens format
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
          <ResponsiveContainer width="100%" height={500}>
            <RadarChart data={radarData} margin={{ top: 40, right: 80, bottom: 40, left: 80 }}>
              <PolarGrid stroke="rgba(255,255,255,0.3)" gridType="polygon" />
              <PolarAngleAxis 
                dataKey="capability" 
                tick={{ fill: 'rgba(255,255,255,0.8)', fontSize: 14, fontWeight: 500 }}
                className="text-white/80"
              />
              <PolarRadiusAxis 
                domain={[0, 100]} 
                tick={{ fill: 'rgba(255,255,255,0.6)', fontSize: 12 }}
                tickCount={6}
                angle={0}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'rgba(17, 24, 39, 0.95)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: '8px',
                  color: 'white'
                }}
              />
              <Legend 
                wrapperStyle={{ color: 'rgba(255, 255, 255, 0.8)' }}
              />
              <Radar name="GLM4.5" dataKey="GLM4.5" stroke="#7A5AF8" fill="#7A5AF8" fillOpacity={0.15} strokeWidth={2} />
              <Radar name="GPT-OSS" dataKey="GPT‑OSS" stroke="#10B981" fill="#10B981" fillOpacity={0.15} strokeWidth={2} />
              <Radar name="Llama 4" dataKey="Llama 4 Maverick" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.15} strokeWidth={2} />
              <Radar name="Kimi" dataKey="MoonshotAI Kimi" stroke="#3DE5FF" fill="#3DE5FF" fillOpacity={0.15} strokeWidth={2} />
              <Radar name="Qwen3" dataKey="Qwen3 Coder" stroke="#FF2EA6" fill="#FF2EA6" fillOpacity={0.15} strokeWidth={2} />
              <Radar name="DeepSeek" dataKey="TNG DeepSeek R1T2 Chimera" stroke="#B7FF3C" fill="#B7FF3C" fillOpacity={0.15} strokeWidth={2} />
            </RadarChart>
          </ResponsiveContainer>
        );

      case 'latency':
        return (
          <ResponsiveContainer width="100%" height={450}>
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey="name" 
                tick={{ fill: 'rgba(255,255,255,0.8)', fontSize: 12 }}
                axisLine={{ stroke: 'rgba(255,255,255,0.3)' }}
                tickLine={{ stroke: 'rgba(255,255,255,0.3)' }}
                interval={0}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                tick={{ fill: 'rgba(255,255,255,0.8)', fontSize: 12 }}
                axisLine={{ stroke: 'rgba(255,255,255,0.3)' }}
                tickLine={{ stroke: 'rgba(255,255,255,0.3)' }}
                label={{ value: 'Latency (ms)', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fill: 'rgba(255,255,255,0.8)' } }}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'rgba(17, 24, 39, 0.95)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: '8px',
                  color: 'white'
                }}
                formatter={(value: number, name: string) => [`${value}ms`, name]}
              />
              <Legend 
                wrapperStyle={{ color: 'rgba(255, 255, 255, 0.8)' }}
              />
              <Bar dataKey="latencyP50" fill="#7A5AF8" name="P50 (median)" radius={[4, 4, 0, 0]} />
              <Bar dataKey="latencyP95" fill="#3DE5FF" name="P95 (95th percentile)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'cost':
        return (
          <ResponsiveContainer width="100%" height={450}>
            <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey="name" 
                tick={{ fill: 'rgba(255,255,255,0.8)', fontSize: 12 }}
                axisLine={{ stroke: 'rgba(255,255,255,0.3)' }}
                tickLine={{ stroke: 'rgba(255,255,255,0.3)' }}
                interval={0}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                tick={{ fill: 'rgba(255,255,255,0.8)', fontSize: 12 }}
                axisLine={{ stroke: 'rgba(255,255,255,0.3)' }}
                tickLine={{ stroke: 'rgba(255,255,255,0.3)' }}
                label={{ value: 'Cost ($USD per 1M tokens)', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fill: 'rgba(255,255,255,0.8)' } }}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'rgba(17, 24, 39, 0.95)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: '8px',
                  color: 'white'
                }}
                formatter={(value: number) => [`$${value.toFixed(2)}`, 'Cost per 1M tokens']}
              />
              <Line 
                type="monotone" 
                dataKey="cost" 
                stroke="#B7FF3C" 
                strokeWidth={4}
                dot={{ fill: '#B7FF3C', strokeWidth: 3, r: 8, stroke: '#1F2937' }}
                activeDot={{ r: 10, stroke: '#B7FF3C', strokeWidth: 3, fill: '#1F2937' }}
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
    { id: 'strengths', label: 'Strengths', description: 'Real-time capability scores: reasoning, coding, creativity, factuality & safety (Updated Dec 2024)' },
    { id: 'latency', label: 'Latency', description: 'Live response times - P50 median & P95 percentile latency in milliseconds' },
    { id: 'cost', label: 'Cost', description: 'Current pricing per million tokens - Updated with latest API rates' },
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
        <div className="mt-8 text-center">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="flex items-center justify-center gap-2 mb-2"
          >
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-green-400 font-medium">Live Data</span>
          </motion.div>
          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="text-xs text-white/50"
          >
            Real-time data updated December 2024. Performance may vary based on query complexity, provider region, and API tier.
          </motion.p>
        </div>
      </div>
    </section>
  );
};

export default DynamicComparison;