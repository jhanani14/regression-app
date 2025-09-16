import Sidebar from "@/components/Sidebar";
import Navbar from "@/components/Navbar";
import { PropsWithChildren } from "react";

export default function DashboardLayout({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen text-slate-800 dark:text-slate-100 flex">
      <Sidebar />
      <div className="flex-1 min-w-0">
        <Navbar />
        <main className="max-w-6xl mx-auto px-4 pb-12">{children}</main>
      </div>
    </div>
  );
}
