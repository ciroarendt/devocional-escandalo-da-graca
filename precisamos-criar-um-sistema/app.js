// ADEMICON — Sistema de Análise de Grupos
// app.js — Main application logic

(function() {
    'use strict';

    const groups = DADOS.groups;
    const calendar = DADOS.calendar;
    const compareSlots = [null, null, null];

    // =====================
    // UTILITY FUNCTIONS
    // =====================

    function currency(val) {
        if (!val && val !== 0) return '—';
        return 'R$ ' + Number(val).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    function pct(val) {
        if (!val && val !== 0) return '—';
        return (val * 100).toFixed(2) + '%';
    }

    function statusLabel(status) {
        const map = {
            'in-progress': 'Em andamento',
            'in-formation': 'Em formação',
            'completed': 'Concluído',
            'cancelled': 'Cancelado'
        };
        return map[status] || status;
    }

    function statusBadgeClass(status) {
        const map = {
            'in-progress': 'badge-green',
            'in-formation': 'badge-blue',
            'completed': 'badge-gray',
            'cancelled': 'badge-red'
        };
        return map[status] || 'badge-gray';
    }

    function bidBadges(bids) {
        const order = ['LF', 'LL', 'LI', 'LM', 'LS'];
        return order.map(code => {
            const b = bids[code];
            if (!b) return '';
            const cls = b.enabled ? '' : ' disabled';
            return `<span class="bid-badge${cls}" title="${b.name}">${code}</span>`;
        }).filter(Boolean).join('');
    }

    function planLabel(sp) {
        if (!sp || !sp.name) return '—';
        const name = sp.name;
        if (sp.isDiluted) return 'Diluido';
        if (sp.isHole) return 'Red. c/ Furo';
        if (name.toLowerCase().includes('linear')) return 'Linear';
        if (name.toLowerCase().includes('reduz')) return 'Reduzido';
        return name.length > 20 ? name.substring(0, 20) + '...' : name;
    }

    function formatDate(dateStr) {
        if (!dateStr) return '—';
        const parts = dateStr.split('/');
        if (parts.length === 3) return `${parts[0]}/${parts[1]}/${parts[2]}`;
        return dateStr;
    }

    // =====================
    // SCORING ALGORITHM
    // =====================

    function calculateScore(group, filters) {
        let score = 50; // Base score

        // Credit proximity (0-25 points)
        if (filters.credit) {
            const diff = Math.abs(group.amount - filters.credit) / filters.credit;
            if (diff < 0.1) score += 25;
            else if (diff < 0.25) score += 20;
            else if (diff < 0.5) score += 10;
            else score -= 5;
        }

        // Installment within budget (0-20 points)
        if (filters.installment) {
            const instVal = group.installment.reducedValue || group.installment.value;
            if (instVal <= filters.installment) {
                score += 20;
                // Bonus for being close to budget (using more of it)
                const usage = instVal / filters.installment;
                if (usage > 0.7) score += 5;
            } else {
                score -= 15;
            }
        }

        // Bid type availability (0-15 points)
        if (filters.bidType) {
            const bid = group.bids[filters.bidType];
            if (bid && bid.enabled) {
                score += 15;
            } else {
                score -= 10;
            }
        }

        // Urgency match (0-10 points)
        if (filters.urgency) {
            const months = group.installment.monthsRemaining;
            if (filters.urgency === 'short' && months <= 60) score += 10;
            else if (filters.urgency === 'medium' && months > 60 && months <= 120) score += 10;
            else if (filters.urgency === 'long' && months > 120) score += 10;
            else score -= 5;
        }

        // Bonus for more bid options
        const enabledBids = Object.values(group.bids).filter(b => b.enabled).length;
        score += enabledBids * 2;

        // Bonus for active group
        if (group.active) score += 3;
        if (group.status === 'in-formation') score += 5;

        // Bonus for more remaining participants (more chances)
        if (group.participantsRemaining > 1000) score += 3;

        // Lower admin fee is better
        if (group.administrationFee < 0.2) score += 5;
        else if (group.administrationFee < 0.25) score += 2;

        return Math.max(0, Math.min(100, Math.round(score)));
    }

    function scoreClass(score) {
        if (score >= 70) return 'score-high';
        if (score >= 45) return 'score-medium';
        return 'score-low';
    }

    // =====================
    // NAVIGATION
    // =====================

    const navBtns = document.querySelectorAll('.nav-btn');
    const views = document.querySelectorAll('.view');
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav');

    function switchView(viewName) {
        views.forEach(v => v.classList.remove('active'));
        navBtns.forEach(b => b.classList.remove('active'));
        document.getElementById('view-' + viewName).classList.add('active');
        document.querySelector(`.nav-btn[data-view="${viewName}"]`).classList.add('active');
        nav.classList.remove('open');
    }

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.view));
    });

    menuToggle.addEventListener('click', () => {
        nav.classList.toggle('open');
    });

    // =====================
    // DASHBOARD
    // =====================

    function renderDashboard() {
        const statsGrid = document.getElementById('stats-grid');
        const segCounts = {};
        const fullDataGroups = groups.filter(g => g.hasFullData);
        let totalBidTypes = 0;

        groups.forEach(g => {
            segCounts[g.segment] = (segCounts[g.segment] || 0) + 1;
            totalBidTypes += Object.values(g.bids).filter(b => b.enabled).length;
        });

        statsGrid.innerHTML = `
            <div class="stat-card">
                <div class="stat-value">${groups.length}</div>
                <div class="stat-label">Grupos Ativos</div>
            </div>
            <div class="stat-card green">
                <div class="stat-value">${fullDataGroups.length}</div>
                <div class="stat-label">Com Cotas Disponíveis</div>
            </div>
            <div class="stat-card blue">
                <div class="stat-value">${Object.keys(segCounts).length}</div>
                <div class="stat-label">Segmentos</div>
            </div>
            <div class="stat-card orange">
                <div class="stat-value">${Math.round(totalBidTypes / groups.length * 10) / 10}</div>
                <div class="stat-label">Lances por Grupo (média)</div>
            </div>
        `;

        // Segment tabs
        const tabsEl = document.getElementById('segment-tabs');
        const segs = ['Todos', ...Object.keys(segCounts)];
        tabsEl.innerHTML = segs.map(seg => {
            const count = seg === 'Todos' ? groups.length : segCounts[seg];
            return `<button class="seg-tab${seg === 'Todos' ? ' active' : ''}" data-seg="${seg}">${seg}<span class="seg-count">${count}</span></button>`;
        }).join('') + `<label style="display:inline-flex;align-items:center;gap:6px;margin-left:16px;font-size:12px;color:#757575;cursor:pointer"><input type="checkbox" id="hide-no-data" checked> Apenas com cotas disponíveis</label>`;

        tabsEl.querySelectorAll('.seg-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                tabsEl.querySelectorAll('.seg-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                renderDashboardTable(tab.dataset.seg);
            });
        });

        document.getElementById('hide-no-data').addEventListener('change', () => {
            const activeSeg = tabsEl.querySelector('.seg-tab.active').dataset.seg;
            renderDashboardTable(activeSeg);
        });

        renderDashboardTable('Todos');
    }

    function renderDashboardTable(segment) {
        const tbody = document.getElementById('dashboard-tbody');
        const hideNoData = document.getElementById('hide-no-data') && document.getElementById('hide-no-data').checked;
        let filtered = segment === 'Todos' ? groups : groups.filter(g => g.segment === segment);
        if (hideNoData) filtered = filtered.filter(g => g.hasFullData);

        tbody.innerHTML = filtered.map(g => {
            const instVal = g.installment.reducedValue || g.installment.value;
            const noData = !g.hasFullData;
            const rowCls = noData ? ' style="opacity:0.65"' : '';
            return `<tr${rowCls}>
                <td class="group-name">${g.name} ${g.category ? '<small style="color:#9e9e9e">Cat ' + g.category + '</small>' : ''}</td>
                <td class="currency">${noData ? '<span style="color:#bdbdbd">—</span>' : currency(g.amount)}</td>
                <td class="currency">${noData ? '<span style="color:#bdbdbd">—</span>' : currency(instVal)}</td>
                <td>${noData ? '—' : pct(g.administrationFee)}</td>
                <td>${noData ? '—' : g.installment.monthsRemaining + ' meses'}</td>
                <td>${noData ? '—' : g.participantsRemaining.toLocaleString('pt-BR') + ' / ' + g.participantsTotal.toLocaleString('pt-BR')}</td>
                <td><div class="bid-badges">${bidBadges(g.bids)}</div></td>
                <td>${noData ? '<span class="badge badge-orange">Cotas esgotadas</span>' : '<span class="badge badge-gray" title="' + g.salesPlan.name + '">' + planLabel(g.salesPlan) + '</span>'}</td>
                <td>${noData ? '<span class="badge badge-gray">Ativo</span>' : '<span class="badge ' + statusBadgeClass(g.status) + '">' + statusLabel(g.status) + '</span>'}</td>
                <td>
                    <button class="btn btn-sm btn-outline" onclick="app.showDetail('${g.id}')">Detalhes</button>
                </td>
            </tr>`;
        }).join('');
    }

    // =====================
    // SEARCH / FILTER
    // =====================

    function initFilters() {
        const segSelect = document.getElementById('filter-segment');
        const segs = [...new Set(groups.map(g => g.segment))];
        segs.forEach(seg => {
            const opt = document.createElement('option');
            opt.value = seg;
            opt.textContent = seg;
            segSelect.appendChild(opt);
        });

        document.getElementById('btn-search').addEventListener('click', performSearch);

        // Also search on Enter
        document.querySelectorAll('.filters-card input, .filters-card select').forEach(el => {
            el.addEventListener('keydown', e => { if (e.key === 'Enter') performSearch(); });
            el.addEventListener('change', performSearch);
        });
    }

    function performSearch() {
        const filters = {
            segment: document.getElementById('filter-segment').value,
            credit: parseFloat(document.getElementById('filter-credit').value) || 0,
            installment: parseFloat(document.getElementById('filter-installment').value) || 0,
            bidType: document.getElementById('filter-bid-type').value,
            urgency: document.getElementById('filter-urgency').value,
            correction: document.getElementById('filter-correction').value,
        };

        let filtered = [...groups];

        if (filters.segment) {
            filtered = filtered.filter(g => g.segment === filters.segment);
        }

        if (filters.correction) {
            filtered = filtered.filter(g => g.correctionIndex === filters.correction);
        }

        // Filter by installment budget
        if (filters.installment) {
            filtered = filtered.filter(g => {
                const instVal = g.installment.reducedValue || g.installment.value;
                return instVal <= filters.installment * 1.1; // 10% tolerance
            });
        }

        // Filter by bid type
        if (filters.bidType) {
            filtered = filtered.filter(g => {
                const bid = g.bids[filters.bidType];
                return bid && bid.enabled;
            });
        }

        // Filter by urgency
        if (filters.urgency) {
            filtered = filtered.filter(g => {
                const months = g.installment.monthsRemaining;
                if (filters.urgency === 'short') return months <= 60;
                if (filters.urgency === 'medium') return months > 60 && months <= 120;
                if (filters.urgency === 'long') return months > 120;
                return true;
            });
        }

        // Score and sort
        filtered.forEach(g => {
            g._score = calculateScore(g, filters);
        });
        filtered.sort((a, b) => b._score - a._score);

        renderSearchResults(filtered);
    }

    function renderSearchResults(results) {
        const container = document.getElementById('search-results');

        if (results.length === 0) {
            container.innerHTML = '<div class="no-results"><span>🔍</span><p>Nenhum grupo encontrado com esses filtros.</p><p>Tente ajustar os critérios de busca.</p></div>';
            return;
        }

        container.innerHTML = results.map(g => {
            const instVal = g.installment.reducedValue || g.installment.value;
            const sc = g._score || 50;
            const noData = !g.hasFullData;
            return `<div class="result-card" ${noData ? 'style="border-top-color:#FF9800"' : ''}>
                <div class="score-circle ${scoreClass(sc)}">${sc}</div>
                <div class="rc-name">${g.name} ${noData ? '<span class="badge badge-orange" style="font-size:10px;vertical-align:middle">Cotas esgotadas</span>' : ''}</div>
                <div class="rc-segment">${g.segment} | Cat. ${g.category || '—'} ${g.correctionIndex ? '| ' + g.correctionIndex : ''}</div>
                <div class="rc-grid">
                    <div class="rc-item">
                        <label>Crédito</label>
                        <span>${noData ? '—' : currency(g.amount)}</span>
                    </div>
                    <div class="rc-item">
                        <label>Parcela</label>
                        <span>${noData ? '—' : currency(instVal)}</span>
                    </div>
                    <div class="rc-item">
                        <label>Taxa Admin</label>
                        <span>${noData ? '—' : pct(g.administrationFee)}</span>
                    </div>
                    <div class="rc-item">
                        <label>Meses Restantes</label>
                        <span>${noData ? '—' : g.installment.monthsRemaining}</span>
                    </div>
                </div>
                <div class="rc-bids">
                    <div class="bid-badges">${bidBadges(g.bids)}</div>
                </div>
                <div class="rc-actions">
                    <button class="btn btn-sm btn-primary" onclick="app.showDetail('${g.id}')">Detalhes</button>
                    <button class="btn btn-sm btn-compare" onclick="app.addToCompare('${g.id}', this)">+ Comparar</button>
                </div>
            </div>`;
        }).join('');
    }

    // =====================
    // GROUP DETAIL MODAL
    // =====================

    function showDetail(groupId) {
        const g = groups.find(x => x.id === groupId);
        if (!g) return;

        const modal = document.getElementById('modal-content');
        const instVal = g.installment.reducedValue || g.installment.value;
        const noData = !g.hasFullData;

        modal.innerHTML = `
            <h2>Grupo ${g.name}</h2>
            <p class="modal-segment">${g.segment} | ${noData ? 'Cotas esgotadas' : statusLabel(g.status)} | Categoria ${g.category || '—'}</p>
            ${noData ? '<div style="background:#FFF3E0;padding:10px 14px;border-radius:8px;margin-bottom:16px;font-size:13px;color:#E65100">Este grupo possui cotas esgotadas no simulador. Dados de crédito, parcela e taxas não estão disponíveis. Apenas a configuração de lances está disponível.</div>' : ''}

            <div class="detail-section">
                <h3>Valores</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>Crédito</label>
                        <span>${currency(g.amount)}</span>
                    </div>
                    <div class="detail-item">
                        <label>Parcela Mensal</label>
                        <span>${currency(g.installment.value)}</span>
                    </div>
                    <div class="detail-item">
                        <label>Parcela Reduzida</label>
                        <span>${currency(g.installment.reducedValue)}</span>
                    </div>
                    <div class="detail-item">
                        <label>Valor Final Reduzida</label>
                        <span>${currency(g.installment.finalReducedValue)}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Prazos</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>Meses Restantes</label>
                        <span>${g.installment.monthsRemaining} de ${g.installment.monthsTotal}</span>
                    </div>
                    <div class="detail-item">
                        <label>Mês Final Reduzida</label>
                        <span>${g.installment.finalReducedMonth}${g.installment.finalReducedMonth ? 'o mês' : ''}</span>
                    </div>
                    <div class="detail-item">
                        <label>Índice de Correção</label>
                        <span>${g.correctionIndex}</span>
                    </div>
                    <div class="detail-item">
                        <label>Status</label>
                        <span class="badge ${statusBadgeClass(g.status)}">${statusLabel(g.status)}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Taxas</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>Taxa Administração</label>
                        <span>${pct(g.administrationFee)}</span>
                    </div>
                    <div class="detail-item">
                        <label>Taxa Adm / Ano</label>
                        <span>${pct(g.administrationFeePerYear)}</span>
                    </div>
                    <div class="detail-item">
                        <label>Seguro</label>
                        <span>${pct(g.insuranceFee)}</span>
                    </div>
                    <div class="detail-item">
                        <label>Fundo Reserva</label>
                        <span>${pct(g.reserveFundFee)}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Participantes</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>Total</label>
                        <span>${g.participantsTotal.toLocaleString('pt-BR')}</span>
                    </div>
                    <div class="detail-item">
                        <label>Vagas Restantes</label>
                        <span>${g.participantsRemaining.toLocaleString('pt-BR')}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Tipo de Parcela</h3>
                <div class="detail-item" style="margin-bottom: 8px;">
                    <label>Plano de Venda</label>
                    <span>${g.salesPlan.name || '—'}</span>
                </div>
                <div class="detail-grid">
                    <div class="detail-item">
                        <label>Diluido</label>
                        <span>${g.salesPlan.isDiluted ? 'Sim' : 'Não'}</span>
                    </div>
                    <div class="detail-item">
                        <label>Com Furo</label>
                        <span>${g.salesPlan.isHole ? 'Sim' : 'Não'}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Lances Disponíveis</h3>
                <div class="bids-detail">
                    ${renderBidCards(g.bids)}
                </div>
            </div>
        `;

        document.getElementById('modal-overlay').classList.add('open');
    }

    function renderBidCards(bids) {
        const order = ['LF', 'LL', 'LI', 'LM', 'LS'];
        return order.map(code => {
            const b = bids[code];
            if (!b) return '';
            const cls = b.enabled ? 'enabled' : '';
            return `<div class="bid-card ${cls}">
                <div class="bid-name">${b.name} (${code})</div>
                <div class="bid-info">
                    ${b.enabled ? 'Habilitado' : 'Desabilitado'}<br>
                    Oferta: ${b.oferta === 'PE' ? 'Percentual' : b.oferta === 'PC' ? 'Parcelas' : b.oferta || '—'}<br>
                    Lance embutido máx: ${b.lance_embutido_max ? b.lance_embutido_max + '%' : '—'}<br>
                    Parcelas embutido máx: ${b.parcelas_embutido_max || '—'}
                </div>
            </div>`;
        }).filter(Boolean).join('');
    }

    // Close modal
    document.getElementById('modal-close').addEventListener('click', () => {
        document.getElementById('modal-overlay').classList.remove('open');
    });
    document.getElementById('modal-overlay').addEventListener('click', e => {
        if (e.target === document.getElementById('modal-overlay')) {
            document.getElementById('modal-overlay').classList.remove('open');
        }
    });

    // =====================
    // COMPARE
    // =====================

    function initCompare() {
        const selects = document.querySelectorAll('.compare-select');
        const optionsHtml = groups.map(g =>
            `<option value="${g.id}">${g.name} — ${g.segment} — ${currency(g.amount)}</option>`
        ).join('');

        selects.forEach(sel => {
            sel.innerHTML = '<option value="">Selecione um grupo</option>' + optionsHtml;
            sel.addEventListener('change', renderCompare);
        });
    }

    function addToCompare(groupId, btnEl) {
        // Find empty slot
        const emptySlot = compareSlots.findIndex(s => s === null);
        if (emptySlot === -1) {
            // Replace first slot
            compareSlots[0] = groupId;
        } else {
            compareSlots[emptySlot] = groupId;
        }

        // Update selects
        compareSlots.forEach((id, i) => {
            const sel = document.querySelector(`.compare-select[data-slot="${i}"]`);
            if (sel) sel.value = id || '';
        });

        if (btnEl) {
            btnEl.classList.add('selected');
            btnEl.textContent = 'Adicionado';
        }

        renderCompare();
    }

    function renderCompare() {
        const container = document.getElementById('compare-result');
        const selects = document.querySelectorAll('.compare-select');
        const selectedGroups = [];

        selects.forEach((sel, i) => {
            const gId = sel.value;
            compareSlots[i] = gId || null;
            if (gId) {
                const g = groups.find(x => x.id === gId);
                if (g) selectedGroups.push(g);
            }
        });

        if (selectedGroups.length === 0) {
            container.innerHTML = '<div class="no-results" style="grid-column:1/-1"><span>📊</span><p>Selecione grupos para comparar</p></div>';
            return;
        }

        // Find best values for highlighting
        const best = {
            amount: Math.max(...selectedGroups.map(g => g.amount)),
            installment: Math.min(...selectedGroups.map(g => g.installment.reducedValue || g.installment.value)),
            adminFee: Math.min(...selectedGroups.map(g => g.administrationFee)),
            months: null, // depends on preference
            bids: Math.max(...selectedGroups.map(g => Object.values(g.bids).filter(b => b.enabled).length)),
        };

        container.innerHTML = selectedGroups.map(g => {
            const instVal = g.installment.reducedValue || g.installment.value;
            const enabledBids = Object.values(g.bids).filter(b => b.enabled).length;

            function bestCls(val, bestVal, lower) {
                if (selectedGroups.length < 2) return '';
                if (lower) return val === bestVal ? 'best' : '';
                return val === bestVal ? 'best' : '';
            }

            return `<div class="compare-col">
                <h3>${g.name}</h3>
                <div class="compare-row">
                    <span class="cr-label">Segmento</span>
                    <span class="cr-value">${g.segment}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Crédito</span>
                    <span class="cr-value ${g.amount === best.amount ? 'best' : ''}">${currency(g.amount)}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Parcela</span>
                    <span class="cr-value ${instVal === best.installment ? 'best' : ''}">${currency(instVal)}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Parcela Cheia</span>
                    <span class="cr-value">${currency(g.installment.value)}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Taxa Admin</span>
                    <span class="cr-value ${g.administrationFee === best.adminFee ? 'best' : ''}">${pct(g.administrationFee)}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Taxa Admin/Ano</span>
                    <span class="cr-value">${pct(g.administrationFeePerYear)}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Seguro</span>
                    <span class="cr-value">${pct(g.insuranceFee)}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Fundo Reserva</span>
                    <span class="cr-value">${pct(g.reserveFundFee)}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Meses Restantes</span>
                    <span class="cr-value">${g.installment.monthsRemaining} / ${g.installment.monthsTotal}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Participantes</span>
                    <span class="cr-value">${g.participantsRemaining.toLocaleString('pt-BR')} / ${g.participantsTotal.toLocaleString('pt-BR')}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Correção</span>
                    <span class="cr-value">${g.correctionIndex}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Tipo Parcela</span>
                    <span class="cr-value">${planLabel(g.salesPlan)}</span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Lances Hab.</span>
                    <span class="cr-value ${enabledBids === best.bids ? 'best' : ''}">
                        ${enabledBids} de 5
                        <div class="bid-badges" style="margin-top:4px">${bidBadges(g.bids)}</div>
                    </span>
                </div>
                <div class="compare-row">
                    <span class="cr-label">Status</span>
                    <span class="cr-value"><span class="badge ${statusBadgeClass(g.status)}">${statusLabel(g.status)}</span></span>
                </div>
            </div>`;
        }).join('');
    }

    // =====================
    // CALENDAR
    // =====================

    function initCalendar() {
        document.getElementById('calendar-product').addEventListener('change', renderCalendar);
        renderCalendar();
    }

    function renderCalendar() {
        const pid = document.getElementById('calendar-product').value;
        const container = document.getElementById('calendar-grid');
        const assemblies = calendar[pid] || [];

        if (assemblies.length === 0) {
            container.innerHTML = '<div class="no-results"><span>📅</span><p>Nenhuma assembleia encontrada para este produto.</p></div>';
            return;
        }

        container.innerHTML = assemblies.map(a => {
            const groupsList = (a.groups || []).join(', ');
            const isPast = isDatePast(a.date);
            return `<div class="calendar-card" style="${isPast ? 'opacity: 0.5' : ''}">
                <div class="cal-date">${formatDate(a.date)}</div>
                <div class="cal-time">${a.time || ''}</div>
                <div class="cal-groups">${groupsList ? 'Grupos: ' + groupsList : 'Sem grupos listados'}</div>
                ${isPast ? '<span class="badge badge-gray">Realizada</span>' : '<span class="badge badge-green">Futura</span>'}
            </div>`;
        }).join('');
    }

    function isDatePast(dateStr) {
        if (!dateStr) return false;
        const parts = dateStr.split('/');
        if (parts.length !== 3) return false;
        const d = new Date(parts[2], parts[1] - 1, parts[0]);
        return d < new Date();
    }

    // =====================
    // HISTOGRAM UPLOAD
    // =====================

    function initHistogram() {
        const uploadBox = document.getElementById('upload-box');
        const fileInput = document.getElementById('file-input');

        uploadBox.addEventListener('click', () => fileInput.click());

        uploadBox.addEventListener('dragover', e => {
            e.preventDefault();
            uploadBox.style.borderColor = 'var(--red)';
            uploadBox.style.background = 'var(--red-light)';
        });

        uploadBox.addEventListener('dragleave', () => {
            uploadBox.style.borderColor = '';
            uploadBox.style.background = '';
        });

        uploadBox.addEventListener('drop', e => {
            e.preventDefault();
            uploadBox.style.borderColor = '';
            uploadBox.style.background = '';
            if (e.dataTransfer.files.length) {
                processFile(e.dataTransfer.files[0]);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                processFile(fileInput.files[0]);
            }
        });
    }

    function processFile(file) {
        const results = document.getElementById('histogram-results');
        const ext = file.name.split('.').pop().toLowerCase();

        if (ext === 'csv') {
            const reader = new FileReader();
            reader.onload = e => parseCSV(e.target.result);
            reader.readAsText(file, 'utf-8');
        } else if (ext === 'xlsx' || ext === 'xls') {
            results.innerHTML = `
                <h3>Arquivo recebido: ${file.name}</h3>
                <p style="color: var(--gray-600); margin-top: 8px;">
                    Para processar arquivos Excel (.xlsx/.xls), salve como CSV primeiro e faça upload novamente.
                    <br><br>
                    Alternativamente, copie os dados da planilha e cole no campo abaixo:
                </p>
                <textarea id="paste-area" placeholder="Cole os dados da planilha aqui (separados por tab)"
                    style="width:100%; height:200px; margin-top:12px; padding:12px; border:1px solid var(--gray-300); border-radius:8px; font-family:monospace; font-size:12px;"></textarea>
                <button class="btn btn-primary" style="margin-top:12px" onclick="app.parsePastedData()">Processar Dados</button>
            `;
        } else {
            results.innerHTML = '<p style="color:var(--red)">Formato não suportado. Use .csv, .xlsx ou .xls</p>';
        }
    }

    function parseCSV(text) {
        const results = document.getElementById('histogram-results');
        const lines = text.split('\n').map(l => l.trim()).filter(Boolean);

        if (lines.length < 2) {
            results.innerHTML = '<p style="color:var(--red)">Arquivo vazio ou inválido.</p>';
            return;
        }

        // Detect separator
        const sep = lines[0].includes(';') ? ';' : lines[0].includes('\t') ? '\t' : ',';
        const rows = lines.map(l => l.split(sep).map(c => c.trim().replace(/^"|"$/g, '')));

        renderHistogramTable(rows);
    }

    function parsePastedData() {
        const textarea = document.getElementById('paste-area');
        if (!textarea) return;
        const text = textarea.value;
        if (!text.trim()) return;

        const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
        const rows = lines.map(l => l.split('\t'));
        renderHistogramTable(rows);
    }

    function renderHistogramTable(rows) {
        const results = document.getElementById('histogram-results');
        const headers = rows[0];
        const data = rows.slice(1);

        // Try to identify "cancelled" rows
        // Look for columns that might indicate cancelled status
        const cancelColIdx = headers.findIndex(h =>
            h.toLowerCase().includes('cancel') ||
            h.toLowerCase().includes('status') ||
            h.toLowerCase().includes('situacao') ||
            h.toLowerCase().includes('situação')
        );

        let totalRows = data.length;
        let cancelledRows = 0;

        const tableRows = data.map(row => {
            const isCancelled = cancelColIdx >= 0 && row[cancelColIdx] &&
                (row[cancelColIdx].toLowerCase().includes('cancel') ||
                 row[cancelColIdx].toLowerCase().includes('desist'));

            if (isCancelled) cancelledRows++;

            return `<tr class="${isCancelled ? 'cancelled' : ''}">
                ${row.map(cell => `<td>${cell}</td>`).join('')}
            </tr>`;
        }).join('');

        results.innerHTML = `
            <div style="margin-bottom: 16px;">
                <h3>Histograma Importado</h3>
                <p style="color: var(--gray-600); font-size: 13px; margin-top: 4px;">
                    ${totalRows} registros | ${cancelledRows} cancelados (ocultos) | ${totalRows - cancelledRows} ativos
                </p>
                <label style="display: flex; align-items: center; gap: 8px; margin-top: 8px; font-size: 13px; cursor: pointer;">
                    <input type="checkbox" id="show-cancelled" onchange="app.toggleCancelled()">
                    Mostrar lances cancelados
                </label>
            </div>
            <div class="groups-table-wrap">
                <table class="histogram-table">
                    <thead><tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr></thead>
                    <tbody>${tableRows}</tbody>
                </table>
            </div>
        `;
    }

    function toggleCancelled() {
        const checked = document.getElementById('show-cancelled').checked;
        document.querySelectorAll('.histogram-table tr.cancelled').forEach(tr => {
            tr.style.display = checked ? '' : 'none';
        });
    }

    // =====================
    // INITIALIZATION
    // =====================

    renderDashboard();
    initFilters();
    initCompare();
    initCalendar();
    initHistogram();

    // Expose functions for inline handlers
    window.app = {
        showDetail,
        addToCompare,
        parsePastedData,
        toggleCancelled
    };

})();
