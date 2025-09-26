import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Zap, Users, TrendingUp } from 'lucide-react';
import { mockMetrics } from '../config/models';

const ParticleField: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    const particles: Array<{
      x: number;
      y: number;
      vx: number;
      vy: number;
      size: number;
      opacity: number;
    }> = [];

    for (let i = 0; i < 50; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 2 + 1,
        opacity: Math.random() * 0.5 + 0.2,
      });
    }

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      particles.forEach((particle, i) => {
        particle.x += particle.vx;
        particle.y += particle.vy;

        if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;

        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(122, 90, 248, ${particle.opacity})`;
        ctx.fill();

        // Draw connections
        particles.slice(i + 1).forEach((otherParticle) => {
          const distance = Math.sqrt(
            Math.pow(particle.x - otherParticle.x, 2) + 
            Math.pow(particle.y - otherParticle.y, 2)
          );
          
          if (distance < 100) {
            ctx.beginPath();
            ctx.moveTo(particle.x, particle.y);
            ctx.lineTo(otherParticle.x, otherParticle.y);
            ctx.strokeStyle = `rgba(61, 229, 255, ${(1 - distance / 100) * 0.2})`;
            ctx.stroke();
          }
        });
      });

      requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 pointer-events-none"
      style={{ zIndex: 1 }}
    />
  );
};

const ModelBadge: React.FC<{ name: string; delay: number }> = ({ name, delay }) => (
  <motion.div
    initial={{ opacity: 0, x: -20 }}
    animate={{ opacity: 1, x: 0 }}
    transition={{ delay, duration: 0.6 }}
    className="px-3 py-1 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium text-white/80 border border-white/20"
  >
    {name}
  </motion.div>
);

const Hero: React.FC = () => {
  const modelNames = ['GLM4.5', 'GPT‑OSS', 'Llama 4 Maverick', 'MoonshotAI Kimi', 'Qwen3 Coder', 'TNG DeepSeek R1T2 Chimera'];

  return (
    <section className="relative min-h-screen bg-gradient-to-br from-dark via-dark to-primary/20 overflow-hidden flex items-center">
      <ParticleField />
      
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center max-w-5xl mx-auto">
          {/* Logo */}
          <motion.div
            className="mb-6 lg:mb-8"
          >
            <motion.h1
              className="text-4xl sm:text-5xl md:text-6xl lg:text-8xl font-display font-bold bg-gradient-to-r from-primary via-cyan to-magenta bg-clip-text text-transparent"
              initial={{ opacity: 1 }}
              animate={{
                y: [0, -8, 2, -4, 0],
                opacity: [1, 0.95, 1, 0.98, 1],
                rotateZ: [0, 0.3, -0.2, 0.1, 0],
                scale: [1, 1.005, 0.998, 1.002, 1],
              }}
              transition={{
                duration: 12,
                ease: [0.4, 0, 0.6, 1],
                repeat: Infinity,
                repeatType: "loop",
              }}
              whileHover={{
                scale: 1.03,
                rotateZ: 1,
                y: -3,
                transition: { 
                  duration: 0.3, 
                  ease: "easeOut",
                  type: "spring",
                  stiffness: 300,
                  damping: 20
                }
              }}
              style={{
                "@media (prefers-reduced-motion: reduce)": {
                  animation: "none",
                  transform: "none"
                }
              }}
            >
              OrchestrateX
            </motion.h1>
          </motion.div>

          {/* Main headline */}
          <h2
            className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-display font-bold text-white mb-4 lg:mb-6 px-2 lg:px-0"
          >
            Multi‑Model AI Orchestration
          </h2>

          {/* Subheadline */}
          <p
            className="text-lg sm:text-xl lg:text-2xl text-white/80 mb-8 lg:mb-12 leading-relaxed px-4 lg:px-0"
          >
            Route each query to the model that excels, then refine responses via cross‑model critiques.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8 lg:mb-16 px-4 lg:px-0">
            <a
              href="https://chat.orchestratex.me/"
              target="_blank"
              rel="noopener noreferrer"
              className="px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-primary to-magenta rounded-full text-white font-semibold text-base sm:text-lg flex items-center justify-center gap-2 hover:opacity-90 transition-opacity min-h-[48px] touch-manipulation"
            >
              Try Demo <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5" />
            </a>
            <button className="px-6 sm:px-8 py-3 sm:py-4 border-2 border-white/30 rounded-full text-white font-semibold text-base sm:text-lg hover:bg-white/10 transition-colors min-h-[48px] touch-manipulation">
              View API
            </button>
          </div>

          {/* Model badges - Mobile: horizontal scroll, Desktop: wrap */}
          <div className="mb-8 lg:mb-12 px-2 lg:px-0">
            {/* Mobile: Horizontal scroll */}
            <div className="lg:hidden overflow-x-auto pb-2">
              <div className="flex gap-3 min-w-max px-2">
                {modelNames.map((model, index) => (
                  <div
                    key={model}
                    className="px-3 py-1 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium text-white/80 border border-white/20 whitespace-nowrap"
                  >
                    {model}
                  </div>
                ))}
              </div>
            </div>
            
            {/* Desktop: Flex wrap */}
            <div className="hidden lg:flex flex-wrap justify-center gap-3">
              {modelNames.map((model, index) => (
                <div
                  key={model}
                  className="px-3 py-1 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium text-white/80 border border-white/20"
                >
                  {model}
                </div>
              ))}
            </div>
          </div>

          {/* Live metrics */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20 p-4 sm:p-6 max-w-4xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6 text-center">
              <div className="flex items-center justify-center gap-3 p-2">
                <Zap className="w-5 h-5 sm:w-6 sm:h-6 text-cyan flex-shrink-0" />
                <div>
                  <div className="text-xl sm:text-2xl font-bold text-white">
                    {mockMetrics.requestsToday.toLocaleString()}
                  </div>
                  <div className="text-xs sm:text-sm text-white/70">Requests routed today</div>
                </div>
              </div>
              <div className="flex items-center justify-center gap-3 p-2">
                <Users className="w-5 h-5 sm:w-6 sm:h-6 text-lime flex-shrink-0" />
                <div>
                  <div className="text-xl sm:text-2xl font-bold text-white">{mockMetrics.avgLatency}ms</div>
                  <div className="text-xs sm:text-sm text-white/70">Average latency</div>
                </div>
              </div>
              <div className="flex items-center justify-center gap-3 p-2">
                <TrendingUp className="w-5 h-5 sm:w-6 sm:h-6 text-magenta flex-shrink-0" />
                <div>
                  <div className="text-xl sm:text-2xl font-bold text-white">{mockMetrics.costSaved}%</div>
                  <div className="text-xs sm:text-sm text-white/70">Cost saved vs single‑model</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;