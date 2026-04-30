import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Leaf, ArrowRight, CloudSun, Map, Bot, ShieldCheck } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.5, delay }}
    whileHover={{ y: -5, scale: 1.02 }}
    className="bg-white/70 backdrop-blur-xl border border-white/60 p-8 rounded-[24px] shadow-lg shadow-slate-200/50"
  >
    <div className="w-14 h-14 bg-gradient-to-br from-emerald-500 to-green-600 rounded-2xl flex items-center justify-center shadow-md shadow-emerald-500/20 mb-6">
      <Icon className="w-7 h-7 text-white" />
    </div>
    <h3 className="text-xl font-bold text-slate-900 mb-3">{title}</h3>
    <p className="text-slate-600 leading-relaxed text-[15px]">{description}</p>
  </motion.div>
);

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50 overflow-hidden font-sans">
      {/* Navbar */}
      <nav className="absolute top-0 w-full z-50 px-6 py-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center shadow-lg shadow-emerald-500/30">
            <Leaf size={20} className="text-white" />
          </div>
          <span className="text-xl font-bold text-slate-900 tracking-tight">AgriX</span>
        </div>
        <div className="flex items-center gap-4">
          <Link to="/login" className="text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors">Sign In</Link>
          <Link to="/login" className="btn-primary py-2.5 px-5 text-sm rounded-xl">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 px-6">
        {/* Background elements */}
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[60%] bg-emerald-200/40 blur-[120px] rounded-full mix-blend-multiply pointer-events-none" />
        <div className="absolute top-[10%] right-[-10%] w-[40%] h-[50%] bg-blue-200/40 blur-[120px] rounded-full mix-blend-multiply pointer-events-none" />

        <div className="max-w-5xl mx-auto text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/80 backdrop-blur-md border border-emerald-100 shadow-sm mb-8">
              <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-xs font-semibold text-emerald-700 uppercase tracking-wider">AgriX OS 2.0 is live</span>
            </div>
          </motion.div>

          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1, ease: "easeOut" }}
            className="text-5xl md:text-7xl font-extrabold text-slate-900 tracking-tight leading-[1.1] mb-6"
          >
            Next-Generation AI for <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-green-600">Precision Agriculture.</span>
          </motion.h1>

          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
            className="text-xl md:text-2xl text-slate-500 font-medium max-w-3xl mx-auto mb-10 leading-relaxed"
          >
            Turn satellite data, weather patterns, and machine learning into actionable, farm-level decisions. Manage everything in one stunning dashboard.
          </motion.p>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3, ease: "easeOut" }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link to="/login" className="btn-primary w-full sm:w-auto text-lg px-8 py-4 rounded-2xl group">
              Start Free Trial
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </Link>
            <button className="btn-secondary w-full sm:w-auto text-lg px-8 py-4 rounded-2xl border-white hover:border-slate-200">
              Request Demo
            </button>
          </motion.div>
        </div>

        {/* Dashboard Preview Image/Mockup */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4, ease: "easeOut" }}
          className="mt-20 max-w-6xl mx-auto relative"
        >
          <div className="absolute inset-0 bg-gradient-to-t from-slate-50 to-transparent z-10 h-full pointer-events-none" />
          <div className="bg-white p-2 rounded-[32px] shadow-2xl shadow-slate-300/50 border border-slate-200/50">
            <div className="bg-slate-100 h-[400px] md:h-[600px] w-full rounded-[24px] overflow-hidden relative flex items-center justify-center">
              {/* Abstract representation of dashboard */}
              <div className="absolute inset-0 opacity-20" style={{ backgroundImage: 'radial-gradient(#10b981 1px, transparent 1px)', backgroundSize: '30px 30px' }}></div>
              <div className="z-10 text-center">
                <ShieldCheck className="w-16 h-16 text-emerald-500 mx-auto mb-4 opacity-50" />
                <p className="text-slate-400 font-medium text-lg">Platform Interface Preview</p>
              </div>
            </div>
          </div>
        </motion.div>
      </main>

      {/* Features Section */}
      <section className="py-24 px-6 bg-white relative z-20 border-t border-slate-100">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold text-slate-900 tracking-tight mb-4">Intelligent infrastructure.</h2>
            <p className="text-lg text-slate-500 font-medium">Everything you need to optimize operations and reduce risk.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={Map}
              title="Geospatial Intelligence"
              description="Monitor NDVI health indices and productivity heatmaps with sub-meter resolution."
              delay={0.1}
            />
            <FeatureCard 
              icon={CloudSun}
              title="Climate Hub Forecast"
              description="Prophet-driven weather models predict operational risks before they happen."
              delay={0.2}
            />
            <FeatureCard 
              icon={Bot}
              title="RAG AI Assistant"
              description="Get agronomic advice instantly via conversational AI trained on scientific literature."
              delay={0.3}
            />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-white py-12 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between">
          <div className="flex items-center gap-3 mb-4 md:mb-0">
            <Leaf size={24} className="text-emerald-500" />
            <span className="text-xl font-bold tracking-tight">AgriX</span>
          </div>
          <div className="flex gap-6 text-sm font-medium text-slate-400">
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
            <a href="#" className="hover:text-white transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
