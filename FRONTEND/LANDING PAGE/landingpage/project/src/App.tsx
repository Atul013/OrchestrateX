import React from 'react';
import Hero from './components/Hero';
import HowItWorks from './components/HowItWorks';
import ModelsShowcase from './components/ModelsShowcase';
import DynamicComparison from './components/DynamicComparison';
import UseCases from './components/UseCases';
import TrustAndObservability from './components/TrustAndObservability';
import CTA from './components/CTA';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-dark font-body">
      <Hero />
      <HowItWorks />
      <ModelsShowcase />
      <DynamicComparison />
      <UseCases />
      <TrustAndObservability />
      <CTA />
      <Footer />
    </div>
  );
}

export default App;