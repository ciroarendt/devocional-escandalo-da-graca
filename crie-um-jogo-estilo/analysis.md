# Project Analysis — Spider-Man: Web Swing (Flappy Bird Style)

## Conceito
Jogo estilo Flappy Bird onde o Homem-Aranha (tema "Longe de Casa") se move pela tela soltando teias para subir, em vez de bater asas. O cenário é inspirado em cidades europeias (referência ao filme).

## Tech Stack
- **HTML5 Canvas** — renderização do jogo
- **CSS3** — estilização da UI (menus, score, telas)
- **JavaScript Vanilla** — lógica do jogo, física, colisões
- **Sem dependências externas** — tudo standalone

## Features Principais
1. Personagem Homem-Aranha (sprite pixel art/desenhado via canvas)
2. Mecânica de "soltar teia" ao invés de flap (clique/toque dispara teia para cima)
3. Animação de teia sendo lançada para cima quando o jogador clica
4. Obstáculos estilo colunas/prédios europeus (tema Longe de Casa)
5. Background parallax com skyline de cidade europeia
6. Tela inicial com título temático
7. Sistema de pontuação
8. Tela de Game Over com opção de reiniciar
9. Efeitos sonoros opcionais (web sound)
10. Responsivo — funciona em mobile (touch) e desktop (click/space)

## Arquitetura
- `index.html` — estrutura e canvas
- `styles.css` — layout e UI
- `game.js` — engine principal (loop, física, colisões, rendering)

## Paleta de Cores (Tema Longe de Casa)
- Vermelho Aranha: #BE1E2D
- Azul Aranha: #1B3A6B
- Preto Aranha: #1A1A2E
- Dourado/Sunset: #F4A261
- Céu europeu: #87CEEB → #2C3E7A (gradiente)

## Mecânica de Jogo
- Gravidade puxa o Homem-Aranha para baixo
- Clique/Toque/Espaço = lança teia para cima (impulso vertical)
- Teia visível sobe do personagem até o topo
- Obstáculos são prédios com gaps para passar
- Velocidade aumenta gradualmente
- Colisão = Game Over

## Observações
- Sprites desenhados via Canvas API (sem assets externos)
- Animação fluida a 60fps via requestAnimationFrame
- Touch events para mobile
