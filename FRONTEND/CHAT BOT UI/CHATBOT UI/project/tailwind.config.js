/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'electric-purple': '#7A5AF8',
        'neon-cyan': '#3DE5FF',
        'magenta': '#FF2EA6',
        'slate-dark': '#0B0F1A',
        'lime-accent': '#B7FF3C',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      backdropBlur: {
        'xs': '2px',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { 
            boxShadow: '0 0 20px rgba(122, 90, 248, 0.5), 0 0 30px rgba(61, 229, 255, 0.3)' 
          },
          '100%': { 
            boxShadow: '0 0 30px rgba(122, 90, 248, 0.7), 0 0 40px rgba(61, 229, 255, 0.5)' 
          },
        },
      },
    },
  },
  plugins: [],
};