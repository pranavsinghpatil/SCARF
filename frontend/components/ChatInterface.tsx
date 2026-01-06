'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, User, BookOpen, Copy, Check, RotateCcw, PlusCircle, Menu, X, Sidebar, BookX, Github } from 'lucide-react';
import { queryDocument, resetSession } from '../lib/api';
import { cn } from '../lib/utils';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: string[];
  timestamp: Date;
}

import { FileUpload } from './FileUpload';

interface ChatInterfaceProps {
  files: string[];
  sessionId: string;
  onReset: () => void;
  onFilesChange: (files: string[]) => void;
}

export function ChatInterface({ files, sessionId, onReset, onFilesChange }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'ve analyzed your document. Ask me anything about it.',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [showSidebar, setShowSidebar] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
   

  
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [input]);

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
    setIsLoading(true);

    try {
      const result = await queryDocument(userMessage.content, files, sessionId);
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: result.answer,
        citations: result.citations,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I encountered an issue connecting to the knowledge base: ${(error as any).response?.data?.detail || (error as any).message || "Unknown error"}. Please try again.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="flex h-full w-full bg-[#212121] text-gray-100 font-sans overflow-hidden">
      
      {/* Sidebar (File/Info) */}
      <div 
        className={cn(
             "bg-[#171717] flex flex-col border-r border-white/5 flex-shrink-0 transition-all duration-300 ease-in-out",
             showSidebar ? "w-[260px] translate-x-0" : "w-0 -translate-x-full opacity-0 overflow-hidden border-0"
        )}
      >
          <div className="p-4 flex items-center justify-between border-b border-white/5">
             <div className="flex items-center gap-2 text-white/90 font-medium overflow-hidden">
                <Sparkles size={18} className="shrink-0 text-emerald-400" />
                <span className="truncate font-bold tracking-tight">Readify</span>
             </div>
          </div>

          <div className="flex-1 overflow-y-auto px-2 py-4">
              {/* Integrated File Upload & List (Compact Mode) */}
              <div className="px-2">
                 <FileUpload 
                    onUploadComplete={() => {}} 
                    files={files} 
                    onFilesChange={onFilesChange} 
                    sessionId={sessionId} 
                    isCompact={true} 
                 />
              </div>
          </div>

          {/* Bottom Sidebar Section */}
          <div className="p-3 border-t border-white/5 bg-black/20 space-y-3">
              <button 
                onClick={() => { if(confirm("This conversation will be lost. Do you want to start a new chat?")) onReset(); }} 
                className="w-full flex items-center justify-center gap-2 text-xs font-medium text-gray-300 hover:text-emerald-400 bg-white/5 hover:bg-emerald-500/10 p-2 rounded-lg transition-all border border-white/5 hover:border-emerald-500/20 shadow-lg"
              >
                 <PlusCircle size={14} /> 
                 <span>New Chat</span>
              </button>

              <div className="px-2 py-2 text-[10px] text-gray-500 bg-black/40 rounded border border-white/5 space-y-1">
                <div className="flex justify-between">
                   <span>Engine</span>
                   <span className="text-gray-300">Readify AI</span>
                </div>
                <div className="flex justify-between">
                   <span>ID</span>
                   <span className="font-mono text-gray-400">{sessionId.slice(0,6)}...</span>
                </div>
             </div>
          </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative h-full">
        {/* Header - Minimal */}
        <header className="absolute top-0 w-full h-14 flex items-center justify-between px-4 z-10">
           {/* Sidebar Toggle */}
           <button 
             onClick={() => setShowSidebar(!showSidebar)}
             className="p-2 rounded-lg hover:bg-white/5 text-gray-400 transition-colors"
           >
              {showSidebar ? <Sidebar size={20} /> : <Menu size={20} />}
           </button>

           <div className="bg-[#212121]/95 backdrop-blur-xl px-4 py-1.5 rounded-full border border-white/5 text-sm text-gray-400 font-medium shadow-sm pointer-events-auto">
              Readify AI
           </div>
           
           <div className="w-10"></div> {/* Spacer for center alignment balance */}
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto scroll-smooth">
            <div className="max-w-3xl mx-auto px-4 pt-24 pb-48 space-y-8">
            {messages.map((msg) => (
             <motion.div
               key={msg.id}
               initial={{ opacity: 0, y: 5 }}
               animate={{ opacity: 1, y: 0 }}
               className={cn(
                 "flex gap-4",
                 msg.role === 'user' ? "flex-row-reverse" : "flex-row"
               )}
             >
                {/* Avatars */}
               <div className={cn(
                   "w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-1",
                   msg.role === 'assistant' ? "bg-green-500/10 text-green-400 border border-green-500/20" : "bg-white/10 text-gray-300"
               )}>
                   {msg.role === 'assistant' ? <Sparkles size={14} /> : <User size={14} />}
               </div>

               <div className={cn(
                   "relative max-w-[85%]",
                   msg.role === 'user' 
                     ? "bg-[#2f2f2f] text-white px-5 py-3 rounded-3xl rounded-tr-sm" 
                     : "text-gray-100 py-1"
                 )}
               >
                 <div className="prose prose-invert prose-base max-w-none leading-7 text-gray-200">
                    {msg.role === 'assistant' ? (
                        <ReactMarkdown 
                            remarkPlugins={[remarkGfm]}
                            components={{
                                code: ({node, ...props}) => <code className="bg-black/30 rounded px-1.5 py-0.5 text-sm font-mono text-emerald-300" {...props} />,
                                pre: ({node, ...props}) => <pre className="bg-black/40 p-4 rounded-xl overflow-x-auto my-4 border border-white/5" {...props} />,
                                ul: ({node, ...props}) => <ul className="list-disc pl-5 space-y-1 my-4" {...props} />,
                                ol: ({node, ...props}) => <ol className="list-decimal pl-5 space-y-1 my-4" {...props} />,
                                li: ({node, ...props}) => <li className="pl-1" {...props} />,
                                h1: ({node, ...props}) => <h1 className="text-xl font-bold text-white mt-6 mb-3 border-b border-white/10 pb-2" {...props} />,
                                h2: ({node, ...props}) => <h2 className="text-lg font-bold text-white mt-5 mb-3" {...props} />,
                                h3: ({node, ...props}) => <h3 className="text-base font-bold text-white mt-4 mb-2" {...props} />,
                                blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-emerald-500/50 pl-4 py-1 my-4 italic text-gray-400 bg-white/5 rounded-r-lg" {...props} />,
                                a: ({node, ...props}) => <a className="text-emerald-400 hover:underline" {...props} />,
                            }}
                        >
                            {msg.content}
                        </ReactMarkdown>
                    ) : (
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                    )}
                 </div>

                 {msg.citations && msg.citations.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-white/10">
                        <p className="text-xs font-semibold text-gray-500 mb-2">Sources:</p>
                        <div className="flex flex-wrap gap-2">
                            {msg.citations.map((cite, i) => (
                            <span 
                                key={i} 
                                className="text-[11px] bg-[#2f2f2f] text-gray-300 px-2 py-1 rounded border border-white/10"
                            >
                                {cite}
                            </span>
                            ))}
                        </div>
                    </div>
                 )}
               </div>
             </motion.div>
            ))}

            {isLoading && (
               <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-green-500/10 text-green-400 border border-green-500/20 flex items-center justify-center shrink-0">
                        <Sparkles size={14} />
                    </div>
                    <div className="flex items-center gap-1 h-8">
                        <span className="w-2 h-2 bg-gray-500/50 rounded-full animate-pulse"></span>
                    </div>
               </motion.div>
            )}
            <div ref={messagesEndRef} />
            </div>
        </div>

        {/* Input Area - Bottom Fixed */}
        <div className="p-4 bg-[#212121] absolute bottom-0 w-full">
            <div className="max-w-3xl mx-auto relative">
                <div className="relative group rounded-3xl bg-[#2f2f2f] border border-white/5 focus-within:border-gray-600 transition-all shadow-lg overflow-hidden">
                    <textarea
                        ref={textareaRef}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Message Readify..."
                        rows={1}
                        className="w-full bg-transparent text-white placeholder-gray-400 text-base px-5 py-4 pr-12 focus:outline-none resize-none max-h-[200px] scrollbar-hide"
                        disabled={isLoading}
                    />
                    <button
                        onClick={() => handleSubmit()}
                        disabled={!input.trim() || isLoading}
                        className={cn(
                            "absolute right-2 bottom-2 p-2 rounded-full transition-all flex items-center justify-center",
                            input.trim() 
                            ? "bg-white text-black hover:bg-gray-200" 
                            : "bg-[#424242] text-gray-500 cursor-not-allowed"
                        )}
                    >
                        <Send size={16} />
                    </button>
                </div>
                <div className="text-center mt-2 pb-2 space-y-2">
                    <div className="flex justify-center items-center gap-4 text-[10px] font-mono">
                        <div className="text-gray-600">
                            Created by <a href="https://prnav.me" target="_blank" className="text-gray-400 hover:text-emerald-400 transition-colors">Pranav</a>
                        </div>
                        <span className="text-gray-800">•</span>
                        <a href="https://twitter.com/pranavenv" target="_blank" className="text-gray-600 hover:text-white transition-colors">
                            <svg viewBox="0 0 24 24" aria-hidden="true" className="w-4 h-4 fill-current">
                                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path>
                            </svg>
                        </a>
                        <span className="text-gray-800">•</span>
                        <a href="https://github.com/pranavsinghpatil/Readify" target="_blank" className="text-gray-600 hover:text-emerald-400 transition-colors flex items-center gap-1">
                             <Github size={10} /> Source Code
                        </a>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
}
