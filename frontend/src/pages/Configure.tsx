import { useEffect, useState } from "react";
import ColumnSelector from "@/components/ColumnSelector";
import api from "@/api";
import { motion } from "framer-motion";

export default function Configure() {
  const [columns, setColumns] = useState<string[]>([]);
  const [dtypes, setDtypes] = useState<Record<string, string>>({});
  const [target, setTarget] = useState("");
  const [features, setFeatures] = useState<string[]>([]);
  const [split, setSplit] = useState(0.2);
  const [algorithm, setAlgorithm] = useState("linear_regression");
  const [algorithms, setAlgorithms] = useState<string[]>([]);
  const [algoInfo, setAlgoInfo] = useState<Record<string, any>>({});
  const [recommended, setRecommended] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const datasetId = localStorage.getItem("dataset_id");

  useEffect(() => {
    const fetchInfo = async () => {
      if (!datasetId) return;
      try {
        const res = await api.get(`/datasets/${datasetId}/info`);
        if (Array.isArray(res.data?.columns)) {
          setColumns(res.data.columns);
          setDtypes(res.data.dtypes || {});
        }
      } catch {}
    };
    fetchInfo();
  }, [datasetId]);

  useEffect(() => {
    if (target && dtypes[target]) {
      const dtype = dtypes[target];
      if (dtype === "object" || dtype === "category") {
        setAlgorithm("random_forest_classifier");
        setRecommended("random_forest_classifier");
      } else {
        setAlgorithm("linear_regression");
        setRecommended("linear_regression");
      }
    }
  }, [target, dtypes]);

  useEffect(() => {
    const fetchAlgos = async () => {
      try {
        const res = await api.get("/experiments/algorithms");
        if (Array.isArray(res.data?.algorithms)) setAlgorithms(res.data.algorithms);
      } catch {
        setAlgorithms([
          "linear_regression",
          "ridge_regression",
          "lasso_regression",
          "random_forest_regressor",
          "gradient_boosting_regressor",
          "decision_tree_regressor",
          "logistic_regression",
          "random_forest_classifier",
          "gradient_boosting_classifier",
          "decision_tree_classifier",
          "svm_classifier",
          "knn_classifier",
        ]);
      }
    };
    fetchAlgos();
  }, []);

  useEffect(() => {
    const fetchAlgoInfo = async () => {
      try {
        const res = await api.get("/experiments/algorithm-info");
        setAlgoInfo(res.data || {});
      } catch {}
    };
    fetchAlgoInfo();
  }, []);

  async function runExperiment() {
    if (!datasetId) return;
    setBusy(true);
    setError(null);
    try {
      const res = await api.post("/experiments/run", {
        dataset_id: datasetId,
        target,
        features,
        split,
        algorithm,
      });
      window.location.href = `/results/${res.data.experiment_id}`;
    } catch (e: any) {
      setError(e?.response?.data?.detail || "❌ Failed to start experiment.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="grid gap-6 animate-fadeIn">
      {/* Header */}
      <motion.div
        className="glass p-6 shadow-card"
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2 className="text-3xl font-bold text-primary mb-2">
          Configure Experiment
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Dataset ID: {datasetId ?? "-"}
        </p>
      </motion.div>

      {/* Column selection */}
      <motion.div
        className="glass p-6 shadow-card"
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <h3 className="text-lg font-semibold mb-4 text-primary">
          Select Target & Features
        </h3>
        {columns.length > 0 ? (
          <ColumnSelector
            columns={columns}
            target={target}
            setTarget={setTarget}
            features={features}
            setFeatures={setFeatures}
          />
        ) : (
          <>
            <div className="label">Target column</div>
            <input
              className="input mb-4"
              placeholder="e.g., price"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
            />
            <div className="label">Features (comma-separated)</div>
            <input
              className="input"
              placeholder="e.g., rooms,area,age"
              onChange={(e) =>
                setFeatures(
                  e.target.value
                    .split(",")
                    .map((s) => s.trim())
                    .filter(Boolean)
                )
              }
            />
          </>
        )}
      </motion.div>

      {/* Algorithm selection */}
      <motion.div
        className="glass p-6 shadow-card"
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <div className="label">Algorithm</div>
        <select
          value={algorithm}
          onChange={(e) => setAlgorithm(e.target.value)}
          className="input w-60"
        >
          {algorithms.map((algo) => (
            <option key={algo} value={algo}>
              {algo.replace(/_/g, " ")}
            </option>
          ))}
        </select>

        {algoInfo[algorithm] && (
          <motion.div
            className="mt-4 p-4 rounded-xl bg-slate-100 dark:bg-slate-800 shadow-inner"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            {recommended === algorithm && (
              <span className="text-xs bg-green-500 text-white px-2 py-1 rounded-full mr-2">
                ✅ Recommended
              </span>
            )}
            <p className="text-sm">
              <strong>Description:</strong> {algoInfo[algorithm].description}
            </p>
            <p className="text-sm mt-1">
              <strong>Best For:</strong> {algoInfo[algorithm].best_for}
            </p>
          </motion.div>
        )}
      </motion.div>

      {/* Split + Run */}
      <motion.div
        className="glass p-6 grid sm:grid-cols-2 gap-4 shadow-card"
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <div>
          <div className="label">Test split (0.1 - 0.9)</div>
          <input
            type="number"
            min={0.1}
            max={0.9}
            step={0.05}
            value={split}
            onChange={(e) => setSplit(parseFloat(e.target.value))}
            className="input w-40"
          />
        </div>
        <div className="self-end">
          <button
            className="btn-primary w-full hover-scale"
            onClick={runExperiment}
            disabled={busy || !target || features.length === 0}
          >
            {busy ? "Running..." : "🚀 Run Experiment"}
          </button>
        </div>
      </motion.div>

      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded-lg text-sm">
          {error}
        </div>
      )}
    </div>
  );
}
