# PRP: Webapp — MCTI Lei do Bem Scraper

## Objetivo
Transformar o scraper CLI em um webapp interativo com interface visual para listar, filtrar e baixar os lotes da Lei do Bem.

## Estado Atual
Scraper CLI funcional (`scraper.py`) que extrai 51 arquivos do MCTI.

## Estado Alvo
Webapp HTML/CSS/JS com backend Python (Flask-like com http.server) que:
- Mostra dashboard com todos os lotes organizados por ano
- Permite filtrar por ano-base e tipo de documento
- Permite download individual e em lote
- Visual moderno e responsivo

## Arquitetura
```
├── app.py              # Servidor web Python (http.server + API)
├── scraper.py          # Módulo scraper (já existe)
├── templates/
│   └── index.html      # Interface principal (SPA)
├── static/
│   ├── style.css       # Estilos
│   └── app.js          # Lógica frontend
├── downloads/          # Arquivos baixados
└── relatorio.json      # Cache dos metadados
```

## Plano de Implementação

### Sprint 1 — Webapp Completo
- [ ] 1. Criar `app.py` — servidor HTTP com API REST
  - GET `/` → serve index.html
  - GET `/api/lotes` → retorna JSON com todos os lotes
  - GET `/api/lotes?ano=2023` → filtra por ano
  - POST `/api/download` → inicia download de arquivo(s)
  - GET `/api/status` → status dos downloads em andamento
  - GET `/static/*` → serve arquivos estáticos
- [ ] 2. Criar `templates/index.html` — página principal
- [ ] 3. Criar `static/style.css` — design moderno gov.br-inspired
- [ ] 4. Criar `static/app.js` — lógica do frontend
- [ ] 5. Refatorar `scraper.py` para funcionar como módulo importável
- [ ] 6. Testar o webapp rodando localmente

## Validação
- [ ] Servidor inicia sem erros
- [ ] API `/api/lotes` retorna os 51 arquivos em JSON
- [ ] Interface renderiza corretamente com filtros funcionando
- [ ] Download de arquivo funciona via interface
