/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
        colors: {
            "primary": "#0056A3",
            "secondary": "#EE8600",
            "accent": "#6CC1EB",
            "background-light": "#F8FAFC",
            "surface": "#FFFFFF",
            "text-main": "#1E293B",
            "text-muted": "#64748B",
            "muted": "#64748B",
            "border-color": "#E2E8F0",
            "sidebar-bg": "#0056A3"
        },
        fontFamily: {
            "display": ["Newsreader", "'Roboto Slab'", "serif"],
            "body": ["Geologica", "Inter", "sans-serif"]
        },
        borderRadius: {
            "DEFAULT": "0px",
            "lg": "0px",
            "xl": "0px",
            "full": "9999px"
        },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}
