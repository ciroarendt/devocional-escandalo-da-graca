# PRP: Sistema de Análise de Grupos de Consórcio ADEMICON

## Objetivo
Sistema web para consultores ADEMICON analisarem e compararem grupos de consórcio, com dados de lances, sorteios, parcelas e configuração de contemplação, para sugerir os melhores grupos por perfil de cliente.

## Estado Atual
- [x] 56 grupos via API simulador (crédito, parcela, taxa, participantes, tipo parcela)
- [x] 240 grupos com configuração de lances (LF, LL, LI, LM, LS)
- [x] Histórico de assembleias: 49 meses imóveis + 37 meses veículos (MKT API)
- [x] 528 datas de sorteio + 368 resultados de loteria (CRM API)
- [x] 92 extrações detalhadas com categorias A-F (CRM API)
- [x] Análise de proximidade e tipos de lance recomendados (CRM API)
- [x] 45 cotas do consultor com dados detalhados
- [x] Calendário de assembleias futuras (5 produtos)
- [x] Scripts de coleta funcionais
- [x] Sistema web para consultores

## Estado Alvo
- Sistema web profissional com tema ADEMICON
- Dashboard com visão geral dos grupos por segmento
- Filtros por perfil do cliente (crédito, parcela, lance, urgência)
- Ranking inteligente dos melhores grupos
- Detalhes por grupo (lances permitidos, tipo parcela, calendário)
- Upload de histograma para dados de contemplação por lance (excl. cancelados)
- Comparativo entre grupos

## Plano de Implementação

### Sprint 1 — Sistema Web Completo
- [x] 1. `dados.js` — Consolidar todos os JSONs em dados embutidos (56 grupos, 5 calendários, bids config)
- [x] 2. `index.html` — Estrutura da página responsiva (5 views: dashboard, buscar, comparar, calendário, histograma)
- [x] 3. `styles.css` — Estilização ADEMICON (vermelho/cinza escuro, responsivo mobile)
- [x] 4. `app.js` — Lógica principal:
  - [x] 4.1 Dashboard com resumo por segmento (cards de stats + tabela completa)
  - [x] 4.2 Seleção de segmento (Imóveis, Veículos, Motos, Serviços, OBM) com tabs
  - [x] 4.3 Filtros de perfil:
    - Valor de crédito desejado
    - Parcela máxima mensal
    - Tipo de lance preferido (Fixo, Livre, Limitado, Fidelidade)
    - Urgência (prazo para contemplação)
    - Índice de correção (INCC, INPC, IPCA)
  - [x] 4.4 Algoritmo de ranking/score (0-100 baseado em crédito, parcela, lances, urgência, taxas)
  - [x] 4.5 Cards de resultado com score visual (círculo colorido verde/laranja/vermelho)
  - [x] 4.6 Detalhes do grupo (modal: lances, taxas, parcela, plano venda, participantes)
  - [x] 4.7 Comparativo lado a lado (até 3 grupos com destaque de melhor valor)
  - [x] 4.8 Upload de histograma (CSV + colar Excel, exclui cancelados)
  - [x] 4.9 Calendário de assembleias (5 produtos)

## Arquivos
- `index.html`: Página principal
- `styles.css`: Estilos
- `app.js`: Lógica
- `dados.js`: Dados consolidados

## Validação
- [x] Exibe todos os 56 grupos com dados completos
- [x] Filtros funcionam por segmento, crédito, parcela, lance, urgência, correção
- [x] Ranking ordena por score inteligente (0-100)
- [x] Detalhes mostram lances permitidos (LF/LL/LI/LM/LS) com config completa
- [x] Upload de histograma parseia CSV e dados colados, exclui cancelados
- [x] Responsivo em mobile
- [x] Calendário de assembleias para 5 produtos
