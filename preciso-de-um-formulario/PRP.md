# PRP: Formulário de Consulta de CEP

## Objetivo
Criar um formulário web responsivo que consulta CEPs via API ViaCEP e preenche automaticamente os campos de endereço.

## Arquitetura
```
/
├── index.html    — Estrutura do formulário
├── styles.css    — Estilização responsiva
└── script.js     — Lógica de CEP (máscara, consulta, preenchimento)
```

## Checklist de Implementação

### Sprint 1 — Estrutura e Estilo
- [x] Criar `index.html` com formulário semântico (CEP, logradouro, número, complemento, bairro, cidade, estado)
- [x] Criar `styles.css` com design moderno e responsivo
- [x] Adicionar estados visuais (loading, sucesso, erro)

### Sprint 2 — Lógica JavaScript
- [x] Criar `script.js` com máscara de CEP (99999-999)
- [x] Implementar consulta à API ViaCEP via fetch
- [x] Preenchimento automático dos campos ao receber resposta
- [x] Tratamento de erros (CEP inválido, sem conexão)
- [x] Feedback visual durante carregamento (spinner)

## Validação
- [x] Digitar CEP válido (ex: 01001-000) → campos preenchidos automaticamente
- [x] Digitar CEP inválido → mensagem de erro clara
- [x] Layout responsivo funcionando em mobile
- [x] Campos preenchidos ficam editáveis
