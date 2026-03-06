# Análise do Projeto — Scraper MCTI Lei do Bem (Lotes)

## Resumo
Aplicativo para capturar automaticamente todos os lotes (pareceres técnicos, contestações, recursos administrativos, retificações) publicados na página de Lotes da Lei do Bem do MCTI.

## Fonte dos Dados
- **URL**: https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/lei-do-bem/paginas/lotes
- **Proteção**: Site usa bot detection (Akamai/TSPD) — necessário headers de browser
- **Formato**: PDFs individuais + ZIPs com publicações anteriores

## Inventário dos Dados Encontrados

### PDFs por Ano-Base (31 PDFs relevantes)
| Ano-Base | Tipo | Lotes | Quantidade |
|----------|------|-------|------------|
| 2023 | Contestação | 1º ao 11º | 11 PDFs |
| 2022 | Contestação | 10º, 11º, 12º | 3 PDFs |
| 2021 | Recurso Administrativo | 1º ao 7º | 7 PDFs |
| 2020 | Recurso Administrativo | vários | 5 PDFs |
| 2018 | Parecer Técnico | 9º lote | 1 PDF |
| 2017 | Contestação | 4º lote | 1 PDF |

### ZIPs (publicações anteriores consolidadas)
| Ano-Base | Conteúdo | Quantidade |
|----------|----------|------------|
| 2023 | Pareceres técnicos anteriores | 1 ZIP |
| 2022 | Recurso adm + Contestação + Pareceres | 3 ZIPs |
| 2021 | Contestação anteriores | 1 ZIP |
| 2020 | Recurso adm + Pareceres anteriores | 3 ZIPs |
| 2019 | Conjunto dos lotes | 1 ZIP |
| 2018 | Conjunto dos lotes | 1 ZIP |
| 2017 | Conjunto + anteriores | 3 ZIPs |
| 2016 | Conjunto + anteriores | 2 ZIPs |
| 2015 | Conjunto + anteriores | 4 ZIPs |
| 2014 | Conjunto dos lotes | 2 ZIPs |
| 2013 | Conjunto dos lotes | 1 ZIP |

### Manuais (2 PDFs)
- Manual do Usuário - Contestação
- Manual do Usuário - Recurso Administrativo

## Decisões Técnicas
- **Linguagem**: Python 3 (disponível no ambiente)
- **HTTP**: `requests` ou `urllib` com headers de browser (contornar bot detection)
- **HTML Parsing**: `re` (regex) ou `html.parser` (stdlib) — evitar dependências externas
- **Organização**: Arquivos baixados organizados por ano-base em pastas
- **Output**: Relatório JSON com metadados de todos os arquivos + log de download

## Funcionalidades
1. Scraping da página de lotes (extração de todos os links PDF/ZIP)
2. Download automático dos arquivos organizados por ano-base
3. Geração de relatório/índice em JSON com metadados
4. Log de progresso e tratamento de erros
5. Opção de filtrar por ano-base específico
