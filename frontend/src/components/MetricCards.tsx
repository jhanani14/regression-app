import { ExperimentMetrics } from "@/types";
import { motion } from "framer-motion";

export default function MetricCards({ metrics }: { metrics?: ExperimentMetrics }) {
  if (!metrics) return null;

  const labelMap: Record<string, string> = {
    rmse: "RMSE",
    r2: "R²",
    accuracy: "Accuracy",
    f1: "F1 Score",
  };

  const getColor = (key: string, value: number) => {
    if (key === "accuracy" || key === "f1" || key === "r2") {
      return value > 0.8 ? "text-green-500" : value > 0.5 ? "text-yellow-500" : "text-red-500";
    }
    if (key === "rmse") {
      return value < 5 ? "text-green-500" : value < 10 ? "text-yellow-500" : "text-red-500";
    }
    return "text-slate-600 dark:text-slate-300";
  };

  return (
    <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
      {Object.entries(metrics).map(([key, value], idx) => {
        const label = labelMap[key] || key;
        let displayValue: string | number = "-";

        if (typeof value === "number") {
          displayValue = key === "accuracy" ? (value * 100).toFixed(2) + "%" : value.toFixed(4);
        }

        return (
          <motion.div
            key={key}
            className="glass backdrop-blur-lg p-5 rounded-xl shadow-sm hover-scale cursor-default"
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1, duration: 0.3 }}
          >
            <div className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">
              {label}
            </div>
            <div
              className={`text-2xl font-bold mt-2 ${typeof value === "number" ? getColor(key, value) : ""}`}
            >
              {displayValue}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
