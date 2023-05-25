/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*"],
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
      black : "#000000"
    }
  },
  plugins: [],
}