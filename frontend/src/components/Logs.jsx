import { Terminal, CheckCircle, XCircle, Info } from 'lucide-react';

export function Logs({ logs }) {
  if (logs.length === 0) return null;

  const getIcon = (type) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-4 h-4 text-emerald-600" />;
      case 'error':
        return <XCircle className="w-4 h-4 text-red-600" />;
      default:
        return <Info className="w-4 h-4 text-blue-600" />;
    }
  };

  const getTextColor = (type) => {
    switch (type) {
      case 'success':
        return 'text-emerald-700';
      case 'error':
        return 'text-red-700';
      default:
        return 'text-slate-700';
    }
  };

  return (
    <div className="card bg-slate-50 border-slate-300 max-h-64 overflow-y-auto">
      <div className="flex items-center space-x-2 mb-3 pb-3 border-b border-slate-200">
        <Terminal className="w-5 h-5 text-slate-600" />
        <h3 className="font-semibold text-slate-900">Activity Log</h3>
      </div>
      <div className="space-y-2 font-mono text-sm">
        {logs.map((log, index) => (
          <div key={index} className="flex items-start space-x-2">
            {getIcon(log.type)}
            <span className={getTextColor(log.type)}>{log.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
