/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        serif: ["'Source Serif 4'", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      colors: {
        paper: "#F3F5F0",
        surface: "#FFFFFF",
        ink: "#23262B",
        muted: "#6B7280",
        border: "#DCE1D8",
        navy: {
          DEFAULT: "#2B3A55",
          light: "#3E4F70",
        },
        amber: {
          DEFAULT: "#C97D2E",
          light: "#E8A85C",
        },
        sage: {
          DEFAULT: "#5B7A5B",
          light: "#7C9473",
        },
      },
    },
  },
  plugins: [],
};
