# PRP: Pitch Deck Interativo — codrsync x Inventeer

## Objective
Criar uma apresentação interativa de pitch deck como single-page HTML com 16 slides fullscreen, animações, navegação por teclado/touch/dots, e design dark premium.

## Current State
Nenhum arquivo existe. Specs completas fornecidas pelo usuário.

## Target State
Um único `index.html` com CSS e JS inline, 16 slides interativos, totalmente responsivo e print-friendly.

## Implementation Plan

### Sprint 1 — Estrutura e Navegação
- [x] Boilerplate HTML com meta tags, Google Fonts (Inter), CSS reset
- [x] CSS design tokens (custom properties: cores, tipografia, spacing)
- [x] Layout base: 16 sections fullscreen com scroll-snap-type: y mandatory
- [x] Dots de navegação laterais fixos na direita
- [x] Progress bar fixa no topo
- [x] Contador "Slide X de 16" no canto inferior
- [x] Keyboard navigation (ArrowUp/Down, PageUp/Down, Home/End)
- [x] Touch swipe para mobile
- [x] Intersection Observer para detectar slide ativo e animar elementos

### Sprint 2 — Slides 1-4 (Capa, Problema, Solução, Traction)
- [x] Slide 1: Capa com logo gradiente, fade-in sequencial, badge, pulse animation
- [x] Slide 2: Problema com 4 cards animados + número grande $17B+ (counter animado)
- [x] Slide 3: Solução com grid 2x4 features + badges "LIVE"
- [x] Slide 4: Traction com métricas + tabela custo de replicação com barras animadas

### Sprint 3 — Slides 5-8 (Timing, Inventeer, Proposta, Investimento)
- [x] Slide 5: Timeline horizontal interativa com 4 marcos + fill animation
- [x] Slide 6: 2 colunas com setas conectando necessidades/ofertas
- [x] Slide 7: Donut chart CSS animado 55/45 + cards lado a lado
- [x] Slide 8: Tabela comparativa 4 opções com highlight na proposta

### Sprint 4 — Slides 9-12 (Receita, Roadmap, Competitiva, Riscos)
- [x] Slide 9: Gráfico de barras CSS animado MRR + linha breakeven
- [x] Slide 10: 3 colunas roadmap com timeline vertical + fill animation
- [x] Slide 11: 3 círculos concêntricos CSS + tabela comparativa com checkmarks
- [x] Slide 12: Grid 2x3 cards risco/mitigação com hover transition

### Sprint 5 — Slides 13-16 (Termos, Sobre, Próximos Passos, Encerramento)
- [x] Slide 13: Tabela term sheet elegante com fundo semi-transparente
- [x] Slide 14: Foto placeholder + badges + logos grayscale + stats
- [x] Slide 15: 5 steps verticais com timeline + CTA pulsante (mailto link)
- [x] Slide 16: Gradiente sutil + typewriter effect + contato

### Sprint 6 — Polish
- [x] Responsividade mobile (media queries 768px e 480px)
- [x] @media print layout vertical
- [x] Keyboard: Home/End adicionados
- [x] Performance: zero libs externas, apenas Google Fonts

## Files to Modify
- `index.html`: Arquivo único com todo HTML, CSS inline e JS inline

## Validation
- [ ] Todos os 16 slides renderizam corretamente
- [ ] Scroll-snap funciona suavemente
- [ ] Dots de navegação refletem slide atual
- [ ] Keyboard navigation funciona (arrows + page up/down)
- [ ] Animações disparam ao entrar no viewport
- [ ] Responsivo em mobile
- [ ] Print layout funcional
