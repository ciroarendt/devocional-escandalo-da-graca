/**
 * bible.js — Bíblia NVT via bolls.life API + Sistema de Tooltips
 * Bíblia na Mesa · 365 Devocionais
 *
 * API: https://bolls.life/get-verse/NVT/{book_num}/{chapter}/{verse}/
 */

// ─── Mapa de livros PT-BR → número do livro (ordem canônica) ──────────────
const BOOK_NUM = {
  // Antigo Testamento
  'genesis': 1, 'gênesis': 1,
  'exodo': 2, 'êxodo': 2,
  'levitico': 3, 'levítico': 3,
  'numeros': 4, 'números': 4,
  'deuteronomio': 5, 'deuteronômio': 5,
  'josue': 6, 'josué': 6,
  'juizes': 7, 'juízes': 7,
  'rute': 8,
  '1 samuel': 9, '1samuel': 9,
  '2 samuel': 10, '2samuel': 10,
  '1 reis': 11, '1reis': 11,
  '2 reis': 12, '2reis': 12,
  '1 cronicas': 13, '1 crônicas': 13,
  '2 cronicas': 14, '2 crônicas': 14,
  'esdras': 15,
  'neemias': 16,
  'ester': 17,
  'jo': 18, 'jó': 18,
  'salmos': 19, 'salmo': 19,
  'proverbios': 20, 'provérbios': 20,
  'eclesiastes': 21,
  'cantares': 22, 'cantares dos cantares': 22,
  'isaias': 23, 'isaías': 23,
  'jeremias': 24,
  'lamentacoes': 25, 'lamentações': 25,
  'ezequiel': 26,
  'daniel': 27,
  'oseias': 28, 'oséias': 28,
  'joel': 29,
  'amos': 30, 'amós': 30,
  'obadias': 31,
  'jonas': 32,
  'miqueias': 33,
  'naum': 34,
  'habacuque': 35,
  'sofonias': 36,
  'ageu': 37,
  'zacarias': 38,
  'malaquias': 39,
  // Novo Testamento
  'mateus': 40,
  'marcos': 41,
  'lucas': 42,
  'joao': 43, 'joão': 43,
  'atos': 44,
  'romanos': 45,
  '1 corintios': 46, '1 coríntios': 46,
  '2 corintios': 47, '2 coríntios': 47,
  'galatas': 48, 'gálatas': 48,
  'efesios': 49, 'efésios': 49,
  'filipenses': 50,
  'colossenses': 51,
  '1 tessalonicenses': 52,
  '2 tessalonicenses': 53,
  '1 timoteo': 54, '1 timóteo': 54,
  '2 timoteo': 55, '2 timóteo': 55,
  'tito': 56,
  'filemom': 57,
  'hebreus': 58,
  'tiago': 59,
  '1 pedro': 60,
  '2 pedro': 61,
  '1 joao': 62, '1 joão': 62,
  '2 joao': 63, '2 joão': 63,
  '3 joao': 64, '3 joão': 64,
  'judas': 65,
  'apocalipse': 66
};

const verseCache = new Map();

/**
 * Faz o parse de uma referência como "João 3:16" ou "Romanos 8:28-30"
 * Retorna { bookNum, chapter, verse } ou null se não reconhecido.
 */
function parseReference(refText) {
  const raw = refText.trim().toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '') // remove acentos para match
    .replace(/[.,;]/g, '');

  // tenta identificar o livro (do mais longo para o mais curto)
  const keys = Object.keys(BOOK_NUM).sort((a, b) => b.length - a.length);
  let bookNum = null;
  let rest = '';

  for (const key of keys) {
    const normalKey = key.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    if (raw.startsWith(normalKey)) {
      bookNum = BOOK_NUM[key];
      rest = raw.slice(normalKey.length).trim();
      break;
    }
  }

  if (!bookNum) return null;

  // extrai capítulo e versículo: "3:16", "3.16", "3 16"
  const match = rest.match(/^(\d+)[:.\s](\d+)/);
  if (!match) return null;

  return { bookNum, chapter: parseInt(match[1]), verse: parseInt(match[2]) };
}

/**
 * Busca versículo na NVT via bolls.life.
 * Se a referência tiver intervalo (ex: 8:28-30), busca só o primeiro versículo.
 */
