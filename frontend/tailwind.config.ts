import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#F8FAFC",
        surface: "#FFFFFF",
        border: "#E2E8F0",
        primary: {
          50: "#f0f7fa",
          100: "#d9ecf2",
          500: "#1b7a9e",
          700: "#0f5a7a",
          800: "#0B4F6C",
          900: "#083a50",
        },
        accent: {
          50: "#fcf8ee",
          100: "#f7edd1",
          500: "#d99b38",
          600: "#C5832B",
          700: "#a6681e",
        },
        success: {
          50: "#ecfdf5",
          100: "#d1fae5",
          600: "#059669",
          700: "#047857",
        },
        danger: {
          50: "#fef2f2",
          100: "#fee2e2",
          600: "#DC2626",
          700: "#b91c1c",
        },
        warning: {
          50: "#fffbeb",
          100: "#fef3c7",
          600: "#D97706",
          700: "#b45309",
        },
        info: {
          50: "#eff6ff",
          100: "#dbeafe",
          600: "#2563EB",
          700: "#1d4ed8",
        }
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
