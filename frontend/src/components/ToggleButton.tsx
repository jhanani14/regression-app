import { useEffect, useState } from "react";

export default function ToggleButton() {
  const [theme, setTheme] = useState<"light" | "dark">(
    (localStorage.getItem("theme") as "light" | "dark") ||
      (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")
  );

  useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") root.classList.add("dark");
    else root.classList.remove("dark");
    localStorage.setItem("theme", theme);
  }, [theme]);

  const isDark = theme === "dark";

  return (
    <button
      aria-label="Toggle theme"
      onClick={() => setTheme(isDark ? "light" : "dark")}
      className="btn-ghost rounded-full p-2 hover-scale hover:bg-white hover:bg-opacity-20 dark:hover:bg-slate-700 dark:hover:bg-opacity-40 transition"
      title={`Switch to ${isDark ? "light" : "dark"} mode`}
    >
      {isDark ? (
        <svg width="22" height="22" viewBox="0 0 24 24" className="fill-yellow-400 drop-shadow">
          <path d="M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.8 1.42-1.42zM1 13h3v-2H1v2zm10 10h2v-3h-2v3zm9.66-18.95l-1.41-1.41-1.8 1.79 1.42 1.42 1.79-1.8zM17.24 19.16l1.8 1.79 1.41-1.41-1.79-1.8-1.42 1.42zM20 11v2h3v-2h-3zM12 4c-4.42 0-8 3.58-8 8s3.58 8 8 8a8 8 0 000-16z"/>
        </svg>
      ) : (
        <svg width="22" height="22" viewBox="0 0 24 24" className="fill-primary drop-shadow">
          <path d="M12 4a8 8 0 109.95 6.32 1 1 0 00-1.49-1.09A6 6 0 1112 6a1 1 0 000-2z"/>
        </svg>
      )}
    </button>
  );
}