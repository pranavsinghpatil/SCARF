'use client';

import React, { useRef, useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Loader2, X } from 'lucide-react';
import { uploadDocument, deleteFile } from '../lib/api';
import { cn } from '../lib/utils';

export function FileUpload({ onUploadComplete, files, onFilesChange, isCompact = false, sessionId }: { 
  onUploadComplete: () => void; 
  files: string[];
  onFilesChange: (files: string[]) => void;
  isCompact?: boolean;
  sessionId: string;
}) {
  const [isDragging, setIsDragging] = useState(false);
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [processingCount, setProcessingCount] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      await processUpload(e.dataTransfer.files);
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      await processUpload(e.target.files);
    }
  };

  const processUpload = async (fileList: FileList) => {
    setStatus('uploading');
    setErrorMessage('');
    setProcessingCount(fileList.length);
    
    try {
      const result = await uploadDocument(fileList, sessionId);
      setStatus('success');
      const updated = Array.from(new Set([...files, ...result.filenames]));
      onFilesChange(updated);
      
      setTimeout(() => {
          onUploadComplete();
          setStatus('idle'); 
      }, 800);
      
    } catch (error: any) {
      setStatus('error');
      setErrorMessage(error.response?.data?.detail || "Upload failed. Please check file format.");
    }
  };

  const removeFile = async (nameToRemove: string) => {
    const updated = files.filter(f => f !== nameToRemove);
    onFilesChange(updated);
    try {
        await deleteFile(nameToRemove, sessionId);
    } catch (e) {
        console.error(e);
    }
  };

  if (isCompact) {
    return (
      <div className="w-full flex flex-col gap-3 animate-slide-in-up">
         <div className="flex items-center justify-between px-1">
             <h3 className="text-[11px] font-bold text-gray-500 uppercase tracking-wider">
                Active Context ({files.length})
             </h3>
             <button 
               onClick={() => fileInputRef.current?.click()}
               className="text-[10px] bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded transition-all flex items-center gap-1 border border-emerald-500/20"
             >
               <Upload size={10} /> Add Docs
             </button>
         </div>

         <div className="space-y-1 max-h-[150px] overflow-y-auto px-1 scrollbar-thin">
            {files.map((file, i) => (
                <div key={i} className="group flex items-center justify-between p-2 rounded-md bg-white/5 hover:bg-white/10 transition-colors border border-transparent hover:border-white/5">
                    <div className="flex items-center gap-2 overflow-hidden">
                        <FileText size={12} className="text-gray-500 shrink-0" />
                        <span className="text-[12px] text-gray-300 truncate">{file}</span>
                    </div>
                    <button 
                      onClick={() => removeFile(file)}
                      className="text-gray-600 hover:text-red-100 transition-opacity"
                    >
                        <X size={12} />
                    </button>
                </div>
            ))}
            {status === 'uploading' && (
               <div className="flex items-center gap-2 p-2 rounded-md bg-emerald-500/5 border border-emerald-500/10">
                   <Loader2 size={10} className="animate-spin text-emerald-400" />
                   <span className="text-[10px] text-emerald-400">Processing...</span>
               </div>
            )}
         </div>
         <input type="file" ref={fileInputRef} onChange={handleFileSelect} className="hidden" accept=".pdf,.docx,.txt,.md" multiple />
      </div>
    );
  }

  return (
    <div className="w-full max-w-xl mx-auto">
      <div 
        className={cn(
          "relative border border-dashed rounded-3xl p-12 transition-all duration-300 ease-in-out cursor-pointer overflow-hidden group",
          isDragging ? "border-emerald-500 bg-emerald-500/5 scale-[1.02]" : "border-white/10 hover:border-emerald-500/50 hover:bg-white/5 glass",
          status === 'error' ? "border-red-500/50 bg-red-500/5" : ""
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input type="file" ref={fileInputRef} onChange={handleFileSelect} className="hidden" accept=".pdf,.docx,.txt,.md" multiple />
        <div className="absolute inset-0 bg-gradient-to-tr from-emerald-500/10 to-blue-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
        <div className="relative flex flex-col items-center justify-center text-center space-y-6">
          {status === 'idle' && (
            <>
              <div className="p-5 rounded-2xl bg-gradient-to-br from-gray-800 to-gray-900 shadow-xl ring-1 ring-white/10 group-hover:scale-110 transition-transform duration-300">
                <Upload className="w-8 h-8 text-emerald-400" />
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-semibold text-white tracking-tight">Upload Knowledge Docs</h3>
                <p className="text-sm text-gray-400 leading-relaxed max-w-[260px] mx-auto">
                  Drag & drop your documents here.<br/> Multiple files supported.
                </p>
              </div>
            </>
          )}

          {status === 'uploading' && (
            <div className="space-y-4 w-full max-w-sm">
                <div className="flex items-center justify-between text-white border-b border-white/10 pb-2">
                   <span className="text-sm font-medium">Processing Queue ({processingCount})</span>
                   <Loader2 size={14} className="animate-spin text-emerald-400" />
                </div>
                <div className="flex flex-col gap-2">
                   <div className="flex items-center gap-3 bg-gray-900/40 p-2.5 rounded-lg border border-white/5">
                        <div className="h-1.5 flex-1 bg-gray-700 rounded-full overflow-hidden">
                             <div className="h-full bg-emerald-500 rounded-full animate-progress" style={{ width: '60%' }}></div>
                         </div>
                   </div>
                </div>
            </div>
          )}

          {status === 'success' && (
            <>
               <div className="p-4 rounded-full bg-emerald-500/10 ring-1 ring-emerald-500/50 animate-bounce-short">
                <CheckCircle className="w-10 h-10 text-emerald-400" />
              </div>
              <div>
                <p className="text-lg font-medium text-white">Analysis Complete</p>
                <p className="text-sm text-gray-400">Opening workspace...</p>
              </div>
            </>
          )}

          {status === 'error' && (
            <>
              <div className="p-4 rounded-full bg-red-500/10 ring-1 ring-red-500/50">
                <AlertCircle className="w-10 h-10 text-red-400" />
              </div>
              <div>
                <p className="text-red-400 font-medium">{errorMessage || "Upload failed"}</p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
