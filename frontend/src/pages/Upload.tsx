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

      setTimeout(() => (window.location.href = "/configure"), 800);
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || "❌ Upload failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="min-h-screen flex justify-center items-center bg-slate-50 dark:bg-slate-950 transition-colors">
      <div className="glass w-full max-w-lg p-6">
        <h2 className="text-xl font-semibold mb-2">Upload Your Dataset</h2>
        <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">
          Supported formats: <b>CSV</b> or <b>XLSX</b>
        </p>

        <input
          type="file"
          accept=".csv,.xlsx"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="file:mr-3 file:py-2 file:px-4 file:rounded-lg 
                     file:border-0 file:bg-blue-600 file:text-white 
                     hover:file:bg-blue-700 cursor-pointer w-full"
        />

        <button
          onClick={handleUpload}
          disabled={!file || busy}
          className="btn-primary mt-4 flex items-center justify-center gap-2 w-full"
        >
          <UploadIcon size={18} />
          {busy ? "Uploading..." : "Upload"}
        </button>

        {msg && (
          <div
            className={`mt-4 text-sm p-2 rounded-lg ${
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
