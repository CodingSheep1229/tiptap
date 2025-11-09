import { RefreshCw, Landmark } from 'lucide-react';

export function Header({ onConnectBank, onSync, onRefresh, isLoading }) {
  return (
    <div className="bg-white shadow-sm border-b border-slate-200 mb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <img
              src="/logo.png"
              alt="TipTap Logo"
              className="w-12 h-12 object-contain"
            />
            <div>
              <h1 className="text-3xl font-bold text-slate-900">TipTap</h1>
              <p className="text-sm text-slate-600">Restaurant Tip Tracker</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={onConnectBank}
              disabled={isLoading}
              className="btn-primary flex items-center space-x-2"
            >
              <Landmark className="w-4 h-4" />
              <span>Connect Bank</span>
            </button>

            <button
              onClick={onSync}
              disabled={isLoading}
              className="btn-secondary flex items-center space-x-2"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              <span>Sync</span>
            </button>

            <button
              onClick={onRefresh}
              disabled={isLoading}
              className="btn-secondary"
            >
              Refresh
            </button>
          </div>
        </div>

        <p className="mt-4 text-slate-600 text-sm max-w-2xl">
          Track restaurant charges and detect tip overcharges automatically. Record your tip when you see a pending charge,
          and we'll verify it when the transaction posts.
        </p>
      </div>
    </div>
  );
}
