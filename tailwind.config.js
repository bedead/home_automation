/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    './templates/**',
  ],
  theme: {
    extend: {},
    colors: {
      new_orange: {
        lighter: "#fc9433",
        brighter: "#fb841c",
      },
      new_brown: {
        lighter: "#df7827",
        brighter: "#c46c33",
      },
      new_white: {
        lighter: "#fcdec4",
        khaki: "#fcc48c"
      },
      white: {
        simple: "#ffffff",
        shade: "#ffebd9"
      },
      black: "#000000",
      gray: {
        50: '#f9fafb',
        200: '#e5e7eb',
        400: '#9ca3af',
        600: '#4b5563',
        800: '#1f2937',
        950: '#030712',
      },
      red: {
        600: '#dc2626',
        700: '#b91c1c',
        800: '#991b1b',
        900: '#7f1d1d',
        950: '#450a0a'
      }
    }
  },
  plugins: [],
}