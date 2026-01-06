'use client';

import React, { useState, useEffect } from 'react';
import { FileUpload } from '../components/FileUpload';
import { ChatInterface } from '../components/ChatInterface';
import { Sparkles, Github, FileText, ChevronRight } from 'lucide-react';
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

  return (
    <main className="min-h-screen relative overflow-hidden flex flex-col">
      
      {/* Dynamic Background Elements */}
      <div className="fixed inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-gray-900 via-[#0a0f1e] to-black"></div>
      <div className="fixed top-0 left-0 right-0 h-[500px] bg-emerald-500/10 blur-[120px] rounded-full mix-blend-screen pointer-events-none"></div>
      <div className="fixed bottom-0 right-0 w-[500px] h-[500px] bg-blue-600/10 blur-[100px] rounded-full mix-blend-screen pointer-events-none"></div>

      {/* Navbar */}
      <header className="absolute top-0 w-full z-50 border-b border-white/5 bg-transparent">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 group cursor-pointer">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-blue-600 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-gray-200 to-gray-400 tracking-tight">
              Readify
            </span>
          </div>
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-400">
            <a href="#" className="hover:text-white transition-colors flex items-center gap-2">
              <FileText size={16} /> Docs
            </a>
            <a href="#" className="hover:text-white transition-colors flex items-center gap-2">
              <Github size={16} /> Source
            </a>
            <div className="w-[1px] h-4 bg-white/10"></div>
            <span className="text-xs font-mono px-2 py-1 rounded bg-white/5 border border-white/5 text-emerald-400/80">
              v1.0 Beta
            </span>
          </nav>
        </div>
      </header>

      {/* Content */}
      <div className="flex-1 flex flex-col pt-24 pb-10 px-6 max-w-7xl mx-auto w-full">
        
        {/* State 1: Upload / Hero */}
        {!hasUploaded && (
          <div className="relative z-10 w-full max-w-5xl flex flex-col items-center gap-12 animate-fade-in">
             <div className="text-center space-y-6">
               <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/10 bg-white/5 backdrop-blur-md">
                 <Sparkles size={14} className="text-emerald-400" />
                 <span className="text-xs font-medium text-gray-300">Powered by Gemini 2.5 Flash</span>
               </div>
               
               <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white">
                 Chat with your <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">Knowledge</span>
               </h1>
               
               <p className="text-lg text-gray-400 max-w-2xl mx-auto leading-relaxed">
                 Upload research papers, contracts, or technical documentation. 
                 Get instant answers with precise citations.
               </p>
             </div>

             <FileUpload 
                onUploadComplete={handleUploadComplete} 
                files={files}
                onFilesChange={handleFilesChange}
                sessionId={sessionId}
             />
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
               />
           </div>
        )}

      </div>
      
    </main>
  );
}
