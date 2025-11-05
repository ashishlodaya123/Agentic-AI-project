/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#2563EB',
        'secondary': '#4F46E5',
        'success': '#16A34A',
        'warning': '#EA580C',
        'error': '#DC2626',
        'neutral-background': '#F8FAFC',
        'neutral-surface': '#FFFFFF',
        'neutral-text': '#1E293B',
        'neutral-text-secondary': '#64748B',
        'neutral-border': '#E2E8F0',
      },
      spacing: {
        'xxs': '0.25rem',  // 4px
        'xs': '0.5rem',    // 8px
        'sm': '0.75rem',   // 12px
        'md': '1rem',      // 16px
        'lg': '1.5rem',    // 24px
        'xl': '2rem',      // 32px
        'xxl': '3rem',     // 48px
      },
    },
  },
  plugins: [],
}