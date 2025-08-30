import React from 'react';
import zhipuLogo from '../../logos/zhipu.png';
import openaiLogo from '../../logos/openai.png';
import metaLogo from '../../logos/meta.jpeg';
import moonshotLogo from '../../logos/moonshot.png';
import alibabaLogo from '../../logos/alibaba.jpeg';
import tngtechLogo from '../../logos/tngtech.png';
import { motion } from 'framer-motion';
import { Github, BookOpen, Activity, Shield, FileText, Users, ExternalLink } from 'lucide-react';

const Footer: React.FC = () => {
  const footerLinks = {
    Product: [
      { name: 'Documentation', href: 'https://github.com/Atul013/OrchestrateX/blob/main/README.md', icon: BookOpen },
  { name: 'API Reference', href: 'https://github.com/Atul013/OrchestrateX/blob/main/docs/API_REFERENCE.md', icon: FileText },
  { name: 'GitHub', href: 'https://github.com/Atul013/OrchestrateX', icon: Github },
    ],
    Company: [
  { name: 'About', href: 'https://github.com/Atul013/OrchestrateX/blob/main/TEAM_RESPONSIBILITIES.md', icon: Users },
  { name: 'Privacy Policy', href: 'https://github.com/Atul013/OrchestrateX/blob/main/PRIVACY_POLICY.md', icon: Shield },
  { name: 'Terms of Service', href: 'https://github.com/Atul013/OrchestrateX/blob/main/TERMS_OF_SERVICE.md', icon: FileText },
  { name: 'Contact', href: 'https://github.com/Atul013/OrchestrateX/blob/main/CONTACT.md', icon: Users },
    ],
  };

  const modelProviders = [
    { name: 'OpenAI', logo: openaiLogo, url: 'https://openai.com/' },
    { name: 'Zhipu AI', logo: zhipuLogo, url: 'https://bigmodel.cn/' },
    { name: 'Meta', logo: metaLogo, url: 'https://ai.meta.com/meta-ai/' },
    { name: 'Moonshot', logo: moonshotLogo, url: 'https://www.moonshot-ai.com/' },
    { name: 'TNG Tech', logo: tngtechLogo, url: 'https://www.tngtech.com/' },
    { name: 'Alibaba', logo: alibabaLogo, url: 'https://www.alibabacloud.com/en/solutions/ai/data-intelligence?_p_lc=1' },
  ];

  return (
    <footer className="bg-dark border-t border-white/10">
      <div className="container mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          {/* Brand Section */}
          <div className="md:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h3 className="text-3xl font-display font-bold bg-gradient-to-r from-primary via-cyan to-magenta bg-clip-text text-transparent mb-4">
                OrchestrateX
              </h3>
              <p className="text-white/80 mb-6 leading-relaxed max-w-md">
                OrchestrateX uses multiple AI models in harmony — selecting the best, inviting critiques, and delivering refined answers.
              </p>
              <div className="flex gap-4">
                <motion.a
                  href="https://github.com/Atul013/OrchestrateX"
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  className="w-10 h-10 bg-white/10 backdrop-blur-sm rounded-lg flex items-center justify-center text-white/70 hover:text-white hover:bg-white/20 transition-colors border border-white/20"
                >
                  <Github className="w-5 h-5" />
                </motion.a>
                <motion.a
                  href="https://github.com/Atul013/OrchestrateX/blob/main/README.md"
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  className="w-10 h-10 bg-white/10 backdrop-blur-sm rounded-lg flex items-center justify-center text-white/70 hover:text-white hover:bg-white/20 transition-colors border border-white/20"
                >
                  <BookOpen className="w-5 h-5" />
                </motion.a>
                <motion.a
                  href="#"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  className="w-10 h-10 bg-white/10 backdrop-blur-sm rounded-lg flex items-center justify-center text-white/70 hover:text-white hover:bg-white/20 transition-colors border border-white/20"
                >
                  <Activity className="w-5 h-5" />
                </motion.a>
              </div>
            </motion.div>
          </div>

          {/* Links Sections */}
          {Object.entries(footerLinks).map(([category, links], categoryIndex) => (
            <div key={category}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: categoryIndex * 0.1 }}
              >
                <h4 className="text-lg font-semibold text-white mb-4">{category}</h4>
                <ul className="space-y-3">
                  {links.map((link, index) => {
                    const IconComponent = link.icon;
                    return (
                      <li key={index}>
                        <motion.a
                          href={link.href}
                          whileHover={{ x: 4 }}
                          className="flex items-center gap-2 text-white/70 hover:text-white transition-colors group"
                        >
                          <IconComponent className="w-4 h-4 group-hover:text-cyan" />
                          {link.name}
                          <ExternalLink className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                        </motion.a>
                      </li>
                    );
                  })}
                </ul>
              </motion.div>
            </div>
          ))}
        </div>

        {/* Model Providers Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="mt-16 pt-8 border-t border-white/10"
        >
          <h4 className="text-lg font-semibold text-white mb-6 text-center">
            Trusted Model Providers
          </h4>
          <div className="flex flex-wrap justify-center items-center gap-8">
            {modelProviders.map((provider, index) => (
              <motion.a
                key={index}
                href={provider.url}
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.1 }}
                className="flex items-center gap-3 px-4 py-2 bg-white/5 rounded-lg border border-white/10 hover:border-white/20 transition-colors group cursor-pointer"
              >
                <span className="w-8 h-8 flex items-center justify-center filter grayscale group-hover:grayscale-0 transition-all">
                  <img src={provider.logo} alt={provider.name + ' logo'} className="w-8 h-8 object-contain" />
                </span>
                <span className="text-white/60 group-hover:text-white/80 transition-colors font-medium">
                  {provider.name}
                </span>
              </motion.a>
            ))}
          </div>
        </motion.div>

        {/* Bottom Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="mt-16 pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-4"
        >
          <p className="text-white/60 text-center md:text-left">
            © 2025 OrchestrateX. Built for the future of AI collaboration.
          </p>
          <div className="flex items-center gap-6 text-sm text-white/60">
            <span>Made with ❤️ for developers</span>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span>All systems operational</span>
            </div>
          </div>
        </motion.div>
      </div>
    </footer>
  );
};

export default Footer;