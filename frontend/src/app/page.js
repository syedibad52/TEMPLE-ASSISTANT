"use client";
import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import VoiceAssistant from "@/components/VoiceAssistant";

export default function Home() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  return (
    <main className="relative min-h-screen flex flex-col justify-between overflow-hidden">
      <Navbar />

      {/* Animated gradient background */}
      <div className="absolute inset-0 -z-20 bg-gradient-to-br from-orange-50 via-amber-50 to-purple-50 dark:from-gray-950 dark:via-purple-950/30 dark:to-orange-950/20" />

      {/* Floating Orbs */}
      <div className="absolute inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-orange-400/20 dark:bg-orange-500/10 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-amber-400/20 dark:bg-amber-500/10 rounded-full blur-3xl animate-float-delayed" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-400/10 dark:bg-purple-500/5 rounded-full blur-3xl animate-pulse-slow" />
      </div>

      {/* Floating spiritual symbols */}
      {mounted && (
        <div className="absolute inset-0 -z-10 overflow-hidden pointer-events-none">
          {["🕉️", "🪷", "🪔", "🔔", "🙏"].map((symbol, i) => (
            <div
              key={i}
              className="absolute text-2xl opacity-15 dark:opacity-5 animate-float-symbol"
              style={{
                left: `${10 + i * 20}%`,
                top: `${15 + (i % 3) * 25}%`,
                animationDelay: `${i * 1.5}s`,
                animationDuration: `${6 + i}s`,
              }}
            >
              {symbol}
            </div>
          ))}
        </div>
      )}

      <div className="flex-1 flex flex-col items-center justify-center pt-24 pb-12 px-4 relative z-10">
        <div className="w-full max-w-4xl mx-auto">
          {/* Header Section */}
          <div className="text-center mb-8">
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/60 dark:bg-white/5 backdrop-blur-lg border border-orange-200/50 dark:border-orange-800/30 text-orange-700 dark:text-orange-400 text-xs font-semibold mb-4 shadow-sm">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
              AI Temple Guide • Active
            </span>
            <h1 className="text-4xl sm:text-5xl font-bold mb-3 tracking-tight">
              <span className="bg-gradient-to-r from-orange-600 via-amber-500 to-orange-600 dark:from-orange-400 dark:via-amber-300 dark:to-orange-400 bg-clip-text text-transparent">
                Sri Raghavendra Swamy Temple
              </span>
            </h1>
            <p className="text-lg text-orange-700/80 dark:text-orange-300/60 font-medium mb-3">
              ಶ್ರೀ ರಾಘವೇಂದ್ರ ಸ್ವಾಮಿ ದೇವಸ್ಥಾನ
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto">
              Speak or type your question in English or Kannada. Our AI assistant will guide you about temple timings, daily poojas, and services.
            </p>
          </div>

          {/* Voice Assistant Card */}
          <div className="rounded-3xl bg-white/75 dark:bg-gray-900/60 backdrop-blur-xl border border-orange-200/30 dark:border-orange-800/20 shadow-2xl shadow-orange-500/5 overflow-hidden transition-all duration-300 hover:shadow-orange-500/10">
            <VoiceAssistant />
          </div>

          {/* Core Feature Tips */}
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[
              { icon: "🎤", title: "Voice Interaction", desc: "Speak in English or Kannada to ask naturally" },
              { icon: "🌐", title: "Bilingual Response", desc: "Get intelligent voice & text replies in both languages" },
              { icon: "🤖", title: "Smart Guidance", desc: "Real-time info on poojas, timings, and history" },
            ].map((tip, i) => (
              <div
                key={i}
                className="p-4 rounded-2xl bg-white/50 dark:bg-white/5 backdrop-blur-md border border-orange-100/30 dark:border-orange-900/10 text-center transition-all hover:scale-[1.02]"
              >
                <span className="text-2xl">{tip.icon}</span>
                <h3 className="text-sm font-semibold text-gray-900 dark:text-white mt-2">{tip.title}</h3>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{tip.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Simplified Footer */}
      <footer className="w-full py-4 text-center border-t border-orange-200/20 dark:border-orange-900/10 relative z-10 bg-white/30 dark:bg-gray-950/30 backdrop-blur-sm">
        <p className="text-xs text-gray-500 dark:text-gray-500">
          © {new Date().getFullYear()} Sri Raghavendra Swamy Temple • Dedicated AI Voice Assistant
        </p>
      </footer>
    </main>
  );
}
