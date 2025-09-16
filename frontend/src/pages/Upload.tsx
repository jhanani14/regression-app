import { useState } from "react";
import api from "@/api";
import { Upload as UploadIcon } from "lucide-react";

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  async function handleUpload() {
    if (!file) return;
    setBusy(true);
    setMsg(null);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await api.post("/datasets/upload", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      localStorage.setItem("dataset_id", res.data.dataset_id);
      setMsg(`✅ Uploaded. Dataset ID: ${res.data.dataset_id}`);

      setTimeout(() => (window.location.href = "/configure"), 1000);
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || "❌ Upload failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="min-h-[80vh] flex justify-center items-center px-4">
      <div className="glass p-8 w-full max-w-lg animate-fadeIn">
        <h2 className="text-2xl font-bold text-primary mb-2">
          Upload Dataset
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400 mb-6">
          Supported formats: <b>CSV</b> or <b>XLSX</b>
        </p>

        {/* File Input */}
        <label className="flex flex-col items-center justify-center border-2 border-dashed border-primary/40 rounded-xl p-6 cursor-pointer hover:bg-primary/5 transition">
          <input
            type="file"
            accept=".csv,.xlsx"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="hidden"
          />
          <UploadIcon size={36} className="text-primary mb-3" />
          <span className="text-sm text-slate-600 dark:text-slate-300">
            {file ? file.name : "Click or drag file to upload"}
          </span>
        </label>

        <button
          onClick={handleUpload}
          disabled={!file || busy}
          className="btn-primary w-full mt-4 hover-scale"
        >
          {busy ? "Uploading..." : "Upload"}
        </button>

        {msg && (
          <div
            className={`mt-4 text-sm p-3 rounded-lg ${
              msg.startsWith("✅")
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            }`}
          >
            {msg}
          </div>
        )}
      </div>
    </div>
  );
}
