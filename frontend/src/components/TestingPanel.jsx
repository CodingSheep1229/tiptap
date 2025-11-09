import { FlaskConical, Zap } from 'lucide-react';

export function TestingPanel({ onCreateTestItem, onSimulateUpdate, isLoading }) {
  return (
    <div className="card bg-gradient-to-br from-amber-50 to-orange-50 border-amber-200">
      <div className="flex items-start space-x-4">
        <div className="bg-amber-100 p-3 rounded-lg">
          <FlaskConical className="w-6 h-6 text-amber-700" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-slate-900 mb-2">
            Sandbox Testing
          </h3>
          <p className="text-sm text-slate-700 mb-4">
            Use these tools to test tip overcharge detection with dynamic test data. The simulator will move
            pending transactions to posted and increment one by $1 to test overcharge detection.
          </p>
          <div className="flex space-x-3">
            <button
              onClick={onCreateTestItem}
              disabled={isLoading}
              className="btn-secondary btn-sm flex items-center space-x-2"
            >
              <FlaskConical className="w-4 h-4" />
              <span>Create Test Item (50 txns)</span>
            </button>
            <button
              onClick={onSimulateUpdate}
              disabled={isLoading}
              className="btn-secondary btn-sm flex items-center space-x-2"
            >
              <Zap className="w-4 h-4" />
              <span>Simulate Transaction Update</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
