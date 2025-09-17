/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class", // ✅ keep dark mode working
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"], // ✅ ensures Tailwind scans all files
  theme: {
    extend: {
      boxShadow: {
        soft: "0 10px 35px rgba(0,0,0,0.06)", // ✅ custom shadow class
      },
    },
  },
  plugins: [],
};
