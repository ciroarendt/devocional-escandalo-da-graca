# PRP: Scraper MCTI Lei do Bem — Captura de Lotes

## Objetivo
Criar um aplicativo Python que acessa a página de Lotes da Lei do Bem no site do MCTI, extrai todos os links de PDFs e ZIPs, e faz o download organizado por ano-base.

## Estado Atual
Aplicativo funcional e testado.

## Estado Alvo
Um script Python funcional que:
- Acessa a página do MCTI e extrai todos os links de arquivos
- Baixa PDFs e ZIPs organizados em pastas por ano-base
- Gera um relatório JSON com índice de todos os arquivos
- Mostra progresso no terminal
- Permite filtrar por ano-base

## Arquitetura

```
mcti-lei-do-bem-scraper/
├── scraper.py           # Script principal (CLI)
├── downloads/           # Pasta criada automaticamente
│   ├── manuais/         # Manuais do usuário
│   ├── 2023/            # PDFs e ZIPs do ano-base 2023
│   ├── 2022/
│   ├── ...
│   └── 2013/
└── relatorio.json       # Índice gerado com metadados
```

## Plano de Implementação

### Sprint 1 — Aplicativo Completo
- [x] 1. Criar `scraper.py` com classe principal
- [x] 2. Implementar método de fetch da página com headers anti-bot
- [x] 3. Implementar parser de links (extração de PDFs e ZIPs)
- [x] 4. Implementar classificação por ano-base (regex no URL)
- [x] 5. Implementar download de arquivos com barra de progresso
- [x] 6. Implementar organização em pastas por ano-base
- [x] 7. Implementar geração de relatório JSON
- [x] 8. Implementar CLI com argparse (filtro por ano, --list, etc.)
- [x] 9. Testar execução: listar todos os arquivos disponíveis (51 arquivos encontrados)
- [x] 10. Testar download de um arquivo para validar o fluxo (PDF 743KB baixado com sucesso)

## Validação
- [x] Comando `python3 scraper.py --list` lista 51 arquivos
- [x] Comando `python3 scraper.py --ano 2023` filtra 12 arquivos do ano-base 2023
- [x] Download de arquivo completa com sucesso (PDF válido, header %PDF-)
- [x] Relatório JSON gerado corretamente em downloads/relatorio.json
