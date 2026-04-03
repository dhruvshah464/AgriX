import { useState, useRef, useEffect } from 'react';
import { Bot, Send, Sparkles, User, Loader2 } from 'lucide-react';
import { useAssistant } from '../hooks/useAssistant';

const suggestedQuestions = [
  'How can I improve wheat yield in low rainfall?',
  'When is the best time to apply DAP fertilizer?',
  'What are signs of nitrogen deficiency in rice?',
  'How to manage cotton bollworm organically?',
];

export default function AssistantPage() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const { loading, submitQuestion } = useAssistant();
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (text) => {
    const query = text || input.trim();
    if (!query) return;

    setMessages(prev => [...prev, { role: 'user', content: query }]);
    setInput('');

    try {
      const response = await submitQuestion(query);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response?.answer || 'I apologize, I couldn\'t process that request right now.',
        sources: response?.sources || [],
      }]);
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'The AI assistant is currently unavailable. Please ensure the backend service is running.',
        sources: [],
      }]);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center">
          <Bot size={20} className="text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-slate-800">AI Assistant</h1>
          <p className="text-sm text-slate-500">RAG-powered agricultural knowledge engine</p>
        </div>
      </div>

      {/* Chat area */}
      <div className="flex-1 overflow-y-auto rounded-xl bg-white border border-slate-100 shadow-card mb-4">
        {messages.length === 0 ? (
          /* Empty state */
          <div className="flex flex-col items-center justify-center h-full p-8 text-center">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-100 to-teal-100 flex items-center justify-center mb-4">
              <Sparkles size={28} className="text-emerald-600" />
            </div>
            <h3 className="text-base font-semibold text-slate-700 mb-1">Ask anything about farming</h3>
            <p className="text-sm text-slate-400 max-w-md mb-6">
              Get AI-powered answers about crop management, pest control, fertilization, and more.
            </p>
            <div className="flex flex-wrap gap-2 justify-center max-w-lg">
              {suggestedQuestions.map((q) => (
                <button
                  key={q}
                  onClick={() => handleSend(q)}
                  className="px-3 py-2 text-xs font-medium text-slate-600 bg-slate-50 hover:bg-green-50 hover:text-green-700 rounded-lg border border-slate-200 hover:border-green-200 transition-all"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="p-5 space-y-5">
            {messages.map((msg, i) => (
              <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
                {msg.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center flex-shrink-0">
                    <Bot size={16} className="text-white" />
                  </div>
                )}
                <div className={`max-w-[75%] ${
                  msg.role === 'user'
                    ? 'bg-green-600 text-white rounded-2xl rounded-tr-md px-4 py-3'
                    : 'bg-slate-50 text-slate-700 rounded-2xl rounded-tl-md px-4 py-3'
                }`}>
                  <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                  {msg.sources?.length > 0 && (
                    <div className="mt-3 pt-2 border-t border-slate-200/50">
                      <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1">Sources</p>
                      <ul className="space-y-0.5">
                        {msg.sources.map((s, j) => (
                          <li key={j} className="text-[11px] text-slate-500">• {s}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
                {msg.role === 'user' && (
                  <div className="w-8 h-8 rounded-lg bg-green-100 flex items-center justify-center flex-shrink-0">
                    <User size={16} className="text-green-700" />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center flex-shrink-0">
                  <Bot size={16} className="text-white" />
                </div>
                <div className="bg-slate-50 rounded-2xl rounded-tl-md px-4 py-3 flex items-center gap-2">
                  <Loader2 size={14} className="animate-spin text-green-600" />
                  <span className="text-sm text-slate-500">Thinking...</span>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="flex items-center gap-3 bg-white border border-slate-200 rounded-xl px-4 py-3 shadow-sm">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about farming..."
          className="flex-1 resize-none bg-transparent text-sm text-slate-800 placeholder:text-slate-400 outline-none max-h-24"
          rows={1}
          id="assistant-input"
        />
        <button
          onClick={() => handleSend()}
          disabled={loading || !input.trim()}
          className="w-9 h-9 rounded-lg bg-green-600 hover:bg-green-700 text-white flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}
