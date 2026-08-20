import React, { useState, useEffect } from 'react';
import { X, Copy, Check, Download, FileCode, Folder, Terminal } from 'lucide-react';
import { PythonCodeFile } from '../types';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const PythonCodeModal: React.FC<ModalProps> = ({ isOpen, onClose }) => {
  const [files, setFiles] = useState<PythonCodeFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<PythonCodeFile | null>(null);
  const [copied, setCopied] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (isOpen) {
      fetch('/api/python-files')
        .then((res) => res.json())
        .then((data) => {
          if (data.success && data.files.length > 0) {
            setFiles(data.files);
            setSelectedFile(data.files[0]);
          }
        })
        .catch((err) => console.error('Failed to load python files:', err))
        .finally(() => setLoading(false));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const copyToClipboard = () => {
    if (selectedFile) {
      navigator.clipboard.writeText(selectedFile.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const downloadFile = (file: PythonCodeFile) => {
    const blob = new Blob([file.content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.name;
    a.click();
  };

  const downloadAllAsScript = () => {
    const setupFile = files.find((f) => f.name === 'setup_project.py');
    if (setupFile) {
      downloadFile(setupFile);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-6xl h-[88vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-600/20 text-blue-400 border border-blue-500/30 rounded-lg">
              <FileCode className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-100">Python Project Repository</h2>
              <p className="text-xs text-slate-400">
                Full, complete, non-truncated Python source files runnable out-of-the-box
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={downloadAllAsScript}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold transition-colors shadow"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download setup_project.py</span>
            </button>

            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Body */}
        <div className="flex-1 flex overflow-hidden">
          {/* File Explorer Sidebar */}
          <div className="w-64 bg-slate-950 border-r border-slate-800 p-3 overflow-y-auto space-y-1">
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-2 py-1 flex items-center gap-1.5">
              <Folder className="w-3.5 h-3.5 text-blue-400" />
              <span>Project Files ({files.length})</span>
            </div>

            {loading ? (
              <div className="text-xs text-slate-500 p-3">Loading files...</div>
            ) : (
              files.map((file) => {
                const isSelected = selectedFile?.path === file.path;
                return (
                  <button
                    key={file.path}
                    onClick={() => setSelectedFile(file)}
                    className={`w-full text-left px-2.5 py-2 rounded-lg text-xs font-mono transition-all flex items-center gap-2 ${
                      isSelected
                        ? 'bg-blue-600/20 text-blue-300 font-semibold border border-blue-500/30'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                    }`}
                  >
                    <FileCode className="w-3.5 h-3.5 shrink-0" />
                    <span className="truncate">{file.path}</span>
                  </button>
                );
              })
            )}
          </div>

          {/* Code Viewer Area */}
          <div className="flex-1 flex flex-col bg-slate-900 overflow-hidden">
            {selectedFile && (
              <>
                <div className="px-4 py-2 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
                  <span className="text-xs font-mono text-blue-400 font-medium flex items-center gap-2">
                    <Terminal className="w-3.5 h-3.5" />
                    ### FILE: {selectedFile.path}
                  </span>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={copyToClipboard}
                      className="flex items-center gap-1 px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-xs transition-colors border border-slate-700"
                    >
                      {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      <span>{copied ? 'Copied!' : 'Copy Code'}</span>
                    </button>

                    <button
                      onClick={() => downloadFile(selectedFile)}
                      className="flex items-center gap-1 px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-xs transition-colors border border-slate-700"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Download File</span>
                    </button>
                  </div>
                </div>

                <div className="flex-1 p-4 overflow-auto font-mono text-xs text-slate-200 bg-[#0D1117] leading-relaxed">
                  <pre>{selectedFile.content}</pre>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
