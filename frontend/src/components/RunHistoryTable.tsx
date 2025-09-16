import { ExperimentItem } from "@/types";
import { formatDate } from "@/utils/formatDate";

export default function RunHistoryTable({ rows }: { rows: ExperimentItem[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead className="bg-black bg-opacity-5 dark:bg-white dark:bg-opacity-5">
          <tr>
            <th className="text-left p-3">ID</th>
            <th className="text-left p-3">Created</th>
            <th className="text-left p-3">Target</th>
            <th className="text-left p-3">Status</th>
            <th className="text-left p-3">R²</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => {
            const r2 = r.metrics?.r2 ?? null;
            const statusColor =
              r.status === "failed"
                ? "bg-red-500"
                : r.status === "running"
                ? "bg-yellow-500"
                : "bg-green-500";

            return (
              <tr
                key={r.id}
                className={`cursor-pointer transition hover:scale-[1.01] hover:shadow-md ${
                  i % 2 === 0
                    ? "bg-black bg-opacity-0"
                    : "bg-black bg-opacity-[0.02] dark:bg-white dark:bg-opacity-[0.02]"
                }`}
                onClick={() => (window.location.href = `/results/${r.id}`)}
              >
                <td className="p-3 font-mono text-xs">{r.id}</td>
                <td className="p-3">
                  {r.created_at ? formatDate(r.created_at) : "-"}
                </td>
                <td className="p-3">{r.target || "-"}</td>
                <td className="p-3">
                  <span
                    className={`px-2 py-1 text-xs rounded-full text-white ${statusColor}`}
                  >
                    {r.status || "done"}
                  </span>
                </td>
                <td
                  className={`p-3 font-medium ${
                    r2 !== null && r2 >= 0.7
                      ? "text-green-600"
                      : r2 !== null && r2 < 0.4
                      ? "text-red-600"
                      : "text-slate-600 dark:text-slate-300"
                  }`}
                >
                  {r2 !== null ? r2.toFixed(4) : "-"}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
