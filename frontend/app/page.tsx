'use client';

import React, { useState, useEffect } from 'react';
import { FileUpload } from '../components/FileUpload';
import { ChatInterface } from '../components/ChatInterface';
import { Sparkles, Github, FileText, ChevronRight, Twitter } from 'lucide-react';
import { resetSession } from '../lib/api';

export default function Home() {
  const [hasUploaded, setHasUploaded] = useState(false);
  const [files, setFiles] = useState<string[]>([]);
  // Use a simple random ID for the session. In a real app, use UUID.
  const [sessionId, setSessionId] = useState<string>('');

  useEffect(() => {
    // Generate session ID on mount
    setSessionId(Math.random().toString(36).substring(2, 15));
  }, []);

  const handleUploadComplete = () => {
    setTimeout(() => {
      setHasUploaded(true);
    }, 1500);
  };

  const handleFilesChange = (newFiles: string[]) => {
    setFiles(newFiles);
    // If user removes all files, go back to home
    if (newFiles.length === 0 && hasUploaded) {
        setHasUploaded(false);
    }
  };

  // Browser Refresh Protection
  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (hasUploaded) {
        e.preventDefault();
        e.returnValue = "This conversation will be lost. Are you sure you want to leave?";
        return e.returnValue;
      }
    };
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [hasUploaded]);

  return (
    <main className="min-h-screen relative flex flex-col">
      
      {/* Dynamic Background Elements */}
      <div className="fixed inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-gray-900 via-[#0a0f1e] to-black"></div>
      <div className="fixed top-0 left-0 right-0 h-[500px] bg-emerald-500/10 blur-[120px] rounded-full mix-blend-screen pointer-events-none"></div>
      <div className="fixed bottom-0 right-0 w-[500px] h-[500px] bg-blue-600/10 blur-[100px] rounded-full mix-blend-screen pointer-events-none"></div>

      {/* Navbar - Only verify visible on Landing Page */}
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

      {/* Content */}
      <div className="flex-1 flex flex-col justify-center items-center pt-0 pb-10 px-6 max-w-7xl mx-auto w-full min-h-screen">
        
        {/* State 1: Upload / Hero */}
        {!hasUploaded && (
          <div className="relative z-10 w-full max-w-4xl flex flex-col items-center gap-10 animate-fade-in -mt-20 scale-90 origin-center">
             <div className="text-center space-y-8">
               <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 backdrop-blur-md shadow-lg">
                 <Sparkles size={16} className="text-blue-400" />
                 <span className="text-sm font-medium text-gray-200">Advanced RAG Pipeline</span>
               </div>
               
                <h1 className="text-3xl md:text-5xl lg:text-6xl font-bold tracking-tight text-white leading-tight whitespace-nowrap">
                  Readify : <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">Context + Intelligence Quotient</span>
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
          </div>
        )}

        {/* State 2: Chat Interface (Full Screen) */}
        {hasUploaded && (
           <div className="absolute inset-0 z-20 bg-[#030712] flex flex-col animate-fade-in">
               <ChatInterface 
                  files={files} 
                  sessionId={sessionId} 
                  onReset={() => {
                      resetSession(sessionId).then(() => {
                           window.location.reload(); 
                      });
                  }}
                  onFilesChange={handleFilesChange}
               />
           </div>
        )}

      </div>
      
      {/* Footer */}
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
