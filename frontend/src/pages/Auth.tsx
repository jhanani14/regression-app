import { useState } from "react";
import api from "@/api";

export default function Auth() {
  const [tab, setTab] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true); 
    setError(null);
    try {
      const url = tab === "login" ? "/auth/login" : "/auth/register";
      const res = await api.post(url, { email, password });

      if (tab === "login") {
        localStorage.setItem("token", res.data.access_token);
        window.location.href = "/upload";
      } else {
        setTab("login");
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Something went wrong");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-brand">
      <div className="glass-gradient w-full max-w-md p-8 animate-fadeIn">
        {/* Tabs */}
        <div className="flex justify-between mb-6">
          <button
            className={`px-4 py-2 rounded-lg transition ${
              tab === "login" ? "bg-white/20" : "hover:bg-white/10"
            }`}
            onClick={() => setTab("login")}
          >
            Login
          </button>
          <button
            className={`px-4 py-2 rounded-lg transition ${
              tab === "register" ? "bg-white/20" : "hover:bg-white/10"
            }`}
            onClick={() => setTab("register")}
          >
            Register
          </button>
        </div>

        {/* Form */}
        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="label text-white">Email</label>
            <input
              className="input bg-white/90 text-black"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="label text-white">Password</label>
            <input
              className="input bg-white/90 text-black"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && (
            <div className="bg-red-500/80 text-white text-sm px-3 py-2 rounded-lg">
              {error}
            </div>
          )}

          <button
            className="btn-primary w-full hover-scale"
            disabled={busy}
          >
            {busy ? "Please wait..." : tab === "login" ? "Login" : "Create account"}
          </button>
        </form>
      </div>
    </div>
  );
}
