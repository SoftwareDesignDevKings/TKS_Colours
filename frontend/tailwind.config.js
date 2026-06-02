/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Primary brand — dark slate
        surface: {
          DEFAULT: '#0f172a',
          card: '#1e293b',
          elevated: '#273549',
          border: '#334155',
        },
        // Accent — violet
        accent: {
          DEFAULT: '#7c3aed',
          light: '#a78bfa',
          dark: '#5b21b6',
        },
        // Club colours
        club: {
          media: '#f59e0b',
          programming: '#6366f1',
          robotics: '#10b981',
          cyber: '#ef4444',
          ai: '#8b5cf6',
        },
        // Status colours
        status: {
          pending: '#f59e0b',
          approved: '#10b981',
          rejected: '#ef4444',
          withdrawn: '#6b7280',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        xl: '1rem',
        '2xl': '1.5rem',
      },
      boxShadow: {
        card: '0 4px 24px 0 rgba(0, 0, 0, 0.4)',
        glow: '0 0 20px rgba(124, 58, 237, 0.3)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-soft': 'pulseSoft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.6' },
        },
      },
    },
  },
  plugins: [],
}
