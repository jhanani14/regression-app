import { motion } from "framer-motion";
import { Menu, Upload, SlidersHorizontal, History, LogOut } from "lucide-react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";


const links = [
{ to: "/upload", label: "Upload", Icon: Upload },
{ to: "/configure", label: "Configure", Icon: SlidersHorizontal },
{ to: "/history", label: "History", Icon: History },
];


export default function Sidebar() {
const [open, setOpen] = useState<boolean>(() => localStorage.getItem("sb_open") !== "0");
const navigate = useNavigate();
const loc = useLocation();
useEffect(() => localStorage.setItem("sb_open", open ? "1" : "0"), [open]);
const logout = () => {
localStorage.removeItem("token");
navigate("/auth");
};
return (
<motion.aside
initial={{ width: open ? 224 : 64 }}
animate={{ width: open ? 224 : 64 }}
transition={{ duration: 0.3 }}
className="h-screen sticky top-0 flex flex-col bg-primary text-white shadow-card"
>
<div className="flex items-center justify-between p-3 border-b border-white/20">
{open && <span className="font-bold tracking-wide text-lg">ML Studio</span>}
<button className="p-2 hover:bg-white/20 rounded-lg" onClick={() => setOpen((v) => !v)}>
<Menu size={20} />
</button>
</div>
<nav className="flex-1 mt-2 space-y-1">
{links.map(({ to, label, Icon }) => {
const active = loc.pathname.startsWith(to);
return (
<Link
key={to}
to={to}
className={`group flex items-center gap-3 px-3 py-2 mx-2 rounded-lg transition-colors ${active ? "bg-white/20 shadow-inner" : "hover:bg-white/10"}`}
title={!open ? label : undefined}
>
<Icon size={20} />
{open && <span className="text-sm font-medium">{label}</span>}
</Link>
);
})}
</nav>
<button className="flex items-center gap-3 px-3 py-2 mx-2 mb-3 rounded-lg hover:bg-white/10" onClick={logout}>
<LogOut size={20} />
{open && <span className="text-sm font-medium">Logout</span>}
</button>
</motion.aside>
);
}