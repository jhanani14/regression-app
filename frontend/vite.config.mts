import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],

  // ✅ Optional alias for clean imports like "@/components/..."
  resolve: {
    alias: {
      "@": "/src",
    },
  },

  // ✅ Local development server
  server: {
    port: 5173,
  },

  // ✅ Ensure process.env and import.meta.env both work
  define: {
    "process.env": {}, // avoids axios/env reference issues
  },
});
