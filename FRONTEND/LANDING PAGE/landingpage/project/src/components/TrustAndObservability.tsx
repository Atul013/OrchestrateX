import React, { useEffect, useState } from 'react';
import { motion, useAnimation, useInView } from 'framer-motion';
import { Shield, Key, FileText, Zap, Database, DollarSign, CheckCircle } from 'lucide-react';

const CounterCard: React.FC<{ 
  icon: React.ReactNode; 
  title: string; 
  value: string; 
  description: string;
  color: string;
  delay: number;
}> = ({ icon, title, value, description, color, delay }) => {
  const [displayValue, setDisplayValue] = useState('0');
  const ref = React.useRef(null);
  const inView = useInView(ref, { once: true });
  const controls = useAnimation();

  useEffect(() => {
    if (inView) {
      controls.start({ opacity: 1, y: 0 });
      
      // Animate counter
      const finalValue = parseInt(value.replace(/[^0-9]/g, ''));
      const increment = finalValue / 50;
      let current = 0;
      
      const timer = setInterval(() => {
        current += increment;
        if (current >= finalValue) {
          setDisplayValue(value);
          clearInterval(timer);
        } else {
          setDisplayValue(Math.floor(current).toLocaleString());
        }
      }, 30);

      return () => clearInterval(timer);
    }
  }, [inView, controls, value]);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={controls}
      transition={{ duration: 0.6, delay }}
      className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-8 hover:bg-white/15 transition-all duration-300 group"
    >
      <div className="flex items-center gap-4 mb-4">
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-white group-hover:scale-110 transition-transform ${color}`}>
          {icon}
        </div>
        <h3 className="text-xl font-display font-bold text-white">{title}</h3>
      </div>
      
      <div className="mb-4">
        <div className="text-3xl font-bold text-white mb-2">{displayValue}</div>
        <p className="text-white/70 leading-relaxed">{description}</p>
      </div>

      <div className="flex items-center gap-2 text-sm text-white/60">
        <CheckCircle className="w-4 h-4 text-green-400" />
        <span>Active & Monitored</span>
      </div>
    </motion.div>
  );
};

const TrustAndObservability: React.FC = () => {
  const trustFeatures = [
    {
      icon: <Shield className="w-6 h-6" />,
      title: "Rate Limiting",
      value: "10,000",
      description: "Requests per minute protected against abuse and ensuring fair usage across all clients",
      color: "bg-gradient-to-r from-primary to-cyan"
    },
    {
      icon: <Key className="w-6 h-6" />,
      title: "API Security",
      value: "256-bit",
      description: "End-to-end encryption with rotating keys and secure credential management",
      color: "bg-gradient-to-r from-cyan to-magenta"
    },
    {
      icon: <FileText className="w-6 h-6" />,
      title: "Audit Logs",
      value: "24/7",
      description: "Complete request tracing with retention policies and compliance reporting",
      color: "bg-gradient-to-r from-magenta to-primary"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Circuit Breakers",
      value: "99.9%",
      description: "Automatic failover protection preventing cascading failures across models",
      color: "bg-gradient-to-r from-primary to-lime"
    },
    {
      icon: <Database className="w-6 h-6" />,
      title: "Smart Caching",
      value: "85%",
      description: "Intelligent response caching reducing latency and costs for similar queries",
      color: "bg-gradient-to-r from-lime to-cyan"
    },
    {
      icon: <DollarSign className="w-6 h-6" />,
      title: "Cost Governance",
      value: "$0.001",
      description: "Automated budget controls and cost optimization across all model providers",
      color: "bg-gradient-to-r from-cyan to-magenta"
    }
  ];

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
            Trust & Observability
          </h2>
          <p className="text-xl text-white/80 max-w-3xl mx-auto leading-relaxed">
            Enterprise-grade security, monitoring, and governance built into every aspect of the platform
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {trustFeatures.map((feature, index) => (
            <CounterCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              value={feature.value}
              description={feature.description}
              color={feature.color}
              delay={index * 0.1}
            />
          ))}
        </div>

        {/* Compliance Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-8"
        >
          <h3 className="text-2xl font-display font-bold text-white mb-6 text-center">
            Privacy & Compliance
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Data Protection</h4>
              <ul className="space-y-2 text-white/80">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  Zero data retention by default
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  PII detection and anonymization
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  GDPR and CCPA compliant
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  SOC 2 Type II certified
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Monitoring</h4>
              <ul className="space-y-2 text-white/80">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  Real-time performance metrics
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  Custom alerting and notifications
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  Detailed usage analytics
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-400" />
                  24/7 system health monitoring
                </li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default TrustAndObservability;