import { useState } from 'react';
import { Receipt, DollarSign } from 'lucide-react';

export function PendingTransactions({ transactions, onRecordTip, isLoading }) {
  const [tipAmounts, setTipAmounts] = useState({});

  const handleRecordTip = async (txnId) => {
    const tipAmount = parseFloat(tipAmounts[txnId]);
    if (isNaN(tipAmount) || tipAmount < 0) {
      alert('Please enter a valid tip amount');
      return;
    }
    await onRecordTip(txnId, tipAmount);
    setTipAmounts(prev => ({ ...prev, [txnId]: '' }));
  };

  if (transactions.length === 0) {
    return (
      <div className="card text-center py-12">
        <Receipt className="w-16 h-16 text-slate-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-slate-900 mb-2">No Pending Transactions</h3>
        <p className="text-slate-600">
          Sync your account or create test data to see pending restaurant charges
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {transactions.map((txn) => (
        <div key={txn.plaid_txn_id} className="card">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3">
                <div className="bg-blue-100 p-2 rounded-lg">
                  <Receipt className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900">
                    {txn.merchant_name || 'Unknown Merchant'}
                  </h3>
                  <p className="text-sm text-slate-600">
                    Pending charge: ${Math.abs(txn.amount).toFixed(2)}
                    {' · '}
                    {txn.authorized_date || txn.date}
                  </p>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  placeholder="Tip amount"
                  value={tipAmounts[txn.plaid_txn_id] || ''}
                  onChange={(e) => setTipAmounts(prev => ({
                    ...prev,
                    [txn.plaid_txn_id]: e.target.value
                  }))}
                  className="input pl-8 w-32"
                  disabled={isLoading}
                />
              </div>
              <button
                onClick={() => handleRecordTip(txn.plaid_txn_id)}
                disabled={isLoading || !tipAmounts[txn.plaid_txn_id]}
                className="btn-success btn-sm"
              >
                Record Tip
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
