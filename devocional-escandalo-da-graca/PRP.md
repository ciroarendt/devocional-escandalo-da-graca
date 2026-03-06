# PRP: Devocional 365 — "O Escândalo da Graça"

## Objetivo
Criar um aplicativo web de leitura devocional (estilo Kindle) com 365 devocionais baseados no livro "O Escândalo da Graça" de Karl Dietz, publicável na internet.

## Estado Atual
- App web completo e funcional
- 365 devocionais gerados e validados
- Interface e-reader com todas as funcionalidades

## Arquitetura Final
```
devocional365/
├── index.html          # App principal (SPA)
├── css/
│   └── styles.css      # Estilos do e-reader (tema claro/escuro)
├── js/
│   ├── app.js          # Lógica de navegação, favoritos, progresso
│   └── devotionals.js  # 365 devocionais em JSON (~550KB)
└── manifest.json       # PWA manifest
```

## Distribuição dos 365 Devocionais pelo Ano
- **Jan (31):** A Natureza de Deus — "Deus É", marcos zero, novo nascimento
- **Fev (28):** Graça — Fundamentos, escândalo, erradicação do pecado
- **Mar (31):** Graça — Perspectiva divina, suficiência, transformação
- **Abr (30):** Da Graça à Justiça — Transição entre os pilares
- **Mai (31):** Justiça de Deus — Justificação pela fé
- **Jun (30):** Justiça — Salvação como conhecimento e consciência
- **Jul (31):** Herança — Fundamentos: herança não é conquista
- **Ago (31):** Herança — Identidade de filhos, natureza divina
- **Set (30):** Glória — Natureza divina, participantes da glória
- **Out (31):** Glória — Igreja, família, chaves do Reino
- **Nov (30):** Vida no Reino — Conceitos, prioridade, comissão
- **Dez (31):** Síntese — Integração dos 4 pilares

## Sprint 1 — Geração dos Devocionais ✅
- [x] Extrair e organizar todos os temas/subtemas do livro
- [x] Gerar os devocionais de Janeiro (dias 1-31) — 31 devocionais
- [x] Gerar os devocionais de Fevereiro (dias 32-59) — 28 devocionais
- [x] Gerar os devocionais de Março (dias 60-90) — 31 devocionais
- [x] Gerar os devocionais de Abril (dias 91-120) — 30 devocionais
- [x] Gerar os devocionais de Maio (dias 121-151) — 31 devocionais
- [x] Gerar os devocionais de Junho (dias 152-181) — 30 devocionais
- [x] Gerar os devocionais de Julho (dias 182-212) — 31 devocionais
- [x] Gerar os devocionais de Agosto (dias 213-243) — 31 devocionais
- [x] Gerar os devocionais de Setembro (dias 244-273) — 30 devocionais
- [x] Gerar os devocionais de Outubro (dias 274-304) — 31 devocionais
- [x] Gerar os devocionais de Novembro (dias 305-334) — 30 devocionais
- [x] Gerar os devocionais de Dezembro (dias 335-365) — 31 devocionais

## Sprint 2 — Interface do App ✅
- [x] Criar index.html com estrutura semântica
- [x] Criar styles.css com design e-reader (tema claro/escuro)
- [x] Criar app.js com lógica de navegação e estado
- [x] Renderização do devocional com animações suaves
- [x] Implementar navegação por calendário (seletor de dia)
- [x] Implementar tema claro/escuro com toggle
- [x] Implementar progresso de leitura (localStorage)
- [x] Implementar marcação de favoritos
- [x] Implementar busca por título/tema
- [x] Responsividade mobile-first
- [x] PWA manifest para instalação
- [x] Swipe touch para navegação mobile
- [x] Slider de dias na barra inferior
- [x] Atalhos de teclado (setas, D, F, T)

## Validação ✅
- [x] Todos os 365 devocionais validados (5 parágrafos, 5+ refs cada)
- [x] Navegação funciona (anterior/próximo/calendário/slider)
- [x] Tema claro/escuro com persistência
- [x] Responsivo em mobile e desktop
- [x] Progresso salva no localStorage
- [x] Favoritos funcionam com persistência
- [x] Busca por título/tema funcional
