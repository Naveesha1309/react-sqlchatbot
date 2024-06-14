/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      
        colors: {
    
          'login-color': '#ffedd5',
          'login-color-button-hover':'#fb923c',
          'login-color-button-hover-dark':'#f97316',
          'navbar': '#171717'
        }
  
    },
    
  },
  plugins: [],
}

