import { CheckCircle2, AlertCircle, Clock, FileText } from 'lucide-react';

export function TipRecords({ records }) {
  if (records.length === 0) {
    return (
      <div className="card text-center py-12">
        <FileText className="w-16 h-16 text-slate-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-slate-900 mb-2">No Tip Records Yet</h3>
        <p className="text-slate-600">
          Record a tip for a pending transaction to start tracking
        </p>
      </div>
    );
  }

  const getStatusBadge = (record) => {
    if (record.checked_at) {
      if (record.is_overcharged) {
        return (
          <div className="flex items-center space-x-2">
            <span className="badge badge-warning flex items-center space-x-1">
              <AlertCircle className="w-3 h-3" />
              <span>OVERCHARGED ${record.overcharge_amount.toFixed(2)}</span>
            </span>
          </div>
        );
      }
      return (
        <span className="badge badge-success flex items-center space-x-1">
          <CheckCircle2 className="w-3 h-3" />
          <span>VERIFIED</span>
        </span>
      );
    }
    return (
      <span className="badge badge-pending flex items-center space-x-1">
        <Clock className="w-3 h-3" />
        <span>PENDING</span>
      </span>
    );
  };

  return (
    <div className="card overflow-hidden p-0">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Merchant
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Base Amount
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Expected Tip
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Expected Total
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Actual Total
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Status
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {records.map((record) => (
              <tr
                key={record.id}
                className={`hover:bg-slate-50 transition-colors ${
                  record.is_overcharged ? 'bg-amber-50' : ''
                }`}
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-slate-900">
                    {record.merchant_name || 'Unknown'}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                  ${Math.abs(record.pending_amount).toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                  ${record.expected_tip_amount.toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">
                  ${record.expected_total.toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                  {record.actual_total ? `$${record.actual_total.toFixed(2)}` : '—'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {getStatusBadge(record)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
