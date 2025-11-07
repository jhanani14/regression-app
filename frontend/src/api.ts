import axios from "axios";

// ✅ Load API base URL dynamically from environment variables
// In production (Amplify), this will come from .env.production or Amplify Environment Variables
const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000"; // fallback for local dev

// ✅ Create a reusable Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// ✅ Automatically attach JWT token (if exists) for every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ✅ Handle unauthorized responses globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      localStorage.removeItem("token");
      if (!location.pathname.startsWith("/auth")) {
        location.href = "/auth";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
