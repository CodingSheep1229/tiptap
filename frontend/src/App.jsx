import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { PendingTransactions } from './components/PendingTransactions';
import { TipRecords } from './components/TipRecords';
import { TestingPanel } from './components/TestingPanel';
import { Logs } from './components/Logs';
import { api } from './services/api';

function App() {
  const [pendingTransactions, setPendingTransactions] = useState([]);
  const [tipRecords, setTipRecords] = useState([]);
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const addLog = (message, type = 'info') => {
    setLogs(prev => [...prev, { message, type, timestamp: Date.now() }]);
  };

  const loadData = async () => {
    try {
      const [pending, tips] = await Promise.all([
        api.getPendingTransactions(),
        api.getTipRecords()
      ]);

      // Filter out pending transactions that already have tips recorded
      const recordedPendingIds = new Set(tips.map(t => t.pending_txn_id));
      const unrecordedPending = pending.filter(txn => !recordedPendingIds.has(txn.plaid_txn_id));

      setPendingTransactions(unrecordedPending);
      setTipRecords(tips);
    } catch (error) {
      addLog(`Failed to load data: ${error.message}`, 'error');
    }
  };

  const handleConnectBank = async () => {
    setIsLoading(true);
    addLog('Requesting link token...');

    try {
      const { link_token } = await api.createLinkToken();
      addLog('Got link token ✓', 'success');

      const handler = window.Plaid.create({
        token: link_token,
        onSuccess: async (public_token, metadata) => {
          addLog('Link success. Public token received ✓', 'success');
          addLog(`Institution: ${metadata.institution?.name || 'n/a'}`);

          try {
            const { item_id } = await api.exchangePublicToken(public_token);
            addLog(`Exchange OK → item_id=${item_id}`, 'success');
            await handleSync();
          } catch (error) {
            addLog(error.message, 'error');
          }
        },
        onExit: (err, metadata) => {
          if (err) {
            addLog(`Link exit: ${err.error_code} — ${err.error_message}`, 'error');
          } else {
            addLog('Link exited by user.');
          }
          setIsLoading(false);
        },
      });

      handler.open();
    } catch (error) {
      addLog(error.message, 'error');
      setIsLoading(false);
    }
  };

  const handleSync = async () => {
    setIsLoading(true);
    addLog('Triggering /sync...');

    try {
      await api.manualSync();
      addLog('Sync requested ✓ (check API logs for results)', 'success');
      await loadData();
    } catch (error) {
      addLog(`Sync failed: ${error.message}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRecordTip = async (txnId, tipAmount) => {
    setIsLoading(true);

    try {
      const { expected_total } = await api.recordTip(txnId, tipAmount);
      addLog(`Tip recorded! Expected total: $${expected_total.toFixed(2)}`, 'success');
      await loadData();
    } catch (error) {
      addLog(`Failed to record tip: ${error.message}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateTestItem = async () => {
    setIsLoading(true);
    addLog('Creating test item with dynamic transactions...');

    try {
      const { message } = await api.createTestItem();
      addLog(`✓ ${message}`, 'success');
      await loadData();
    } catch (error) {
      addLog(`Failed: ${error.message}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSimulateUpdate = async () => {
    setIsLoading(true);
    addLog('Simulating transaction updates (pending → posted, +$1 overcharge)...');

    try {
      const { message } = await api.simulateTransactionUpdate();
      addLog(`✓ ${message}`, 'success');
      await loadData();
    } catch (error) {
      addLog(`Failed: ${error.message}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  // Load data on mount
  useEffect(() => {
    loadData();
  }, []);

  // Load Plaid Link script
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdn.plaid.com/link/v2/stable/link-initialize.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div className="min-h-screen">
      <Header
        onConnectBank={handleConnectBank}
        onSync={handleSync}
        onRefresh={loadData}
        isLoading={isLoading}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="grid grid-cols-1 gap-8">
          {/* Testing Panel */}
          <TestingPanel
            onCreateTestItem={handleCreateTestItem}
            onSimulateUpdate={handleSimulateUpdate}
            isLoading={isLoading}
          />

          {/* Logs */}
          <Logs logs={logs} />

          {/* Pending Transactions */}
          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-4">Pending Transactions</h2>
            <p className="text-slate-600 mb-6">
              Record your tip amount for pending restaurant charges
            </p>
            <PendingTransactions
              transactions={pendingTransactions}
              onRecordTip={handleRecordTip}
              isLoading={isLoading}
            />
          </section>

          {/* Tip Records */}
          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-4">Tip Records</h2>
            <p className="text-slate-600 mb-6">
              Track your tip records and see if any restaurants overcharged you
            </p>
            <TipRecords records={tipRecords} />
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;
