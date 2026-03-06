# Prompt para Workspace codrsync — Resposta Estratégica à Inventeer

Cole este prompt no seu workspace codrsync:

---

Crie uma apresentação interativa de resposta estratégica como single-page HTML. Esta NÃO é um pitch — é uma **demonstração de valor** que guia o espectador por um "caminho neural" até a conclusão natural de que o codrsync tem valor real e mensurável.

## Conceito: "Experience the Product"

A apresentação tem 3 atos:
- **Ato 1 (Slides 1-4)**: SENTIR — Mini-demos interativas que mostram o que o codrsync faz
- **Ato 2 (Slides 5-8)**: ENTENDER — O valor concreto disso para a Inventeer
- **Ato 3 (Slides 9-12)**: DECIDIR — A proposta revisada (cliente enterprise + equity minoritário)

O tom é: confiante, demonstrativo, sem desespero. "Estou mostrando o que existe. Vocês decidem se querem fazer parte."

## Design

- Estilo: Dark premium (fundo #0a0a0f, acentos em cyan #00d4ff e branco)
- Tipografia: Inter (Google Fonts), clean e moderna
- Layout: Fullscreen slides com scroll-snap vertical
- Animações: Fade-in suave nos elementos (Intersection Observer)
- Navegação: Dots laterais + setas teclado + swipe mobile
- Barra de progresso no topo
- Responsivo desktop + mobile
- NO frameworks — HTML/CSS/JS puro
- Tudo em 1 arquivo index.html

## Slides (12 total)

### ═══════════════════════════════════
### ATO 1: SENTIR — "O que o codrsync faz"
### ═══════════════════════════════════

### Slide 1: Capa — "Don't take our word for it. Experience it."

- Logo "codrsync" em gradiente cyan-to-white
- Subtítulo: "Esta apresentação foi criada dentro de um workspace codrsync."
- Texto menor: "Tudo que você vai ver aqui — o design, as animações, as demos — foi gerado por IA orquestrada pelo codrsync em minutos, não semanas."
- Badge pulsante: "LIVE DEMO — você está dentro do produto agora"
- Seta animada para baixo convidando a scrollar
- Animação: Logo pulsa, texto fade-in sequencial

### Slide 2: Demo 1 — "Cloud Workspaces: Do zero ao deploy em 60 segundos"

- Título: "Isso aqui? É um workspace codrsync rodando agora."
- Terminal fake CSS (fundo preto, texto verde monospace) mostrando uma simulação animada de:
  ```
  $ codrsync workspace create --template react-app
  ✓ Container criado (2.1s)
  ✓ Dependencies instaladas (8.3s)
  ✓ Preview disponível em https://seu-projeto.ws.codrsync.dev
  ✓ Claude Code conectado ao workspace
  ✓ Contexto do projeto carregado automaticamente

  Workspace pronto. Tempo total: 14.2s
  ```
- Cada linha aparece com delay de 800ms, simulando execução real
- Ao lado: 3 cards com métricas
  - "Container ARM isolado" (com ícone de shield)
  - "Preview público instantâneo" (com ícone de link)
  - "IA já conectada com contexto" (com ícone de brain)
- Texto de destaque: "Seus 18+ engenheiros poderiam ter workspaces dedicados amanhã."
- Nota sutil: "Cursor, Bolt, Lovable: nenhum oferece workspaces isolados com preview ao vivo."

### Slide 3: Demo 2 — "Context Engineering: A IA que lembra"

- Título: "O que acontece quando a IA tem memória?"
- Layout split vertical:
  - **Coluna esquerda "SEM codrsync"** (fundo cinza escuro, tom apagado):
    - Diálogo fake mostrando:
      ```
      Sessão 1: "Crie um componente de login"
      → IA cria componente

      Sessão 2: "Adicione validação ao login"
      → IA: "Que componente de login? Pode me mostrar o código?"
      → Dev: cola 200 linhas de código
      → IA: "Ah ok, entendi" (gastou 5 min de contexto)

      Sessão 3: "O login não funciona no mobile"
      → IA: "Pode me explicar a arquitetura do projeto?"
      → Dev: (...morre por dentro)
      ```
    - Label: "Isso acontece 20x por dia com qualquer dev"
  - **Coluna direita "COM codrsync"** (fundo com borda cyan, destaque):
    - Diálogo fake mostrando:
      ```
      Sessão 1: "Crie um componente de login"
      → IA cria componente
      → [Context salvo automaticamente]

      Sessão 2: "Adicione validação ao login"
      → IA: "Baseado no LoginForm.tsx que criamos ontem,
        vou adicionar Zod validation com os patterns
        que este projeto usa..."

      Sessão 3: "O login não funciona no mobile"
      → IA: "Vi no context que o LoginForm usa flex-col.
        O problema é o viewport height no Safari iOS.
        Corrigindo..."
      ```
    - Label: "Context Engineering = a IA trabalha com você, não para você"
- Animação: Coluna esquerda aparece primeiro (meio segundo), depois a direita "ilumina" com borda cyan animada
- Texto de destaque: "Cada engenheiro da Inventeer economiza 1-2h/dia. Com 18+ devs, são 25-36 horas/dia recuperadas."

### Slide 4: Demo 3 — "BYOK: Traga sua própria IA"

- Título: "Não apostamos em um provider. Orquestramos todos."
- Grid visual 2x3 de cards de providers:
  - Claude (Anthropic) — badge "Context Engineering nativo"
  - GPT-4o (OpenAI) — badge "Mais popular"
  - Gemini (Google) — badge "Grátis para prototipagem"
  - Grok (xAI) — badge "Alta velocidade"
  - Ollama (Local) — badge "100% privado, HIPAA ready"
  - Mais por vir... — badge "Extensível"
- Cada card tem toggle fake ON/OFF (CSS only) que mostra/oculta detalhes ao clicar
- Abaixo dos cards: "Com BYOK, seus clientes enterprise escolhem o provider. Compliance de dados fica com eles."
- Destaque: "Concorrentes forçam lock-in em um provider. codrsync é agnóstico."
- Nota: "A Inventeer já usa Claude Code. Imagina Claude + GPT + Ollama local, tudo orquestrado."

### ═══════════════════════════════════
### ATO 2: ENTENDER — "O que isso vale para vocês"
### ═══════════════════════════════════

### Slide 5: O Cálculo Interno — "ROI para a Inventeer como usuária"

- Título: "Antes de falar de negócio, vamos falar de ROI interno"
- Calculadora interativa CSS/JS (sem backend):
  - Slider: "Quantos engenheiros?" (range 5-50, default 18)
  - Slider: "Horas economizadas por dev/dia?" (range 0.5-3, default 1.5)
  - Slider: "Custo hora do engenheiro (USD)?" (range 50-200, default 100)
  - Output calculado em tempo real:
    - "Horas recuperadas por mês: {devs × horas × 22}"
    - "Valor recuperado por mês: ${horas × custo_hora}"
    - "Valor recuperado por ano: ${mensal × 12}"
  - Com 18 devs, 1.5h/dia, $100/h = $59.400/mês = $712.800/ano
- Texto: "Mesmo que a economia real seja metade disso, são $356K/ano em produtividade."
- Animação: Números atualizam em tempo real conforme os sliders movem
- Abaixo: "E isso é só o uso interno. Imagina oferecer isso para cada cliente da Inventeer."

### Slide 6: O Mercado — "O que a Inventeer pode vender"

- Título: "Consultoria de excelência + Produto SaaS = Enterprise powerhouse"
- Diagrama visual de evolução (seta grande da esquerda pra direita):
  - **Esquerda "A força da Inventeer hoje"**:
    - "Expertise reconhecida em 5 países"
    - "18+ engenheiros de alto nível"
    - "Relacionamentos enterprise de confiança"
    - "Compliance e segurança como DNA"
  - **Direita "Com codrsync no portfólio"**:
    - "Tudo acima + plataforma SaaS como upsell natural"
    - "Margem SaaS: 80%+ sobre as licenças"
    - "Receita recorrente: clientes pagam mês a mês, não por projeto"
    - "Diferencial único: a única consultoria com AI dev platform própria"
- Abaixo: 3 cards de modelos de receita:
  - "Ferramenta interna" — Economia de $350K+/ano (já calculado)
  - "White-label para clientes" — Vender codrsync branded como "Inventeer DevPlatform"
  - "Upsell em contratos" — Todo contrato de consulting inclui acesso à plataforma ($500-2K/mês extra)
- Texto: "A Inventeer não precisa ser dona do codrsync para ganhar dinheiro com ele."

### Slide 7: Comparativo de Deals — "Vamos comparar as propostas"

- Título: "Transparência total: as propostas lado a lado"
- Tabela comparativa com 3 colunas:

  | Aspecto | Contraproposta Inventeer | Nossa Nova Proposta |
  |---|---|---|
  | Equity Ciro | 10-30% (vesting 4 anos) | Ciro mantém 85-90% |
  | Equity Inventeer | 70-90% | 10-15% |
  | IP | Transferido sem reversão | Licença enterprise perpétua |
  | Liderança | Maycon decide tudo | Ciro lidera produto, Inventeer lidera vendas |
  | Custo Inventeer | Salary + recursos (indefinido) | $50K investimento + $3-5K/mês cliente |
  | Risco Inventeer | Alto (opera produto SaaS + consultoria ao mesmo tempo) | Baixo (foca no que faz melhor: enterprise sales) |
  | Upside Inventeer | Dona de um produto, mas precisa escalar 2 negócios simultâneos | 10-15% de um SaaS + receita de revenda, sem desviar foco da consultoria |
  | Se não funcionar | IP na empresa, mas time dividido entre 2 operações distintas | Cancela assinatura, investimento protegido por equity, zero distração |

- Coluna "Contraproposta Inventeer" com fundo levemente vermelho/rosado
- Coluna "Nossa Nova Proposta" com fundo levemente verde
- Texto abaixo: "A pergunta certa não é 'quem é dono'. É 'como cada lado multiplica o que já faz de melhor'."

### Slide 8: Case Study — "O que $50K de investimento compra"

- Título: "O investimento mais eficiente que a Inventeer pode fazer"
- Timeline visual horizontal com 4 marcos:
  - **Mês 1-2**: "Onboarding"
    - Workspaces para todo o time Inventeer
    - Treinamento Context Engineering
    - Integração com stack existente
  - **Mês 3-6**: "Valor Interno"
    - 18+ devs usando diariamente
    - Economia mensurável de produtividade
    - Case study real para prospects
  - **Mês 7-12**: "Valor Externo"
    - Primeiro cliente enterprise via canal Inventeer
    - White-label "Inventeer DevPlatform"
    - Revenue share sobre clientes indicados
  - **Ano 2+**: "Escala"
    - 10-15% de equity valorizado
    - Revenue share recorrente
    - Opção de aumentar participação em rodada futura
- Abaixo: comparativo de investimento
  - "$50K compra 10-15% do codrsync — valuation de $500K"
  - "Para contexto: startups de dev tools pre-revenue com produto funcional captam seed rounds de $500K-$2M com valuation de $3-5M"
  - "A Inventeer entra no melhor momento possível: preço de amigo, acesso privilegiado, ROI interno já no mês 3"

### ═══════════════════════════════════
### ATO 3: DECIDIR — "A proposta revisada"
### ═══════════════════════════════════

### Slide 9: A Proposta — "Parceria inteligente, não sociedade forçada"

- Título: "Uma proposta onde todos ganham mais com menos risco"
- Layout de 2 cards grandes lado a lado:

  **Card 1: "Investimento + Equity"**
  - Investimento: USD $50.000
  - Equity: 10% da codrsync (valuation implícito: $500K)
  - Tipo: SAFE ou equity direto
  - Anti-dilution: Pro-rata em rodadas futuras
  - Board observer seat: 1 cadeira (voz, sem voto de controle)

  **Card 2: "Contrato Enterprise"**
  - Licença: Ilimitada para uso interno Inventeer
  - Workspaces: Até 25 simultâneos
  - Preço: USD $3.000-5.000/mês
  - Suporte: Dedicado, SLA 4h
  - White-label: Direito de revenda com revenue share (20-30% para Inventeer)
  - Duração: 12 meses, renovação automática

- Badge central entre os cards: "Cada lado faz o que faz de melhor. Sem distrações."

### Slide 10: Quem Ganha O Quê — "O upside de cada lado"

- Título: "Projeção de ganhos em 24 meses"
- Split layout:

  **Lado Inventeer:**
  - Economia interna: $350K-700K/ano em produtividade
  - Receita de revenda: 20-30% do MRR de clientes indicados
  - Equity: 10% de um SaaS com meta de $500K+ ARR
  - Valor projetado do equity (ano 2): $50K → $150-250K (3-5x)
  - Diferencial competitivo: única consultoria com AI dev platform própria

  **Lado Ciro:**
  - Receita garantida: $3-5K/mês (cliente enterprise)
  - Capital: $50K para escalar (infra, marketing, compliance)
  - Canal de distribuição: acesso a clientes enterprise da Inventeer
  - Controle: mantém liderança de produto e 85-90% de equity
  - Liberdade: pode buscar outros investidores e clientes independentemente

- Texto: "O modelo ideal é onde cada lado acelera o outro: a Inventeer abre portas enterprise que levariam anos para o codrsync alcançar sozinho, e o codrsync dá à Inventeer um produto SaaS sem precisar desviar o time de engenharia da operação principal."

### Slide 11: Próximos Passos — "Simples e direto"

- 4 steps verticais com timeline visual:
  1. **Esta semana**: Alinhamento sobre o novo modelo (call de 1h)
  2. **Semana 2**: Onboarding do time Inventeer como usuários beta
     - "Melhor due diligence: usar o produto"
  3. **Semana 3-4**: Formalização: contrato enterprise + SAFE/equity
  4. **Mês 2**: Primeiro cliente externo via canal Inventeer
- CTA: "O próximo passo não é assinar um contrato. É experimentar o produto."

### Slide 12: Encerramento

- Fundo com gradiente sutil
- Texto grande centralizado: "O melhor negócio é aquele onde ninguém precisa perder para o outro ganhar."
- Logo codrsync
- Contato: ciro@ciroarendt.com | codrsync.dev
- Texto menor: "Esta apresentação foi criada em um workspace codrsync em menos de 30 minutos. Imagine o que seu time pode fazer."
- Badge: "Confidencial — Fevereiro 2026"
- Animação: Texto com typewriter effect

## Regras técnicas
- Tudo em 1 arquivo index.html (inline CSS e JS)
- Scroll-snap-type: y mandatory
- Intersection Observer para animações de entrada
- Keyboard navigation (ArrowUp/Down, Page Up/Down)
- Touch swipe para mobile
- Barra de progresso fixa no topo
- Contador "Slide X de 12" no canto inferior
- Print-friendly: @media print com layout vertical
- Performance: Nenhuma dependência externa além de Google Fonts
- Os sliders da calculadora (Slide 5) devem funcionar com JS puro — cálculo em tempo real
- Os toggles de provider (Slide 4) devem funcionar com CSS :checked hack ou JS simples
- Terminal animado (Slide 2) com setInterval e delays progressivos

## Tom de escrita
- Confiante mas não arrogante
- Demonstrativo, não argumentativo — "veja" em vez de "acredite"
- Dados concretos, não promessas vagas
- Respeitoso com a Inventeer — reconhecer o valor deles sem diminuir o próprio
- Zero desespero — transmitir que o codrsync tem futuro com ou sem essa parceria
