# PRP: Spider-Man — Web Swing (Flappy Bird Style)

## Objective
Criar um jogo estilo Flappy Bird com tema Homem-Aranha: Longe de Casa, onde o personagem solta teia para subir em vez de bater asas, com cenário de cidades europeias. Inclui sistema de nickname e ranking mundial.

## Current State
Projeto vazio — nenhum arquivo de código existe ainda.

## Target State
Jogo completo e jogável no browser, com:
- Tela de entrada pedindo nickname do jogador
- Personagem Homem-Aranha animado
- Mecânica de teia (visual + física)
- Prédios europeus como obstáculos
- Background parallax com skyline
- Score system + Ranking Mundial (top 10)
- Tela de start, gameplay e game over
- Mobile + Desktop support

## Implementation Plan

### Sprint 1 — Estrutura e Game Engine
- [x] Criar `index.html` com canvas, tela de nickname e estrutura base
- [x] Criar `styles.css` com layout responsivo e UI
- [x] Criar `game.js` — módulo principal com game loop

### Sprint 2 — Nickname e Ranking System
- [x] Tela de entrada de nickname (primeira coisa ao abrir o jogo)
- [x] Sistema de ranking mundial salvo em localStorage (top 10)
- [x] Exibição do ranking na tela de Game Over e tela inicial

### Sprint 3 — Personagem e Física
- [x] Desenhar Homem-Aranha via Canvas (sprite estilizado)
- [x] Implementar gravidade e física de movimento
- [x] Implementar mecânica de "soltar teia" (impulso + animação da teia)
- [x] Animação do personagem (pose de swing)

### Sprint 4 — Obstáculos e Cenário
- [x] Criar sistema de obstáculos (prédios europeus com gap)
- [x] Background parallax com skyline europeia (múltiplas camadas)
- [x] Nuvens decorativas em movimento
- [x] Efeito de chão/base (cobblestone europeu)

### Sprint 5 — Colisão, Score e UI
- [x] Sistema de detecção de colisão
- [x] Sistema de pontuação (score + high score pessoal)
- [x] Tela inicial (título + instrução "Toque para lançar teia" + ranking)
- [x] Tela de Game Over com score, ranking e botão restart
- [x] Dificuldade progressiva (velocidade aumenta)

### Sprint 6 — Polish e Responsividade
- [x] Touch events para mobile
- [x] Efeitos visuais (partículas na teia, flash na colisão)
- [x] Ajustes de balanceamento (gravidade, gap, velocidade)
- [x] Teste e ajustes finais

## Files Created
- `index.html`: Canvas, tela de nickname, HUD, estrutura
- `styles.css`: Layout responsivo, tema Spider-Man, animações CSS
- `game.js`: Engine completa (780+ linhas)

## Validation
- [x] Ao abrir o jogo, pede nickname antes de qualquer coisa
- [x] Nickname aparece no HUD durante o jogo
- [x] Jogo inicia com tela de título após inserir nickname
- [x] Clique/toque/espaço lança teia e personagem sobe
- [x] Obstáculos aparecem e se movem da direita para esquerda
- [x] Colisão com obstáculo ou chão = Game Over
- [x] Score incrementa ao passar por obstáculos
- [x] Game Over mostra score + ranking mundial top 5
- [x] Ranking persiste entre sessões (localStorage)
- [x] Funciona em mobile (touch) e desktop (click/space)
- [x] Visual temático do Homem-Aranha: Longe de Casa
