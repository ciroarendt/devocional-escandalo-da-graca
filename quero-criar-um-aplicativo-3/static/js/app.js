/**
 * Dashboard Lei do Bem — Lotes MCTI
 * Frontend JavaScript
 */

(function () {
    "use strict";

    // ── State ──────────────────────────────────────
    let allLotes = [];
    let filteredLotes = [];
    let stats = {};

    // ── DOM Elements ───────────────────────────────
    const els = {
        loading: document.getElementById("loading-overlay"),
        statTotal: document.getElementById("stat-total"),
        statPdf: document.getElementById("stat-pdf"),
        statZip: document.getElementById("stat-zip"),
        statYears: document.getElementById("stat-years"),
        scrapedAt: document.getElementById("scraped-at"),
        searchInput: document.getElementById("search-input"),
        filterYear: document.getElementById("filter-year"),
        filterType: document.getElementById("filter-type"),
        filterFormat: document.getElementById("filter-format"),
        filterCount: document.getElementById("filter-count"),
        yearChart: document.getElementById("year-chart"),
        tbody: document.getElementById("lotes-tbody"),
        btnRefresh: document.getElementById("btn-refresh"),
        btnCopyLinks: document.getElementById("btn-copy-links"),
        toast: document.getElementById("toast"),
    };

    // ── API ────────────────────────────────────────
    async function fetchLotes(forceRefresh) {
        const url = forceRefresh ? "/api/refresh" : "/api/lotes";
        showLoading(true);
        try {
            const resp = await fetch(url);
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const data = await resp.json();
            if (data.error) throw new Error(data.error);
            return data;
        } catch (err) {
            showToast("Erro ao carregar dados: " + err.message);
            throw err;
        } finally {
            showLoading(false);
        }
    }

    // ── Render Stats ───────────────────────────────
    function renderStats(s) {
        animateNumber(els.statTotal, s.total);
        animateNumber(els.statPdf, s.by_format["PDF"] || 0);
        animateNumber(els.statZip, (s.by_format["ZIP"] || 0) + (s.by_format["7Z"] || 0));
        animateNumber(els.statYears, s.years.length);
        els.scrapedAt.textContent = "";
    }

    function animateNumber(el, target) {
        let current = 0;
        const step = Math.ceil(target / 20);
        const interval = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(interval);
            }
            el.textContent = current;
        }, 30);
    }

    // ── Render Chart ───────────────────────────────
    function renderChart(s) {
        const years = s.years.slice().sort();
        const maxCount = Math.max(...years.map((y) => s.by_year[y] || 0), 1);
        const maxBarHeight = 110; // px

        els.yearChart.innerHTML = years
            .map((year) => {
                const count = s.by_year[year] || 0;
                const height = Math.max((count / maxCount) * maxBarHeight, 8);
                return `
                <div class="chart-bar-group" data-year="${year}">
                    <span class="chart-bar-value">${count}</span>
                    <div class="chart-bar" style="height: ${height}px" title="${year}: ${count} documentos"></div>
                    <span class="chart-bar-label">${year}</span>
                </div>`;
            })
            .join("");

        // Click on bar to filter by year
        els.yearChart.querySelectorAll(".chart-bar-group").forEach((group) => {
            group.style.cursor = "pointer";
            group.addEventListener("click", () => {
                const year = group.dataset.year;
                els.filterYear.value = year;
                applyFilters();
            });
        });
    }

    // ── Render Filters ─────────────────────────────
    function populateFilters(s) {
        // Year
        els.filterYear.innerHTML = '<option value="">Todos</option>';
        s.years.forEach((year) => {
            const opt = document.createElement("option");
            opt.value = year;
            opt.textContent = year;
            els.filterYear.appendChild(opt);
        });

        // Type
        els.filterType.innerHTML = '<option value="">Todos</option>';
        s.types.forEach((type) => {
            const opt = document.createElement("option");
            opt.value = type;
            opt.textContent = type;
            els.filterType.appendChild(opt);
        });

        // Format
        els.filterFormat.innerHTML = '<option value="">Todos</option>';
        Object.keys(s.by_format)
            .sort()
            .forEach((fmt) => {
                const opt = document.createElement("option");
                opt.value = fmt;
                opt.textContent = fmt;
                els.filterFormat.appendChild(opt);
            });
    }

    function applyFilters() {
        const search = els.searchInput.value.toLowerCase().trim();
        const year = els.filterYear.value;
        const type = els.filterType.value;
        const format = els.filterFormat.value;

        filteredLotes = allLotes.filter((l) => {
            if (year && l.year !== year) return false;
            if (type && l.type !== type) return false;
            if (format && l.format !== format) return false;
            if (search) {
                const haystack = `${l.name} ${l.filename} ${l.url} ${l.type} ${l.year}`.toLowerCase();
                if (!haystack.includes(search)) return false;
            }
            return true;
        });

        els.filterCount.textContent = `${filteredLotes.length} de ${allLotes.length} documentos`;
        renderTable(filteredLotes);
    }

    // ── Render Table ───────────────────────────────
    function getTypeClass(type) {
        const map = {
            "Contestacao": "contestacao",
            "Recurso Administrativo": "recurso",
            "Parecer Tecnico": "parecer",
            "Consolidado": "consolidado",
            "Manual": "manual",
            "Retificacao": "retificacao",
        };
        // Normalize for lookup (remove accents)
        const normalized = type
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");
        return map[normalized] || "outro";
    }

    function getFormatClass(format) {
        return format.toLowerCase().replace("/", "");
    }

    function renderTable(lotes) {
        if (lotes.length === 0) {
            els.tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="empty-state">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                        </svg>
                        <p>Nenhum documento encontrado com os filtros selecionados.</p>
                    </td>
                </tr>`;
            return;
        }

        els.tbody.innerHTML = lotes
            .map(
                (l, idx) => `
            <tr style="animation-delay: ${Math.min(idx * 0.02, 0.5)}s">
                <td class="col-id" style="text-align:center; color: var(--gray-400); font-size: 0.78rem;">${idx + 1}</td>
                <td class="col-year">
                    <span class="year-badge">${l.year}</span>
                </td>
                <td class="col-name">
                    <div class="doc-name">${escapeHtml(l.name)}${l.is_legacy ? '<span class="legacy-badge">antigo</span>' : ""}</div>
                    <div class="doc-filename">${escapeHtml(l.filename)}</div>
                </td>
                <td class="col-type">
                    <span class="type-badge type-${getTypeClass(l.type)}">${escapeHtml(l.type)}</span>
                </td>
                <td class="col-format">
                    <span class="format-badge format-${getFormatClass(l.format)}">${l.format}</span>
                </td>
                <td class="col-action" style="text-align:center">
                    <a href="${escapeHtml(l.url)}" target="_blank" rel="noopener" class="btn btn-download" title="Baixar ${escapeHtml(l.filename)}">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                        Baixar
                    </a>
                </td>
            </tr>`
            )
            .join("");
    }

    // ── Helpers ────────────────────────────────────
    function escapeHtml(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    function showLoading(show) {
        if (show) {
            els.loading.classList.remove("hidden");
        } else {
            els.loading.classList.add("hidden");
        }
    }

    function showToast(message) {
        els.toast.textContent = message;
        els.toast.classList.add("show");
        setTimeout(() => els.toast.classList.remove("show"), 3000);
    }

    function copyFilteredLinks() {
        if (filteredLotes.length === 0) {
            showToast("Nenhum link para copiar.");
            return;
        }
        const links = filteredLotes.map((l) => l.url).join("\n");
        navigator.clipboard
            .writeText(links)
            .then(() => showToast(`${filteredLotes.length} links copiados!`))
            .catch(() => {
                // Fallback for environments without clipboard API
                const ta = document.createElement("textarea");
                ta.value = links;
                document.body.appendChild(ta);
                ta.select();
                document.execCommand("copy");
                document.body.removeChild(ta);
                showToast(`${filteredLotes.length} links copiados!`);
            });
    }

    // ── Event Listeners ────────────────────────────
    els.searchInput.addEventListener("input", debounce(applyFilters, 250));
    els.filterYear.addEventListener("change", applyFilters);
    els.filterType.addEventListener("change", applyFilters);
    els.filterFormat.addEventListener("change", applyFilters);
    els.btnRefresh.addEventListener("click", () => init(true));
    els.btnCopyLinks.addEventListener("click", copyFilteredLinks);

    function debounce(fn, delay) {
        let timer;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    }

    // ── Init ───────────────────────────────────────
    async function init(forceRefresh) {
        try {
            const data = await fetchLotes(forceRefresh);
            allLotes = data.lotes;
            stats = data.stats;

            renderStats(stats);
            renderChart(stats);
            populateFilters(stats);
            applyFilters();

            if (forceRefresh) {
                showToast("Dados atualizados com sucesso!");
            }
        } catch (err) {
            console.error("Failed to load data:", err);
        }
    }

    init(false);
})();
