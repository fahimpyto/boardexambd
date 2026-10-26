/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*.html',
    './assets/js/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif', '"Noto Sans Bengali"', 'Vrinda', 'SolaimanLipi'],
      },
      boxShadow: {
        soft: '0 10px 30px -12px rgba(30, 27, 75, 0.18)',
      },
    },
  },
  plugins: [],
};
