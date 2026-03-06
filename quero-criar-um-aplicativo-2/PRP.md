# PRP: Scraper MCTI Lei do Bem — Captura de Lotes

## Objetivo
Criar um aplicativo Python que faz scraping da página de Lotes do MCTI (Lei do Bem), extrai todos os links de PDFs e ZIPs organizados por ano-base, e faz o download dos arquivos de forma estruturada.

## Estado Atual
Nenhum código existe ainda. A análise de viabilidade já foi feita: o site responde corretamente com headers de navegador e os dados estão acessíveis.

## Estado Final
Um aplicativo Python (`scraper_lotes_mcti.py`) que:
1. Acessa a página de Lotes e faz parsing do HTML
2. Extrai links de PDF/ZIP organizados por ano-base
3. Faz download dos arquivos em pastas organizadas (`downloads/2023/`, `downloads/2022/`, etc.)
4. Mostra progresso no terminal
5. Gera um relatório JSON com metadados de todos os arquivos
6. Suporta filtro por ano-base (ex: `--ano 2023`)
7. Evita re-download de arquivos já existentes

## Plano de Implementação

### Sprint 1 — Aplicativo Completo
- [ ] Criar estrutura do projeto (pasta, requirements.txt)
- [ ] Implementar módulo de scraping (parsear HTML, extrair links por ano-base)
- [ ] Implementar módulo de download (download com progresso, organização em pastas)
- [ ] Implementar CLI com argparse (filtro por ano, modo dry-run, etc.)
- [ ] Implementar geração de relatório JSON com metadados
- [ ] Implementar tratamento de erros e retry
- [ ] Testar o scraper (dry-run para listar arquivos)

## Arquivos a Criar
- `scraper_lotes_mcti.py`: Script principal com toda a lógica
- `requirements.txt`: Dependências Python

## Validação
- [ ] Executar em modo dry-run e verificar se lista todos os 48+ arquivos
- [ ] Verificar organização por ano-base
- [ ] Testar filtro por ano específico
- [ ] Confirmar que download funciona para pelo menos 1 arquivo
