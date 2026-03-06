# PRP: Enduro Atari Clone — Mobile

## Objective
Criar um clone jogável do Enduro (Atari 2600) otimizado para smartphone, com controles touch, estrada pseudo-3D, carros inimigos e ciclo dia/noite.

## Current State
Nenhum arquivo existe — projeto do zero.

## Target State
Jogo completo jogável no browser mobile com:
- Estrada pseudo-3D com perspectiva
- Carro do jogador controlado por toque
- Carros inimigos para ultrapassar
- Meta de ultrapassagens por dia
- Ciclo dia/noite com paletas diferentes
- Tela inicial, HUD e game over
- Sons retro opcionais

## Implementation Plan

### Sprint 1 — Core do Jogo
- [x] 1. `index.html` — Estrutura HTML com canvas responsivo e meta tags mobile
- [x] 2. `styles.css` — Layout fullscreen mobile-first, orientação portrait
- [x] 3. `game.js` — Game loop principal (init, update, render, requestAnimationFrame)
- [x] 4. Renderização da estrada pseudo-3D (segmentos, perspectiva, faixas)
- [x] 5. Carro do jogador (sprite pixel art, posição, renderização)
- [x] 6. Controles touch (esquerda/direita por toque nas metades da tela, freio na parte inferior)
- [x] 7. Controles teclado (setas para teste em desktop)
- [x] 8. Carros inimigos (spawn, movimento, escala por profundidade)
- [x] 9. Sistema de colisão (jogador vs inimigos, redução de velocidade)
- [x] 10. Velocidade e aceleração (auto-acelera, freio, colisão desacelera)
- [x] 11. HUD (velocímetro, carros ultrapassados, dia atual, meta)
- [x] 12. Ciclo dia/noite (paletas de cores: dia, entardecer, noite, amanhecer)
- [x] 13. Efeito neve/neblina em dias avançados
- [x] 14. Sistema de dias e metas (200 carros dia 1, incrementa)
- [x] 15. Tela inicial com título e "Toque para Jogar"
- [x] 16. Tela de game over (não atingiu a meta)
- [x] 17. Sons retro via Web Audio API (motor, colisão, ultrapassagem)
- [x] 18. Vibração no celular ao colidir (Vibration API)

## Files Created
- `index.html`: Estrutura principal, canvas, links para CSS/JS
- `styles.css`: Layout responsivo, fullscreen, mobile-first
- `game.js`: Toda lógica do jogo (~650 linhas)

## Validation
- [x] Jogo carrega sem erros no console
- [x] Estrada renderiza com perspectiva correta
- [x] Controles touch funcionam no mobile
- [x] Carros inimigos aparecem e podem ser ultrapassados
- [x] Colisão funciona corretamente
- [x] HUD mostra informações corretas
- [x] Ciclo dia/noite funciona
- [x] Tela inicial e game over funcionam
- [x] Performance estável (60fps) no mobile
