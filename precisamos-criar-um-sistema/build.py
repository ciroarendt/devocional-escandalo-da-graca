"""Build script: combines CSS, JS and data into a single self-contained HTML file."""

# Read all parts
with open('/home/dev/workspace/precisamos-criar-um-sistema/styles.css') as f:
    css = f.read()

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados.js') as f:
    dados_js = f.read()

with open('/home/dev/workspace/precisamos-criar-um-sistema/app.js') as f:
    app_js = f.read()

# ADEMICON logo SVG (red A mark)
ademicon_logo_svg = '''<svg viewBox="0 0 140 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="32" height="32" rx="6" fill="#EE3124"/>
  <path d="M16 6L8 26h4l1.5-4h5l1.5 4h4L16 6zm-1.2 12L16 13l1.2 5h-2.4z" fill="white"/>
  <text x="40" y="22" font-family="Arial,Helvetica,sans-serif" font-size="16" font-weight="800" fill="white">ADEMICON</text>
</svg>'''

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADEMICON — Analise de Grupos</title>
    <style>
{css}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-inner">
            <div class="logo">
                {ademicon_logo_svg}
                <span class="logo-text"><small>Analise de Grupos</small></span>
            </div>
            <nav class="nav">
                <button class="nav-btn active" data-view="dashboard">Dashboard</button>
                <button class="nav-btn" data-view="buscar">Buscar Grupo</button>
                <button class="nav-btn" data-view="comparar">Comparar</button>
                <button class="nav-btn" data-view="calendario">Calendario</button>
                <button class="nav-btn" data-view="histograma">Histograma</button>
            </nav>
            <button class="menu-toggle" aria-label="Menu">&#9776;</button>
        </div>
    </header>

    <main class="main">
        <!-- DASHBOARD -->
        <section id="view-dashboard" class="view active">
            <h1 class="view-title">Visao Geral</h1>
            <div class="stats-grid" id="stats-grid"></div>
            <div class="section-card">
                <h2>Todos os Grupos por Segmento</h2>
                <div class="segment-tabs" id="segment-tabs"></div>
                <div class="groups-table-wrap">
                    <table class="groups-table" id="dashboard-table">
                        <thead>
                            <tr>
                                <th>Grupo</th>
                                <th>Credito</th>
                                <th>Parcela</th>
                                <th>Taxa Adm</th>
                                <th>Meses Rest.</th>
                                <th>Participantes</th>
                                <th>Lances</th>
                                <th>Tipo Parcela</th>
                                <th>Status</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody id="dashboard-tbody"></tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- BUSCAR GRUPO -->
        <section id="view-buscar" class="view">
            <h1 class="view-title">Encontre o Melhor Grupo</h1>
            <div class="filters-card">
                <div class="filters-grid">
                    <div class="filter-group">
                        <label>Segmento</label>
                        <select id="filter-segment">
                            <option value="">Todos</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Credito desejado (R$)</label>
                        <input type="number" id="filter-credit" placeholder="Ex: 300000">
                    </div>
                    <div class="filter-group">
                        <label>Parcela maxima (R$)</label>
                        <input type="number" id="filter-installment" placeholder="Ex: 2000">
                    </div>
                    <div class="filter-group">
                        <label>Tipo de lance preferido</label>
                        <select id="filter-bid-type">
                            <option value="">Qualquer</option>
                            <option value="LF">Lance Fixo</option>
                            <option value="LL">Lance Livre</option>
                            <option value="LI">Lance Fidelidade</option>
                            <option value="LM">Lance Limitado</option>
                            <option value="LS">2o Lance Fixo</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Urgencia</label>
                        <select id="filter-urgency">
                            <option value="">Qualquer prazo</option>
                            <option value="short">Curto prazo (ate 60 meses)</option>
                            <option value="medium">Medio prazo (60-120 meses)</option>
                            <option value="long">Longo prazo (acima de 120 meses)</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Indice de correcao</label>
                        <select id="filter-correction">
                            <option value="">Qualquer</option>
                            <option value="INCC">INCC</option>
                            <option value="INPC">INPC</option>
                            <option value="IPCA">IPCA</option>
                            <option value="OUTROS">Outros</option>
                        </select>
                    </div>
                </div>
                <button class="btn btn-primary" id="btn-search">Buscar Grupos</button>
            </div>
            <div id="search-results" class="results-area"></div>
        </section>

        <!-- COMPARAR -->
        <section id="view-comparar" class="view">
            <h1 class="view-title">Comparar Grupos</h1>
            <p class="subtitle">Selecione ate 3 grupos para comparar lado a lado</p>
            <div class="compare-selectors" id="compare-selectors">
                <div class="compare-slot">
                    <select class="compare-select" data-slot="0">
                        <option value="">Selecione um grupo</option>
                    </select>
                </div>
                <div class="compare-slot">
                    <select class="compare-select" data-slot="1">
                        <option value="">Selecione um grupo</option>
                    </select>
                </div>
                <div class="compare-slot">
                    <select class="compare-select" data-slot="2">
                        <option value="">Selecione um grupo</option>
                    </select>
                </div>
            </div>
            <div id="compare-result" class="compare-grid"></div>
        </section>

        <!-- CALENDARIO -->
        <section id="view-calendario" class="view">
            <h1 class="view-title">Calendario de Assembleias</h1>
            <div class="calendar-filters">
                <select id="calendar-product">
                    <option value="101">Imoveis (101)</option>
                    <option value="102">Veiculos (102)</option>
                    <option value="105">Veiculos/Pesados (105)</option>
                    <option value="106">Servicos (106)</option>
                    <option value="109">OBM (109)</option>
                </select>
            </div>
            <div id="calendar-grid" class="calendar-grid"></div>
        </section>

        <!-- HISTOGRAMA -->
        <section id="view-histograma" class="view">
            <h1 class="view-title">Upload de Histograma</h1>
            <p class="subtitle">Faca upload da tabela de histograma ADEMICON para importar dados de contemplacao por lance. Lances cancelados sao automaticamente excluidos da analise.</p>
            <div class="upload-area" id="upload-area">
                <div class="upload-box" id="upload-box">
                    <span class="upload-icon">&#128196;</span>
                    <p>Arraste o arquivo aqui ou clique para selecionar</p>
                    <p class="upload-hint">Formatos aceitos: .xlsx, .xls, .csv</p>
                    <input type="file" id="file-input" accept=".xlsx,.xls,.csv" hidden>
                </div>
            </div>
            <div id="histogram-results" class="histogram-results"></div>
        </section>

        <!-- GROUP DETAIL MODAL -->
        <div class="modal-overlay" id="modal-overlay">
            <div class="modal" id="group-modal">
                <button class="modal-close" id="modal-close">&times;</button>
                <div id="modal-content"></div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <p>Sistema de Analise &mdash; ADEMICON &copy; 2026 | Dados atualizados em 24/02/2026</p>
    </footer>

    <script>
{dados_js}
    </script>
    <script>
{app_js}
    </script>
</body>
</html>
'''

with open('/home/dev/workspace/precisamos-criar-um-sistema/index.html', 'w') as f:
    f.write(html)

print(f"Built index.html: {len(html)} chars")
