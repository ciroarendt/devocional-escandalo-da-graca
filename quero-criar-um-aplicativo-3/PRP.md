# PRP: Dashboard Web — Lotes Lei do Bem (MCTI)

## Objetivo
Criar uma aplicação web com dashboard interativo que faz scraping da página de Lotes do MCTI, exibe todos os documentos (PDFs, ZIPs, 7z) organizados por ano-base, permite filtrar, buscar e baixar os arquivos diretamente.

## Current State
- Página do MCTI com ~54 arquivos espalhados sem boa organização visual
- Usuário precisa navegar manualmente e clicar em cada link
- Sem filtros, sem busca, sem visão consolidada

## Target State
- Dashboard web moderno e responsivo
- Scraping automático da página do MCTI ao carregar
- Tabela/cards organizados por ano-base (2013-2023)
- Filtros por ano-base e tipo de documento (parecer, contestação, recurso)
- Barra de busca
- Estatísticas visuais (total por ano, tipos de documento)
- Download direto dos arquivos
- Indicador de status/progresso do scraping

## Arquitetura
- **Frontend:** HTML5 + CSS3 + JavaScript vanilla (sem framework, leve e rápido)
- **Backend:** Python com Flask (API REST que faz o scraping)
- **Estilo:** Design moderno com CSS Grid/Flexbox, cores inspiradas no gov.br
- **Estrutura:**
  ```
  /
  ├── app.py              # Backend Flask + API de scraping
  ├── requirements.txt    # Dependências Python
  ├── templates/
  │   └── index.html      # Dashboard principal
  ├── static/
  │   ├── css/
  │   │   └── style.css   # Estilos do dashboard
  │   └── js/
  │       └── app.js      # Lógica do frontend
  ├── analysis.md
  └── PRP.md
  ```

## Implementation Plan

### Sprint 1 — Backend (API de Scraping)
- [x] Criar `requirements.txt` com dependências
- [x] Criar `app.py` com Flask + endpoint `/api/lotes` que faz scraping da página do MCTI
- [x] Parsear HTML e extrair: URL, nome do arquivo, ano-base, tipo (parecer/contestação/recurso), formato (PDF/ZIP/7z)
- [x] Endpoint `/api/lotes` retorna JSON estruturado
- [x] Implementar cache em memória (não re-scrape a cada request)

### Sprint 2 — Frontend (Dashboard)
- [x] Criar `templates/index.html` — estrutura do dashboard com header, stats, filtros e tabela
- [x] Criar `static/css/style.css` — design moderno, responsivo, tema com cores do gov.br
- [x] Criar `static/js/app.js` — fetch da API, renderização dinâmica, filtros e busca

### Sprint 3 — Features e Polish
- [x] Cards de estatísticas no topo (total arquivos, total por tipo, anos cobertos)
- [x] Filtro por ano-base (dropdown ou botões)
- [x] Filtro por tipo de documento (parecer, contestação, recurso, consolidado)
- [x] Busca por texto no nome do arquivo
- [x] Indicador de loading durante scraping
- [x] Responsividade mobile
- [x] Botão "Copiar Links" (copia URLs filtradas para clipboard)

## Files to Modify/Create
- `requirements.txt`: Flask, requests, beautifulsoup4
- `app.py`: Servidor Flask + scraping logic
- `templates/index.html`: Dashboard HTML
- `static/css/style.css`: Estilos
- `static/js/app.js`: Lógica frontend

## Validation
- [x] Servidor Flask inicia sem erros
- [x] `/api/lotes` retorna JSON com 52 arquivos (30 PDFs, 21 ZIPs, 1 7Z)
- [x] Dashboard carrega e exibe os dados
- [x] Filtros funcionam (ano-base, tipo, formato)
- [x] Busca funciona
- [x] Links de download apontam para URLs corretas do MCTI
- [x] Layout responsivo
- [x] Gráfico de barras por ano-base com clique para filtrar

## Resultados
- **52 documentos** capturados automaticamente do site do MCTI
- **11 anos-base** cobertos (2013 a 2023)
- **5 tipos** de documentos classificados: Contestação (17), Recurso Administrativo (14), Parecer Técnico (12), Consolidado (5), Manual (2), Outro (2)
- **3 formatos**: PDF (30), ZIP (21), 7Z (1)
