# Project Analysis — Enduro Atari Clone

## Resumo
Recriação do clássico jogo Enduro do Atari 2600 jogável no smartphone via browser.
O Enduro original (1983, Activision) é um jogo de corrida em perspectiva traseira onde o jogador ultrapassa carros em uma estrada reta com mudanças de cenário (dia, noite, neve, neblina).

## Tech Stack
- **HTML5 Canvas** — renderização do jogo
- **JavaScript vanilla** — lógica do jogo (sem dependências)
- **CSS** — layout responsivo mobile-first
- **Touch controls** — swipe/toque para controle no smartphone

## Features do Jogo Original
1. Visão traseira do carro do jogador
2. Estrada com perspectiva (ponto de fuga)
3. Carros inimigos para ultrapassar
4. Meta diária de ultrapassagens (200 no dia 1, incrementa)
5. Ciclo dia/noite com mudança de paleta de cores
6. Condições climáticas (neve, neblina)
7. Velocímetro e contador de carros ultrapassados
8. Colisão reduz velocidade
9. Aceleração e frenagem

## Arquitetura
- Single-page HTML com canvas fullscreen
- Game loop com requestAnimationFrame
- Touch controls: toque esquerda/direita para mover, toque inferior para frear
- Pseudo-3D com linhas de estrada escaladas por profundidade
- Sprites em pixel art estilo Atari

## Constraints
- Mobile-first (toque como controle principal)
- Sem dependências externas
- Deve rodar em qualquer browser moderno
- Performance otimizada para mobile

## Tarefas Recomendadas
1. Criar estrutura HTML + Canvas responsivo
2. Implementar estrada pseudo-3D com perspectiva
3. Carro do jogador com controles touch
4. Carros inimigos com IA simples
5. Sistema de colisão e física
6. HUD (velocidade, carros ultrapassados, dia)
7. Ciclo dia/noite com paletas de cores
8. Tela inicial e game over
9. Sons retro (opcional via Web Audio API)
