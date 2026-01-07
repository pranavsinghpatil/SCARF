'use client';

import React, { useState, useEffect } from 'react';
import { FileUpload } from '../components/FileUpload';
import { ChatInterface } from '../components/ChatInterface';
import { Sparkles, Github, FileText, ChevronRight, Twitter } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { resetSession } from '../lib/api';

export default function Home() {
  const [hasUploaded, setHasUploaded] = useState(false);
  const [files, setFiles] = useState<string[]>([]);
  const [sessionId, setSessionId] = useState<string>('');

  useEffect(() => {
    setSessionId(Math.random().toString(36).substring(2, 15));
  }, []);

  const handleUploadComplete = () => {
    setHasUploaded(true);
  };

  const handleFilesChange = (newFiles: string[]) => {
    setFiles(newFiles);
    if (newFiles.length === 0 && hasUploaded) {
        setHasUploaded(false);
    }
  };

  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (hasUploaded) {
        e.preventDefault();
        e.returnValue = "This conversation will be lost. Are you sure you want to leave?";
        return e.returnValue;
      }
    };

    const handleUnload = () => {
      if (hasUploaded && sessionId) {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        fetch(`${API_URL}/api/reset/${sessionId}`, {
          method: 'DELETE',
          keepalive: true
        });
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    window.addEventListener('unload', handleUnload);
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      window.removeEventListener('unload', handleUnload);
    };
  }, [hasUploaded, sessionId]);

  return (
    <main className="min-h-screen relative flex flex-col">
      <div className="fixed inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-gray-900 via-[#0a0f1e] to-black"></div>
      <div className="fixed top-0 left-0 right-0 h-[500px] bg-emerald-500/10 blur-[120px] rounded-full mix-blend-screen pointer-events-none"></div>
      <div className="fixed bottom-0 right-0 w-[500px] h-[500px] bg-blue-600/10 blur-[100px] rounded-full mix-blend-screen pointer-events-none"></div>

      {!hasUploaded && (
        <header className="absolute top-0 w-full z-50 bg-transparent">
          <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2 group cursor-pointer">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-blue-600 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-gray-200 to-gray-400 tracking-tight">
                Readify
              </span>
            </div>
            <nav className="flex items-center gap-4">
              <a 
                href="https://github.com/pranavsinghpatil/Readify" 
                target="_blank"
                className="flex items-center gap-2 text-sm font-medium text-gray-300 hover:text-emerald-400 transition-colors bg-white/5 hover:bg-emerald-500/10 px-4 py-2 rounded-full border border-white/5 hover:border-emerald-500/20 shadow-lg"
              >
                <Github size={16} />
                <span>Source Code</span>
              </a>
            </nav>
          </div>
        </header>
      )}

      <div className="flex-1 flex flex-col justify-center items-center pt-0 pb-10 px-6 max-w-7xl mx-auto w-full min-h-screen">
        <AnimatePresence mode="wait">
          {!hasUploaded ? (
            <motion.div 
              key="hero"
              initial={{ opacity: 0, scale: 0.95, filter: 'blur(10px)' }}
              animate={{ opacity: 1, scale: 0.9, filter: 'blur(0px)' }}
              exit={{ opacity: 0, scale: 1.1, filter: 'blur(20px)' }}
              transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
              className="relative z-10 w-full max-w-4xl flex flex-col items-center gap-16 origin-center -mt-24"
            >
              <div className="text-center space-y-12">
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 backdrop-blur-md shadow-lg">
                  <Sparkles size={16} className="text-blue-400" />
                  <span className="text-sm font-medium text-gray-200">Advanced RAG Pipeline</span>
                </div>
                
                <h1 className="text-3xl md:text-5xl lg:text-6xl font-bold tracking-tight text-white leading-tight whitespace-nowrap">
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">Readify :</span> Context + Intelligence 
                </h1>
                
                <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
                  Interact with your documents intelligently. Upload PDFs, Word docs, or Text files and get precise, context-aware answers instantly.
                </p>
              </div>

              <div className="w-full">
                <FileUpload 
                    onUploadComplete={handleUploadComplete} 
                    files={files}
                    onFilesChange={handleFilesChange}
                    sessionId={sessionId}
                />
              </div>
            </motion.div>
          ) : (
            <motion.div 
              key="chat"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="absolute inset-0 z-20 bg-[#030712] flex flex-col"
            >
                <ChatInterface 
                   files={files} 
                   sessionId={sessionId} 
                   onReset={() => {
                       resetSession(sessionId).then(() => {
                            setTimeout(() => window.location.reload(), 500); 
                       });
                   }}
                   onFilesChange={handleFilesChange}
                />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      
      {!hasUploaded && (
        <footer className="absolute bottom-6 w-full text-center">
            <div className="flex items-center justify-center gap-4 text-sm font-medium">
                <div className="text-gray-500">
                    Created by <a href="https://prnav.me" target="_blank" className="text-white hover:text-emerald-400 transition-colors">Pranav</a>
                </div>
                <span className="text-gray-700">•</span>
                <a href="https://twitter.com/pranavenv" target="_blank" className="text-gray-500 hover:text-white transition-colors">
                    <svg viewBox="0 0 24 24" aria-hidden="true" className="w-6 h-6 fill-current">
                        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path>
                    </svg>
                </a>
            </div>
        </footer>
      )}
    </main>
  );
}
