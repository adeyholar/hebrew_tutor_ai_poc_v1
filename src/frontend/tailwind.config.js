/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        hebrew: ['HebrewFont', 'sans-serif'], // Extend for Hebrew
      },
      direction: {
        rtl: 'rtl', // Custom utility if needed
      },
    },
  },
  plugins: [],
};