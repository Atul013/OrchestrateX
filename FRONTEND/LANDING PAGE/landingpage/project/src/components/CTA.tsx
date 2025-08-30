import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, BookOpen, Github, Zap } from 'lucide-react';

const CTA: React.FC = () => {
  return (
    <section className="py-24 bg-gradient-to-b from-dark to-dark/95">
      <div className="container mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="relative max-w-4xl mx-auto"
        >
          {/* Main CTA Card */}
          <div className="relative bg-gradient-to-r from-primary/20 via-cyan/20 to-magenta/20 backdrop-blur-sm rounded-3xl border border-white/20 p-12 text-center overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-gradient-to-r from-primary/10 via-transparent to-magenta/10 animate-pulse-slow"></div>
            
            {/* Content */}
            <div className="relative z-10">
              <motion.h2
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="text-4xl md:text-6xl font-display font-bold text-white mb-6"
              >
                Ready to Orchestrate?
              </motion.h2>
              
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: 0.3 }}
                className="text-xl text-white/80 mb-8 leading-relaxed max-w-2xl mx-auto"
              >
                Start building with OrchestrateX today. Free-tier friendly with no local deployment required.
              </motion.p>
              
              {/* CTA Buttons */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: 0.4 }}
                className="flex flex-col sm:flex-row gap-4 justify-center mb-8"
              >
                <motion.button
                  whileHover={{ scale: 1.05, boxShadow: '0 20px 40px rgba(122, 90, 248, 0.3)' }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-4 bg-gradient-to-r from-primary to-magenta rounded-full text-white font-semibold text-lg flex items-center justify-center gap-2 shadow-lg"
                >
                  <Zap className="w-5 h-5" />
                  Start Free
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
                
                <motion.a
                  href="https://github.com/Atul013/OrchestrateX/blob/main/README.md"
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-4 bg-white/10 backdrop-blur-sm border border-white/30 rounded-full text-white font-semibold text-lg flex items-center justify-center gap-2 hover:bg-white/20 transition-colors"
                >
                  <BookOpen className="w-5 h-5" />
                  See Docs
                </motion.a>
                
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-4 bg-white/10 backdrop-blur-sm border border-white/30 rounded-full text-white font-semibold text-lg flex items-center justify-center gap-2 hover:bg-white/20 transition-colors"
                >
                  <Github className="w-5 h-5" />
                  Request Access
                </motion.button>
              </motion.div>

              {/* Features List */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: 0.5 }}
                className="flex flex-wrap justify-center gap-8 text-white/70"
              >
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-lime rounded-full"></div>
                  <span>Free tier included</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-cyan rounded-full"></div>
                  <span>No setup required</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-magenta rounded-full"></div>
                  <span>Cancel anytime</span>
                </div>
              </motion.div>
            </div>

            {/* Animated Background Elements */}
            <motion.div
              animate={{
                x: [0, 100, 0],
                y: [0, -50, 0],
                rotate: [0, 180, 360],
              }}
              transition={{
                duration: 20,
                repeat: Infinity,
                ease: "linear",
              }}
              className="absolute top-10 left-10 w-20 h-20 bg-gradient-to-r from-primary/20 to-cyan/20 rounded-full blur-xl"
            />
            <motion.div
              animate={{
                x: [0, -80, 0],
                y: [0, 60, 0],
                rotate: [0, -180, -360],
              }}
              transition={{
                duration: 25,
                repeat: Infinity,
                ease: "linear",
              }}
              className="absolute bottom-10 right-10 w-16 h-16 bg-gradient-to-r from-magenta/20 to-lime/20 rounded-full blur-xl"
            />
          </div>
        </motion.div>

        {/* Secondary CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="text-center mt-16"
        >
          <p className="text-white/60 mb-4">
            Join thousands of developers already building with OrchestrateX
          </p>
          <div className="flex justify-center items-center gap-8 text-white/40">
            <div className="text-2xl font-bold">10k+</div>
            <div className="w-px h-8 bg-white/20"></div>
            <div className="text-2xl font-bold">500+</div>
            <div className="w-px h-8 bg-white/20"></div>
            <div className="text-2xl font-bold">50+</div>
          </div>
          <div className="flex justify-center items-center gap-8 text-sm text-white/50 mt-2">
            <span>Active Users</span>
            <span>Companies</span>
            <span>Countries</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default CTA;