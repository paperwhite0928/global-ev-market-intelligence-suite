/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        mercedes: {
          dark: "#0a0e17",
          panel: "#0f172a",
          border: "#1e293b",
          silver: "#94a3b8",
          blue: "#38bdf8",
          accent: "#2563eb",
          danger: "#f43f5e",
          warning: "#f59e0b",
          success: "#10b981",
          gold: "#fbbf24"
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'monospace']
      }
    },
  },
  plugins: [],
}
