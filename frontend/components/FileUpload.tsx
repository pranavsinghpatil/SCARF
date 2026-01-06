'use client';

import React, { useRef, useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Loader2, X } from 'lucide-react';
import { uploadDocument, deleteFile } from '../lib/api';
import { cn } from '../lib/utils';

interface FileUploadProps {
  onUploadComplete: (filename: string) => void;
  isCompact?: boolean;
}

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
    
    // Add temp names immediately for UI feedback
    const newNames = Array.from(fileList).map(f => f.name);
    
    try {
      const result = await uploadDocument(fileList, sessionId);
      
      // Handle partial success/errors if backend returned them
      if (result.errors && result.errors.length > 0) {
          console.warn("Some files failed:", result.errors);
          // show warning visually? For now just log.
      }

      setStatus('success');
      // Merge new files with existing, avoiding duplicates
      const updated = Array.from(new Set([...files, ...result.filenames]));
      onFilesChange(updated);
      
      // Wait a bit to show success state before triggering parent action (which might hide this component)
      setTimeout(() => {
          onUploadComplete();
          setStatus('idle'); 
      }, 1500);
      
    } catch (error: any) {
      console.error(error);
      setStatus('error');
      setErrorMessage(error.response?.data?.detail || "Upload failed. Please check file format.");
    }
  };



  const removeFile = async (nameToRemove: string) => {
    // Optimistic UI update
    const updated = files.filter(f => f !== nameToRemove);
    onFilesChange(updated);
    
    // Background deletion
    try {
        await deleteFile(nameToRemove, sessionId);
    } catch (e) {
        console.error("Failed to delete file from backend:", e);
        // We could revert the UI change here, but for now let's assume it's fine 
        // as the file is effectively removed from the current context list anyway.
    }
  };

  // Compact View (for when chat is active)
  if (isCompact) {
    return (
      <div 
        className="glass rounded-xl p-4 w-full max-w-2xl mx-auto transition-all animate-slide-in-up flex flex-col gap-4"
      >
         <div className="flex items-center justify-between">
             <h3 className="text-sm font-medium text-white flex items-center gap-2">
                <FileText size={16} className="text-emerald-400" />
                Active Documents
                <span className="text-xs bg-white/10 px-2 py-0.5 rounded-full text-gray-300">{files.length}</span>
             </h3>
             <button 
               onClick={() => fileInputRef.current?.click()}
               className="text-xs bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 px-3 py-1.5 rounded-lg border border-emerald-500/20 transition-all flex items-center gap-2"
             >
               <Upload size={12} /> Add Files
             </button>
         </div>

         {/* File List */}
         <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-h-[120px] overflow-y-auto pr-1">
            {files.map((file, i) => (
                <div key={i} className="group flex items-center justify-between p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/5">
                    <span className="text-xs text-gray-300 truncate max-w-[80%]" title={file}>{file}</span>
                    <button 
                      onClick={() => removeFile(file)}
                      className="p-1 text-gray-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        <X size={12} />
                    </button>
                </div>
            ))}
            {status === 'uploading' && (
               <div className="flex items-center gap-2 p-2 rounded-lg bg-emerald-500/5 border border-emerald-500/20">
                   <Loader2 size={12} className="animate-spin text-emerald-400" />
                   <span className="text-xs text-emerald-400">Processing {processingCount} files...</span>
               </div>
            )}
         </div>
         
         <input type="file" ref={fileInputRef} onChange={handleFileSelect} className="hidden" accept=".pdf,.docx,.txt,.md" multiple />
      </div>
    );
  }

  // Active Upload View (Hero)
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
        
        {/* Glow Effect */}
        <div className="absolute inset-0 bg-gradient-to-tr from-emerald-500/10 to-blue-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
        
        <div className="relative flex flex-col items-center justify-center text-center space-y-6">
          {status === 'idle' && (
            <>
              <div className="p-5 rounded-2xl bg-gradient-to-br from-gray-800 to-gray-900 shadow-xl ring-1 ring-white/10 group-hover:scale-110 transition-transform duration-300">
                <Upload className="w-8 h-8 text-emerald-400" />
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-semibold text-white tracking-tight">Upload Knowledge Base</h3>
                <p className="text-sm text-gray-400 leading-relaxed max-w-[260px] mx-auto">
                  Drag & drop your documents (PDF, DOCX, TXT) here. Multiple files supported.
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
                {/* Mock list for uploading state */}
                <div className="flex flex-col gap-2">
                   <div className="flex items-center gap-3 bg-gray-900/40 p-2.5 rounded-lg border border-white/5">
                        <div className="h-1.5 flex-1 bg-gray-700 rounded-full overflow-hidden">
                             <div className="h-full bg-emerald-500 rounded-full animate-progress" style={{ width: '60%' }}></div>
                         </div>
                   </div>
                </div>
                <p className="text-[10px] text-gray-500 text-center">Parallel extraction & vectorization enabled</p>
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