async function fetchVerse(refText) {
  const cacheKey = refText.trim();
  if (verseCache.has(cacheKey)) return verseCache.get(cacheKey);

  const parsed = parseReference(cacheKey);

  if (!parsed) {
    const result = { text: 'Referência não reconhecida.', ref: cacheKey, translation: 'NVT', error: true };
    verseCache.set(cacheKey, result);
    return result;
  }

  const { bookNum, chapter, verse } = parsed;
  const url = `https://bolls.life/get-verse/NVT/${bookNum}/${chapter}/${verse}/`;

  try {
    const res = await fetch(url, { signal: AbortSignal.timeout(7000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    const text = data.text
      ? data.text
          .replace(/<br\s*\/?>/gi, ' ')  // converte <br> em espaço (ex: Salmos)
          .replace(/<[^>]+>/g, '')        // remove qualquer outro HTML
          .replace(/\s+/g, ' ')
          .trim()
      : 'Versículo não disponível na NVT.';

    const result = { text, ref: cacheKey, translation: 'NVT' };
    verseCache.set(cacheKey, result);
    return result;
  } catch (err) {
    const result = {
      text: 'Não foi possível carregar o versículo. Verifique sua conexão.',
      ref: cacheKey,
      translation: 'NVT',
      error: true
    };
    verseCache.set(cacheKey, result);
    return result;
  }
}

// ─── Tooltip ───────────────────────────────────────────────────────────────

function positionTooltip(tooltip, anchor) {
  const rect = anchor.getBoundingClientRect();
  const isMobile = window.innerWidth <= 640;

  if (isMobile) {
    tooltip.style.cssText = 'left:0;right:0;bottom:0;top:auto;width:100%;max-width:100%;';
    return;
  }

  const tooltipW = 340;
  const estimatedH = 140;
  let top = rect.bottom + window.scrollY + 8;
  let left = rect.left + window.scrollX;

  if (left + tooltipW > window.innerWidth - 8) left = window.innerWidth - tooltipW - 8;
  if (left < 8) left = 8;
  if (rect.bottom + estimatedH > window.innerHeight) top = rect.top + window.scrollY - estimatedH - 8;

  tooltip.style.cssText = `top:${top}px;left:${left}px;bottom:auto;width:${tooltipW}px;max-width:340px;`;
}

function getTooltip() { return document.getElementById('verse-tooltip'); }

function showTooltipLoading(anchor, refText) {
  const tooltip = getTooltip();
  if (!tooltip) return;
  tooltip.querySelector('.verse-tooltip-ref').textContent = refText;
  tooltip.querySelector('.verse-tooltip-text').textContent = 'Carregando...';
  tooltip.querySelector('.verse-tooltip-badge').textContent = '';
  tooltip.classList.remove('visible', 'tooltip-error');
  positionTooltip(tooltip, anchor);
  requestAnimationFrame(() => tooltip.classList.add('visible'));
}

function updateTooltipContent(verse) {
  const tooltip = getTooltip();
  if (!tooltip) return;
  tooltip.querySelector('.verse-tooltip-text').textContent = verse.text;
  tooltip.querySelector('.verse-tooltip-badge').textContent = verse.translation;
  if (verse.error) tooltip.classList.add('tooltip-error');
}

function hideTooltip() {
  const t = getTooltip();
  if (t) t.classList.remove('visible', 'tooltip-error');
}

let tooltipHideTimer = null;
let tooltipInitialized = false;

function initVerseTooltips() {
  if (tooltipInitialized) return;
  tooltipInitialized = true;

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') hideTooltip();
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.devo-ref-item') && !e.target.closest('#verse-tooltip')) {
      hideTooltip();
    }
  });

  document.addEventListener('mouseover', async (e) => {
    const ref = e.target.closest('.devo-ref-item');
    if (!ref) return;
    clearTimeout(tooltipHideTimer);
    const refText = ref.textContent.trim();
    showTooltipLoading(ref, refText);
    const verse = await fetchVerse(refText);
    updateTooltipContent(verse);
  });

  document.addEventListener('mouseout', (e) => {
    if (!e.target.closest('.devo-ref-item')) return;
    const tooltip = getTooltip();
    tooltipHideTimer = setTimeout(() => {
      if (tooltip && !tooltip.matches(':hover')) hideTooltip();
    }, 250);
  });

  const tooltip = getTooltip();
  if (tooltip) {
    tooltip.addEventListener('mouseenter', () => clearTimeout(tooltipHideTimer));
    tooltip.addEventListener('mouseleave', () => { tooltipHideTimer = setTimeout(hideTooltip, 150); });
  }

  document.addEventListener('touchstart', async (e) => {
    const ref = e.target.closest('.devo-ref-item');
    if (!ref) return;
    e.preventDefault();
    const refText = ref.textContent.trim();
    showTooltipLoading(ref, refText);
    const verse = await fetchVerse(refText);
    updateTooltipContent(verse);
  }, { passive: false });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initVerseTooltips);
} else {
  initVerseTooltips();
}
