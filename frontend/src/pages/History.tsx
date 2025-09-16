import { useEffect, useState } from "react";
import api from "@/api";
import RunHistoryTable from "@/components/RunHistoryTable";
import { ExperimentItem } from "@/types";
import { motion } from "framer-motion";
import { Clock } from "lucide-react"; // ✅ Guaranteed icon

export default function History() {
  const [rows, setRows] = useState<ExperimentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.get("/experiments");
        setRows(res.data || []);
      } catch (err: any) {
        setError(err?.response?.data?.detail || "❌ Failed to fetch history.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <motion.div
      className="grid gap-6 animate-fadeIn"
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
    >
      {/* Header */}
      <div className="glass p-6 flex items-center gap-3 shadow-card">
        <Clock size={24} className="text-primary" /> {/* ✅ Changed to Clock */}
        <h2 className="text-3xl font-bold text-primary">Experiment History</h2>
      </div>

      {loading ? (
        <div className="glass p-6 text-center">Loading...</div>
      ) : error ? (
        <div className="glass p-6 text-red-600">{error}</div>
      ) : rows.length === 0 ? (
        <div className="glass p-6 text-slate-500 text-center">
          No experiments found. Upload a dataset and run one!
        </div>
      ) : (
        <div className="glass p-0 overflow-hidden shadow-card">
          <div className="overflow-x-auto">
            <RunHistoryTable rows={rows} />
          </div>
        </div>
      )}
    </motion.div>
  );
}
