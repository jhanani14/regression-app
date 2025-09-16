/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // ✅ Added js & jsx for full coverage
  ],
  theme: {
    extend: {
      // Re-enable white/black for Tailwind v4
      colors: {
        white: "#ffffff",
        black: "#000000",
        primary: "#4f46e5",   // Indigo 600
        secondary: "#10b981", // Emerald 500
        accent: "#f59e0b",    // Amber 500
      },
      boxShadow: {
        soft: "0 10px 35px rgba(0,0,0,0.06)",
        glow: "0 0 20px rgba(79,70,229,0.4)",
        card: "0 4px 15px rgba(0,0,0,0.08)",
      },
      backgroundImage: {
        "gradient-brand": "linear-gradient(to bottom right, #4f46e5, #10b981)",
      },
    },
  },
  plugins: [],
};
