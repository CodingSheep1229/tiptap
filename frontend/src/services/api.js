const API_BASE_URL = import.meta.env.VITE_API_URL || '';

class ApiService {
  async createLinkToken() {
    const res = await fetch(`${API_BASE_URL}/link/token`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to create link token');
    return res.json();
  }

  async exchangePublicToken(publicToken) {
    const res = await fetch(`${API_BASE_URL}/exchange`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ public_token: publicToken })
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Exchange failed: ${text}`);
    }
    return res.json();
  }

  async manualSync() {
    const res = await fetch(`${API_BASE_URL}/sync`, { method: 'POST' });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Sync failed: ${text}`);
    }
    return res.json();
  }

  async getPendingTransactions() {
    const res = await fetch(`${API_BASE_URL}/transactions/pending`);
    if (!res.ok) throw new Error('Failed to fetch pending transactions');
    return res.json();
  }

  async recordTip(pendingTxnId, tipAmount) {
    const res = await fetch(`${API_BASE_URL}/tips`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pending_txn_id: pendingTxnId,
        tip_amount: tipAmount
      })
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Failed to record tip: ${text}`);
    }
    return res.json();
  }

  async getTipRecords() {
    const res = await fetch(`${API_BASE_URL}/tips`);
    if (!res.ok) throw new Error('Failed to fetch tip records');
    return res.json();
  }

  async createTestItem() {
    const res = await fetch(`${API_BASE_URL}/sandbox/create_test_item`, { method: 'POST' });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Failed to create test item: ${text}`);
    }
    return res.json();
  }

  async simulateTransactionUpdate() {
    const res = await fetch(`${API_BASE_URL}/sandbox/simulate_transaction_update`, { method: 'POST' });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Failed to simulate update: ${text}`);
    }
    return res.json();
  }
}

export const api = new ApiService();
