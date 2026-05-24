"use client";
import Link from "next/link";
import { TEMPLE_NAME } from "@/data/templeData";
import ThemeToggle from "./ThemeToggle";

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-white/70 dark:bg-gray-950/70 border-b border-orange-200/30 dark:border-orange-900/20">
      <div className="max-w-4xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo + Name */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-amber-500 flex items-center justify-center shadow-lg shadow-orange-500/25 group-hover:shadow-orange-500/40 transition-shadow">
              <span className="text-white text-lg">🛕</span>
            </div>
            <div>
              <h1 className="text-sm font-bold text-gray-900 dark:text-white leading-tight">
                {TEMPLE_NAME}
              </h1>
              <p className="text-[10px] text-orange-600 dark:text-orange-400 font-medium">
                AI Voice Assistant
              </p>
            </div>
          </Link>

          {/* Theme Toggle */}
          <div className="flex items-center">
            <ThemeToggle />
          </div>
        </div>
      </div>
    </nav>
  );
}
