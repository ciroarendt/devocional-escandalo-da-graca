# Análise do Projeto — Sistema de Análise de Grupos ADEMICON

## Objetivo
Criar um sistema web que analisa grupos de consórcio da ADEMICON para ajudar consultores a encontrar o melhor grupo para o perfil de cada cliente.

## Fontes de Dados Coletadas

### 1. API do Simulador (`api-simulador.ademicon.com.br`) — PÚBLICA
Dados detalhados de **56 grupos com cotas disponíveis**:

| Segmento | Grupos | Crédito Min | Crédito Max | Parcela Min | Parcela Max |
|----------|--------|-------------|-------------|-------------|-------------|
| Imóveis | 44 | R$ 80.000 | R$ 1.087.583 | R$ 454 | R$ 6.654 |
| Veículos | 7 | R$ 40.000 | R$ 251.450 | R$ 603 | R$ 3.383 |
| Motos | 1 | R$ 15.000 | R$ 31.254 | — | — |
| Serviços | 3 | R$ 15.055 | R$ 33.382 | — | — |
| Outros Bens Móveis | 1 | R$ 102.180 | R$ 204.360 | — | — |
| **TOTAL** | **56** | | | | |

Dados por grupo: crédito, parcela (mensal/reduzida), meses restantes, taxa admin, seguro, fundo reserva, índice correção, status, participantes, plano de venda (tipo de parcela).

### 2. API MKT - Histórico de Assembleias (`api.mktademicon.com.br`) — PÚBLICA
- **Imóveis**: 49 meses (Jan/2022 - Jan/2026)
- **Veículos**: 37 meses (Fev/2023 - Fev/2026)
- Dados: números sorteados, participantes, datas

### 3. CRM Consultor API (`crm-consultor.ademicon.com.br`) — AUTENTICADA (AVA PRO)
- **528 datas de sorteio** (desde 2008)
- **368 resultados de loteria** completos
- **33 extrações de imóveis** + **59 extrações de veículos** (2024-2026)
- **Categorias de grupos** (A-F) com participantes por faixa
- **Análise de proximidade** das cotas ao sorteio com tipos de lance recomendados
- **45 cotas** do consultor com dados detalhados

### 4. Configuração de Lances (CRM API) — **240 grupos**
Modalidades de lance por grupo:
- **Lance Fixo (LF)**: habilitado em 240 grupos
- **Lance Livre (LL)**: habilitado em 237 grupos
- **Lance Fidelidade (LI)**: habilitado em 70 grupos
- **Lance Limitado (LM)**: habilitado em 93 grupos
- **Segundo Lance Fixo (LS)**: habilitado em 119 grupos
- Inclui: percentual máximo de lance embutido, tipo de oferta (PE=percentual/PC=parcelas), regra

### 5. Calendário de Assembleias Futuras (API Simulador)
- **Produto 101** (Imóveis): 11 assembleias, 72 grupos
- **Produto 102** (Veículos): 10 assembleias, 4 grupos
- **Produto 105** (Veículos/Pesados): 10 assembleias, 4 grupos
- **Produto 106** (Serviços): 11 assembleias, 4 grupos
- **Produto 109** (OBM): 10 assembleias, 1 grupo

### Cobertura Total
- **124 grupos de imóveis** identificados nas extrações (6 categorias: A-F)
- **126 grupos de veículos** identificados nas extrações (5 categorias: A-E)
- **240 grupos** com configuração de lances

## Tipos de Parcela (salesPlanName) — CORREÇÃO
O `salesPlanName` indica o **tipo de parcela**, NÃO o tipo de lance:
- **Diluído**: parcela reduzida que cresce gradativamente (100% ou 50%)
- **Reduzido com Furo**: parcela menor por X meses, depois sobe
- **Linear**: parcela fixa

## Tipos de Lance (bids/config)
Cada grupo permite combinações diferentes:
- **Lance Fixo (LF)**: valor fixo predeterminado
- **Lance Livre (LL)**: qualquer valor acima do mínimo
- **Lance Fidelidade (LI)**: com base em fidelidade/tempo
- **Lance Limitado (LM)**: com teto máximo
- **Segundo Lance Fixo (LS)**: segunda opção de lance fixo

## Funcionalidade de Upload de Histograma
O sistema terá upload de histograma (tabela ADEMICON) para importar dados de contemplação por lance, excluindo lances cancelados.

## Tech Stack
- **Frontend**: HTML + CSS + JavaScript vanilla
- **Dados**: JSON embutido + upload de histograma
- **Sem backend**: Roda no navegador
- **Responsivo**: Mobile-first

## Arquivos de Dados
- `dados_grupos.json` — 56 grupos (API simulador)
- `dados_assembleias.json` — Histórico assembleias + calendário (API MKT)
- `dados_crm.json` — Draw dates, lottery results, extractions, analyses, wallets (CRM API)
- `dados_bids_config.json` — Configuração de lances por grupo (CRM API)
