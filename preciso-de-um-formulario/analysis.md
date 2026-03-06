# Análise do Projeto — Formulário de CEP

## Objetivo
Criar um formulário web que consulta CEPs brasileiros e preenche automaticamente os campos de endereço.

## Funcionalidades
1. Campo de input para CEP com máscara (99999-999)
2. Consulta automática à API ViaCEP ao completar o CEP
3. Preenchimento automático: logradouro, bairro, cidade, estado
4. Campos editáveis para complemento e número
5. Validação visual (CEP válido/inválido)
6. Design responsivo (mobile-friendly)

## Tech Stack
- **HTML5** — estrutura semântica do formulário
- **CSS3** — estilização responsiva (sem framework, leve)
- **JavaScript Vanilla** — lógica de consulta e preenchimento
- **API ViaCEP** — `https://viacep.com.br/ws/{cep}/json/` (gratuita, sem autenticação)

## Arquitetura
- Single page (index.html + styles.css + script.js)
- Fetch API para consultar o ViaCEP
- Sem dependências externas

## Constraints
- Funcionar em qualquer navegador moderno
- Sem necessidade de backend
- Leve e rápido
