import { useState } from "react";
import ToggleButton from "./ToggleButton";
import { Menu, X } from "lucide-react";

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  const logout = () => {
    localStorage.removeItem("token");
    window.location.href = "/auth";
  };

  const NavLink = ({ href, children }: { href: string; children: React.ReactNode }) => {
    const isActive = window.location.pathname === href;
    return (
      <a
        href={href}
        className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors
        ${isActive ? "bg-primary text-white shadow-soft" : "hover:bg-slate-200 hover:bg-opacity-50 dark:hover:bg-slate-800 dark:hover:bg-opacity-50"}`}
        onClick={() => setMenuOpen(false)}
      >
        {children}
      </a>
    );
  };

  return (
    <header className="sticky top-0 z-20 bg-gradient-brand shadow-card text-white">
      <div className="max-w-6xl mx-auto flex items-center justify-between px-4 py-3">
        {/* Logo */}
        <a href="/upload" className="text-xl font-bold tracking-tight">
          <span className="text-white">ML</span> Studio
        </a>

        {/* Desktop Links */}
        <nav className="hidden md:flex items-center gap-2">
          <NavLink href="/upload">Upload</NavLink>
          <NavLink href="/configure">Configure</NavLink>
          <NavLink href="/history">History</NavLink>
          <ToggleButton />
          <button onClick={logout} className="px-3 py-2 rounded-lg hover:bg-slate-200 hover:bg-opacity-30">
            Logout
          </button>
        </nav>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden p-2 hover:bg-white hover:bg-opacity-20 rounded-lg"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {/* Mobile Menu Dropdown */}
      {menuOpen && (
        <div className="md:hidden bg-white dark:bg-slate-900 shadow-card rounded-b-2xl animate-fadeIn">
          <div className="flex flex-col px-4 py-3 gap-2">
            <NavLink href="/upload">Upload</NavLink>
            <NavLink href="/configure">Configure</NavLink>
            <NavLink href="/history">History</NavLink>
            <ToggleButton />
            <button onClick={logout} className="btn-ghost text-left">
              Logout
            </button>
          </div>
        </div>
      )}
    </header>
  );
}
