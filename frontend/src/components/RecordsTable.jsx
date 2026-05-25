import api from "../services/api";

function RecordsTable({
  records,
  refreshData,
}) {
  const badgeClassByStatus = {
    APPROVED:
      "border-emerald-200 bg-emerald-50 text-emerald-700",
    REJECTED:
      "border-rose-200 bg-rose-50 text-rose-700",
    SUSPICIOUS:
      "border-amber-200 bg-amber-50 text-amber-700",
    PENDING:
      "border-slate-200 bg-slate-100 text-slate-700",
  };

  const approveRecord = async (id) => {

    try {

      await api.post(
        `records/${id}/approve/`
      );

      refreshData();

    } catch (error) {

      console.error(error);
    }
  };

  const rejectRecord = async (id) => {

    try {

      await api.post(
        `records/${id}/reject/`
      );

      refreshData();

    } catch (error) {

      console.error(error);
    }
  };

  return (
    <div className="glass-panel rise rounded-3xl p-6 md:p-8">
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
        <h2 className="headline text-2xl font-semibold md:text-3xl">
        ESG Records
        </h2>
        <p className="text-sm text-slate-500">
          {records.length} records
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full border-separate border-spacing-0">
          <thead>
            <tr className="text-left text-xs uppercase tracking-wide text-slate-500">
              <th className="border-b border-slate-200 px-3 py-3">Category</th>
              <th className="border-b border-slate-200 px-3 py-3">Scope</th>
              <th className="border-b border-slate-200 px-3 py-3">Amount</th>
              <th className="border-b border-slate-200 px-3 py-3">Unit</th>
              <th className="border-b border-slate-200 px-3 py-3">Status</th>
              <th className="border-b border-slate-200 px-3 py-3">Actions</th>
            </tr>
          </thead>

          <tbody>
            {records.length === 0 ? (
              <tr>
                <td className="px-3 py-8 text-center text-slate-500" colSpan={6}>
                  No records available. Upload a CSV to begin.
                </td>
              </tr>
            ) : null}
            {records.map((record) => (
              <tr key={record.id} className="transition hover:bg-white/60">
                <td className="border-b border-slate-100 px-3 py-3 font-semibold text-slate-800">
                  {record.category}
                </td>

                <td className="border-b border-slate-100 px-3 py-3 text-slate-700">
                  {record.scope}
                </td>

                <td className="border-b border-slate-100 px-3 py-3 font-medium text-slate-800">
                  {record.activity_amount}
                </td>

                <td className="border-b border-slate-100 px-3 py-3 text-slate-700">
                  {record.unit}
                </td>

                <td className="border-b border-slate-100 px-3 py-3">
                  <span
                    className={`rounded-full border px-3 py-1 text-xs font-semibold tracking-wide ${
                      badgeClassByStatus[record.status] || badgeClassByStatus.PENDING
                    }`}
                  >
                    {record.status}
                  </span>
                </td>

                <td className="border-b border-slate-100 px-3 py-3">
                  {!record.is_locked && (
                    <div className="flex gap-2">
                      <button
                        onClick={() =>
                          approveRecord(record.id)
                        }
                        className="rounded-lg bg-emerald-600 px-3 py-2 text-sm font-semibold text-white transition hover:bg-emerald-700"
                      >
                        Approve
                      </button>

                      <button
                        onClick={() =>
                          rejectRecord(record.id)
                        }
                        className="rounded-lg bg-rose-600 px-3 py-2 text-sm font-semibold text-white transition hover:bg-rose-700"
                      >
                        Reject
                      </button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RecordsTable;
