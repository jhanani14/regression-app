import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "@/api";
import MetricCards from "@/components/MetricCards";
import { ExperimentMetrics } from "@/types";
import { motion } from "framer-motion";
import { FileDown } from "lucide-react";

export default function Results() {
  const { id } = useParams();
  const [metrics, setMetrics] = useState<ExperimentMetrics | undefined>();
  const [plots, setPlots] = useState<string[]>([]);
  const [algorithm, setAlgorithm] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.get(`/experiments/${id}`);
        setMetrics(res.data.metrics);
        setPlots(res.data.plots || []);
        setAlgorithm(res.data.algorithm);
      } catch (err: any) {
        setError(err?.response?.data?.detail || "❌ Failed to fetch results");
      } finally {
        setLoading(false);
      }
    };
    if (id) load();
  }, [id]);

  const downloadPDF = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("You must be logged in to download.");
        return;
      }

      const res = await fetch(
        `http://localhost:8000/experiments/${id}/download?token=${token}`
      );

      if (!res.ok) throw new Error("Download failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `experiment_${id}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      alert("❌ Failed to download PDF");
    }
  };

  return (
    <motion.div
      className="grid gap-6 animate-fadeIn"
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      {/* Header */}
      <div className="glass p-6 shadow-card">
        <h2 className="text-3xl font-bold text-primary">Results</h2>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Experiment ID: {id}
        </p>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Algorithm: {algorithm.replace(/_/g, " ")}
        </p>
      </div>

      {loading ? (
        <div className="glass p-6 text-center">Loading results...</div>
      ) : error ? (
        <div className="glass p-6 text-red-600">{error}</div>
      ) : !metrics ? (
        <div className="glass p-6">No results available for this experiment.</div>
      ) : (
        <>
          {/* Metrics Section */}
          <MetricCards metrics={metrics} />

          {/* Plots Section */}
          <div className="grid md:grid-cols-2 gap-6">
            {plots.length > 0 ? (
              plots.map((b64, i) => (
                <motion.div
                  key={i}
                  className="glass p-4 rounded-2xl shadow-card hover-scale"
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                >
                  <h3 className="text-lg font-semibold mb-3 text-primary">
                    {algorithm.includes("classifier") ||
                    algorithm.includes("logistic") ||
                    algorithm.includes("svm") ||
                    algorithm.includes("knn")
                      ? i === 0
                        ? "Confusion Matrix"
                        : "ROC Curve"
                      : i === 0
                      ? "Residual Plot"
                      : "Predicted vs Actual"}
                  </h3>
                  <img
                    alt={`Plot ${i + 1}`}
                    className="w-full rounded-xl shadow-soft"
                    src={`data:image/png;base64,${b64}`}
                  />
                </motion.div>
              ))
            ) : (
              <p className="text-slate-500 text-center">No plots available.</p>
            )}
          </div>

          {/* Download Button */}
          <div className="flex justify-center">
            <button
              className="btn-primary hover-scale flex items-center gap-2 px-6 py-3 rounded-full"
              onClick={downloadPDF}
            >
              <FileDown size={18} />
              Download Results (PDF)
            </button>
          </div>
        </>
      )}
    </motion.div>
  );
}
