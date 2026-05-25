import { useEffect, useState } from "react";

import api from "../services/api";

import DashboardCards from "../components/DashboardCards";
import RecordsTable from "../components/RecordsTable";
import UploadForm from "../components/UploadForm";

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [records, setRecords] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    setError("");
    try {
      const statsResponse = await api.get(
        "dashboard/stats/"
      );

      const recordsResponse = await api.get(
        "records/"
      );

      setStats(statsResponse.data);

      setRecords(recordsResponse.data);
    } catch (error) {
      setError("Unable to load dashboard data. Please refresh.");
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen px-4 py-8 md:px-8">
      <div className="mx-auto w-full max-w-7xl space-y-6">
        <header className="glass-panel rise rounded-3xl p-6 md:p-8">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-700">
            Breathe ESG Platform
          </p>
          <h1 className="headline mt-3 text-3xl font-semibold leading-tight md:text-4xl">
            ESG Data Operations Dashboard
          </h1>
          <p className="mt-3 max-w-2xl text-sm text-slate-600 md:text-base">
            Ingest, review, and approve sustainability records with a consistent
            and auditable workflow.
          </p>
        </header>

        <UploadForm onUploadSuccess={fetchDashboardData} />

        {error ? (
          <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
            {error}
          </div>
        ) : null}

        {isLoading ? (
          <div className="glass-panel rounded-3xl p-8 text-center text-slate-600">
            Loading dashboard...
          </div>
        ) : null}

        {stats && !isLoading && (
          <DashboardCards stats={stats} />
        )}

        <RecordsTable
          records={records}
          refreshData={fetchDashboardData}
        />
      </div>
    </div>
  );
}

export default Dashboard;
