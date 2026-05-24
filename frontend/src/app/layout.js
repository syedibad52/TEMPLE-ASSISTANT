import "./globals.css";
import { Toaster } from "react-hot-toast";

export const metadata = {
  title: "Sri Raghavendra Swamy Temple | AI Voice Assistant",
  description:
    "AI-powered temple guide for Sri Raghavendra Swamy Temple. Get pooja timings, festival information, darshan details, and more in English and Kannada. Speak to our intelligent temple assistant.",
  keywords: [
    "temple",
    "AI assistant",
    "Sri Raghavendra Swamy",
    "pooja timings",
    "Kannada",
    "voice assistant",
    "temple guide",
    "darshan",
    "festivals",
  ],
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark" data-scroll-behavior="smooth" suppressHydrationWarning>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#FF6B35" />
      </head>
      <body className="bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 antialiased transition-colors duration-300">
        {children}
        <Toaster
          position="bottom-right"
          toastOptions={{
            className: "!bg-white/80 dark:!bg-gray-900/80 !backdrop-blur-xl !border !border-orange-200/30 dark:!border-orange-800/20 !text-gray-900 dark:!text-white !shadow-2xl !rounded-2xl",
            duration: 4000,
          }}
        />
      </body>
    </html>
  );
}
