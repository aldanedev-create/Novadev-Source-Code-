export default {
  content: ['./index.html', './src/**/*.vue', './src/**/*.js'],
  theme: {
    extend: {
      colors: {
        nova: {
          primary: 'var(--nova-primary)',
          accent: 'var(--nova-accent)',
          surface: 'var(--nova-surface)',
          text: 'var(--nova-text)',
          muted: 'var(--nova-muted)'
        }
      },
      borderRadius: {
        nova: 'var(--nova-radius)'
      },
      fontFamily: {
        sans: ['var(--nova-font)', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif']
      }
    }
  },
  plugins: []
}
