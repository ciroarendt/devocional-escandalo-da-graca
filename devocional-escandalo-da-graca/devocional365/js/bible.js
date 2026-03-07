/**
 * bible.js — Integração com Bible API + Sistema de Tooltips
 * Devocional 365 · Escândalo da Graça
 */

// ─── Mapa de livros PT-BR → nome aceito pela API ───────────────────────────
const BOOK_MAP = {
  'genesis': 'genesis', 'gênesis': 'genesis',
  'exodo': 'exodus', 'êxodo': 'exodus',
  'levitico': 'leviticus', 'levítico': 'leviticus',
  'numeros': 'numbers', 'números': 'numbers',
  'deuteronomio': 'deuteronomy', 'deuteronômio': 'deuteronomy',
  'josue': 'joshua', 'josué': 'joshua',
  'juizes': 'judges', 'juízes': 'judges',
  'rute': 'ruth',
  '1 samuel': '1 samuel', '1samuel': '1 samuel',
  '2 samuel': '2 samuel', '2samuel': '2 samuel',
  '1 reis': '1 kings', '1reis': '1 kings',
  '2 reis': '2 kings', '2reis': '2 kings',
  '1 cronicas': '1 chronicles', '1 crônicas': '1 chronicles',
  '2 cronicas': '2 chronicles', '2 crônicas': '2 chronicles',
  'esdras': 'ezra',
  'neemias': 'nehemiah',
  'ester': 'esther',
  'jo': 'job', 'jó': 'job',
  'salmos': 'psalms', 'salmo': 'psalms',
  'proverbios': 'proverbs', 'provérbios': 'proverbs',
  'eclesiastes': 'ecclesiastes',
  'cantares': 'song of solomon',
  'isaias': 'isaiah', 'isaías': 'isaiah',
  'jeremias': 'jeremiah',
  'lamentacoes': 'lamentations', 'lamentações': 'lamentations',
  'ezequiel': 'ezekiel',
  'daniel': 'daniel',
  'oseias': 'hosea', 'oséias': 'hosea',
  'joel': 'joel',
  'amos': 'amos', 'amós': 'amos',
  'obadias': 'obadiah',
  'jonas': 'jonah',
  'miqueias': 'micah',
  'naum': 'nahum',
  'habacuque': 'habakkuk',
  'sofonias': 'zephaniah',
  'ageu': 'haggai',
  'zacarias': 'zechariah',
  'malaquias': 'malachi',
  'mateus': 'matthew',
  'marcos': 'mark',
  'lucas': 'luke',
  'joao': 'john', 'joão': 'john',
  'atos': 'acts',
  'romanos': 'romans',
  '1 corintios': '1 corinthians', '1 coríntios': '1 corinthians',
  '2 corintios': '2 corinthians', '2 coríntios': '2 corinthians',
  'galatas': 'galatians', 'gálatas': 'galatians',
  'efesios': 'ephesians', 'efésios': 'ephesians',
  'filipenses': 'philippians',
  'colossenses': 'colossians',
  '1 tessalonicenses': '1 thessalonians',
  '2 tessalonicenses': '2 thessalonians',
  '1 timoteo': '1 timothy', '1 timóteo': '1 timothy',
  '2 timoteo': '2 timothy', '2 timóteo': '2 timothy',
  'tito': 'titus',
  'filemom': 'philemon',
  'hebreus': 'hebrews',
  'tiago': 'james',
  '1 pedro': '1 peter',
  '2 pedro': '2 peter',
  '1 joao': '1 john', '1 joão': '1 john',
  '2 joao': '2 john', '2 joão': '2 john',
  '3 joao': '3 john', '3 joão': '3 john',
  'judas': 'jude',
  'apocalipse': 'revelation'
};

const verseCache = new Map();

function normalizeReference(refText) {
  const cleaned = refText.trim().toLowerCase();
  let bestMatch = null;
  let bestLen = 0;

  for (const [ptName, apiName] of Object.entries(BOOK_MAP)) {
    if (cleaned.startsWith(ptName) && ptName.length > bestLen) {
      bestMatch = { ptName, apiName };
      bestLen = ptName.length;
    }
  }

  if (!bestMatch) return refText;
  const rest = cleaned.slice(bestMatch.ptName.length).trim();
  return `${bestMatch.apiName} ${rest}`;
}

async function fetchVerse(refText) {
  const cacheKey = refText.trim();
  if (verseCache.has(cacheKey)) return verseCache.get(cacheKey);

  const normalized = normalizeReference(cacheKey);

  try {
    const url = `https://bible-api.com/${encodeURIComponent(normalized)}?translation=almeida`;
    const res = await fetch(url, { signal: AbortSignal.timeout(6000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    let text = '';
    if (data.text) {
      text = data.text.trim().replace(/\n/g, ' ');
    } else if (data.verses && data.verses.length > 0) {
      text = data.verses.map(v => v.text.trim()).join(' ');
    } else {
      text = 'Versículo não disponível nesta tradução.';
    }

    const result = { text, ref: data.reference || cacheKey, translation: 'Almeida Revisada' };
    verseCache.set(cacheKey, result);
    return result;
  } catch (err) {
    return { text: 'Não foi possível carregar o versículo. Verifique sua conexão.', ref: cacheKey, translation: '', error: true };
  }
}

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
