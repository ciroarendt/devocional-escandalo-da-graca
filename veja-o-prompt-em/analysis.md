# Project Analysis — Pitch Deck codrsync x Inventeer

## Tech Stack
- Single-file HTML (inline CSS + JS)
- Google Fonts (Inter)
- Pure CSS animations + Intersection Observer API
- CSS scroll-snap for slide navigation
- Zero external dependencies/frameworks

## Architecture
- 1 arquivo: `index.html`
- 16 sections fullscreen com scroll-snap
- CSS custom properties para design tokens
- Intersection Observer para animações de entrada
- Keyboard + touch navigation

## Key Patterns
- Dark premium theme (#0a0a0f base, #00d4ff accent)
- Fullscreen vertical scroll-snap slides
- Progressive disclosure via scroll animations
- CSS-only charts (barras, donut, circles concêntricos)
- Responsive: mobile-first com breakpoints
- Print-friendly @media print

## Constraints
- NO frameworks, NO libraries
- NO browser/GUI commands (headless container)
- Everything inline in single HTML file
- Must work on mobile (touch swipe)

## Scope
- 16 slides com conteúdo de pitch deck completo
- Navegação: dots laterais + teclado + swipe + progress bar
- Animações: fade-in, slide-in, typewriter, pulsing, bar growth
- CSS charts: barras horizontais, donut chart, timeline
- Tabelas comparativas estilizadas
- Print layout

## Recommended Approach
- Build slide-by-slide, test navigation first
- Use CSS custom properties for consistent theming
- Intersection Observer with threshold for triggering animations
- Touch events for mobile swipe detection
