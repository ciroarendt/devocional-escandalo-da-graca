# Project Analysis — Scraper de Lotes Lei do Bem (MCTI)

## Objetivo
Aplicativo que visita a página de Lotes do MCTI (Lei do Bem) e captura todos os documentos disponíveis (PDFs, ZIPs, 7z) — pareceres técnicos, contestações, recursos administrativos e retificações organizados por ano-base.

## Fonte de Dados
- **URL Principal:** https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/lei-do-bem/paginas/lotes
- **Proteção:** O site usa WAF que requer headers HTTP específicos (User-Agent, Accept, etc.)
- **Formato:** Página HTML com links diretos para PDFs e ZIPs

## Dados Disponíveis (mapeados)

### Ano-Base 2023 (11 PDFs + 1 ZIP)
- 11 lotes de parecer técnico - contestação (1º ao 11º lote)
- 1 ZIP com publicações anteriores

### Ano-Base 2022 (3 PDFs + 3 ZIPs)
- 3 lotes de parecer técnico - contestação (10º ao 12º)
- ZIPs: recurso administrativo, contestação e pareceres técnicos anteriores

### Ano-Base 2021 (7 PDFs + 1 ZIP + 1 7z)
- 7 lotes de recurso administrativo
- ZIP com contestações anteriores
- 7z com pareceres técnicos anteriores

### Ano-Base 2020 (5 PDFs + 3 ZIPs)
- 5 lotes de recurso administrativo
- ZIPs: recurso administrativo, contestação e pareceres técnicos anteriores

### Ano-Base 2019 (1 ZIP)
- Conjunto dos lotes do ano-base

### Ano-Base 2018 (1 ZIP + 1 PDF)
- Conjunto dos lotes + 9º lote avulso

### Ano-Base 2017 (1 PDF + 2 ZIPs + 2 mirrors antigos)
- Conjunto dos lotes + publicações anteriores

### Ano-Base 2016 (2 ZIPs)
- Conjunto dos lotes + publicações anteriores

### Ano-Base 2015 (2 ZIPs + 2 mirrors antigos)
- Conjunto dos lotes + publicações anteriores

### Ano-Base 2014 (1 ZIP + 1 mirror antigo)
- Conjunto dos lotes

### Ano-Base 2013 (1 ZIP + 1 mirror antigo)
- Conjunto dos lotes

## Total: ~54 arquivos (PDFs, ZIPs, 7z)

## Desafios Técnicos
1. **WAF/Proteção:** Requer headers HTTP completos para não ser bloqueado (403)
2. **Nomes inconsistentes:** URLs seguem padrões diferentes por ano
3. **Mirrors:** Alguns links apontam para `antigo.mctic.gov.br` (site antigo)
4. **Formatos mistos:** PDF, ZIP e 7z
5. **Tamanho dos arquivos:** ZIPs podem ser grandes (vários MB)

## Tech Stack Recomendada
- **Python 3** com `requests` (ou `httpx`) + `BeautifulSoup4`
- **Organização:** Downloads organizados por ano-base em pastas
- **CLI:** Interface de linha de comando com progresso
- **Opção de filtro:** Por ano-base, tipo de documento

## Observações
- Todos os links foram verificados como acessíveis via curl com headers adequados
- A página é relativamente estável (conteúdo institucional)
- Novos lotes são adicionados periodicamente (último: jan/fev 2026 para AB 2023)
