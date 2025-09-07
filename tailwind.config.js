/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './accounts/templates/**/*.html',
    './core/templates/**/*.html',
    './events/templates/**/*.html',
    './static/js/**/*.js',
    './**/*.html',
    './**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}