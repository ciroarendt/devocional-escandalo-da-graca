# Análise do Projeto — Scraper MCTI Lei do Bem (Lotes)

## Objetivo
Criar um aplicativo que acessa a página de Lotes do MCTI (Lei do Bem) e captura automaticamente todos os PDFs e ZIPs disponíveis, organizados por ano-base.

## Fonte de Dados
- **URL**: https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/lei-do-bem/paginas/lotes
- **Proteção**: O site usa proteção anti-bot (TSPD/Imperva), mas responde corretamente com headers de navegador via `requests`
- **Estrutura**: Página HTML com tabelas organizadas por ano-base (2013 a 2023)

## Dados Encontrados na Página

### Ano-Base 2023 (11 PDFs + 1 ZIP)
- 11 lotes de Parecer Técnico (contestação) — publicados entre Nov/2025 e Fev/2026
- 1 ZIP com publicações anteriores

### Ano-Base 2022 (3 PDFs + 3 ZIPs)
- 3 lotes de Parecer Técnico (contestação) — publicados Jan/2026
- ZIPs: recurso administrativo, contestação e pareceres anteriores

### Ano-Base 2021 (7 PDFs + 2 ZIPs)
- 7 lotes de Parecer Técnico (Recurso Administrativo)
- ZIPs: contestação anteriores e pareceres anteriores

### Ano-Base 2020 (5 PDFs + 3 ZIPs)
- 5 lotes de Parecer Técnico (Recurso Administrativo)
- ZIPs: recurso adm, contestação e pareceres anteriores

### Anos 2013-2019 (apenas ZIPs consolidados)
- Cada ano tem 1-2 ZIPs com lotes consolidados

## Total
- **~32 PDFs** relevantes (Lei do Bem)
- **~16 ZIPs** com publicações anteriores
- **Tamanho estimado**: ~50-80 MB total

## Tech Stack Recomendado
- **Python 3** (já disponível no ambiente)
- **requests** + **BeautifulSoup4** (já instalados)
- **Estrutura**: Script CLI organizado que faz scraping + download

## Observações
- Links de PDFs genéricos do site (editais, glossário ANPD) devem ser filtrados — só queremos os da Lei do Bem
- Alguns links apontam para `antigo.mctic.gov.br` (domínio legado)
- Os textos dos links são apenas "Aqui", contexto vem da estrutura da tabela
