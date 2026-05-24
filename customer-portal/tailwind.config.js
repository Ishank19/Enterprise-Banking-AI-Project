/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#101828",
        "bank-blue": "#175CD3",
        "bank-cyan": "#06AED4",
        "bank-green": "#039855",
        "soft-line": "#D0D5DD"
      },
      boxShadow: {
        fintech: "0 18px 45px rgba(16, 24, 40, 0.10)"
      }
    }
  },
  plugins: []
};
