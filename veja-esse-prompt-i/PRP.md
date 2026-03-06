# PRP: codrsync Strategic Response — Apresentação Interativa HTML

## Objetivo
Criar um único `index.html` com 12 slides fullscreen, scroll-snap, dark premium, totalmente interativo.

## Arquitetura
- 1 arquivo: `index.html` com CSS e JS inline
- Estrutura: `<section class="slide" id="slide-N">` × 12
- Navegação global: dots, teclado, swipe
- Barra de progresso fixa no topo
- Intersection Observer para animações de entrada

## Checklist

### Setup & Shell
- [ ] Estrutura HTML base com meta, Google Fonts (Inter), scroll-snap
- [ ] CSS reset + variáveis (--bg, --cyan, --white)
- [ ] Barra de progresso fixa no topo
- [ ] Dots de navegação laterais
- [ ] Contador "Slide X de 12" no canto inferior
- [ ] JS: keyboard navigation (ArrowUp/Down, PageUp/Down)
- [ ] JS: touch swipe mobile
- [ ] JS: Intersection Observer para fade-in

### Ato 1 — Slides 1-4
- [ ] Slide 1: Capa — logo gradiente, subtítulo, badge pulsante, seta animada
- [ ] Slide 2: Terminal animado com delays progressivos + 3 cards de métricas
- [ ] Slide 3: Split layout SEM vs COM codrsync, diálogos fake, animação sequencial
- [ ] Slide 4: Grid 2×3 de providers com toggles clicáveis

### Ato 2 — Slides 5-8
- [ ] Slide 5: Calculadora ROI — 3 sliders, cálculo em tempo real JS
- [ ] Slide 6: Diagrama de evolução + 3 cards de modelos de receita
- [ ] Slide 7: Tabela comparativa 3 colunas com cores (vermelho/verde)
- [ ] Slide 8: Timeline horizontal 4 marcos + comparativo de investimento

### Ato 3 — Slides 9-12
- [ ] Slide 9: 2 cards grandes (Equity + Contrato) com badge central
- [ ] Slide 10: Split layout Inventeer vs Ciro — projeção de ganhos
- [ ] Slide 11: 4 steps verticais com timeline + CTA
- [ ] Slide 12: Encerramento — typewriter effect, contato, badge confidencial

### Finalização
- [ ] @media print layout vertical
- [ ] Testar navegação teclado e dots
- [ ] Verificar responsividade mobile

## Arquivo a criar
- `index.html` — tudo inline

## Validação
- Scroll-snap funcionando (12 slides)
- Terminal animado executando sequencialmente
- Sliders da calculadora atualizando em tempo real
- Toggles de provider respondendo ao clique
- Navegação por teclado e dots funcionando
