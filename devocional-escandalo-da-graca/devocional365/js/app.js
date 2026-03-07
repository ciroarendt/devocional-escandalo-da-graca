// ========================================
// Devocional 365 — App Logic
// ========================================

(function () {
  'use strict';

  // State
  const state = {
    currentDay: 1,
    theme: localStorage.getItem('d365-theme') || 'light',
    favorites: JSON.parse(localStorage.getItem('d365-favorites') || '[]'),
    readDays: JSON.parse(localStorage.getItem('d365-read') || '[]'),
    calendarMonth: new Date().getMonth(),
    calendarYear: new Date().getFullYear(),
  };

  // DOM refs
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);

  const splash = $('#splash');
  const app = $('#app');
  const readerContent = $('#reader-content');
  const topbarTitle = $('#topbar-title');
  const btnMenu = $('#btn-menu');
  const btnFavorite = $('#btn-favorite');
  const btnTheme = $('#btn-theme');
  const btnPrev = $('#btn-prev');
  const btnNext = $('#btn-next');
  const daySlider = $('#day-slider');
  const dayLabel = $('#day-label');
  const sidebar = $('#sidebar');
  const sidebarOverlay = $('#sidebar-overlay');
  const btnCloseMenu = $('#btn-close-menu');
  const searchInput = $('#search-input');
  const iconMoon = $('#icon-moon');
  const iconSun = $('#icon-sun');

  // ========================================
  // Initialization
  // ========================================

  function init() {
    applyTheme(state.theme);
    goToTodayOrSaved();
    bindEvents();

    // Hide splash after short delay
    setTimeout(() => {
      splash.classList.add('fade-out');
      app.classList.remove('hidden');
      setTimeout(() => splash.style.display = 'none', 600);
    }, 1500);
  }

  function goToTodayOrSaved() {
    const saved = localStorage.getItem('d365-lastDay');
    if (saved) {
      navigateTo(parseInt(saved));
    } else {
      navigateToToday();
    }
  }

  function navigateToToday() {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 0);
    const diff = now - start;
    const dayOfYear = Math.floor(diff / 86400000);
    const clamped = Math.max(1, Math.min(365, dayOfYear));
    navigateTo(clamped);
  }

  // ========================================
  // Navigation
  // ========================================

  function navigateTo(day) {
    if (day < 1 || day > 365) return;
    state.currentDay = day;
    localStorage.setItem('d365-lastDay', day);

    // Mark as read
    if (!state.readDays.includes(day)) {
      state.readDays.push(day);
      localStorage.setItem('d365-read', JSON.stringify(state.readDays));
    }

    renderDevotional(day);
    updateUI(day);
  }

  function renderDevotional(day) {
    const devo = DEVOTIONALS[day - 1];
    if (!devo) return;

    readerContent.classList.add('fade-out');

    setTimeout(() => {
      const html = `
        <div class="devo-day-badge">
          <span></span> Dia ${devo.day} de 365
        </div>
        <div class="devo-theme-tag">${devo.theme}</div>
        <h1 class="devo-title">${devo.title}</h1>
        <div class="devo-date">${devo.date_label}</div>

        <div class="devo-verse">
          <p class="devo-verse-text">${devo.verse_text}</p>
          <cite class="devo-verse-ref">${devo.verse_ref}</cite>
        </div>

        <div class="devo-body">
          ${devo.paragraphs.map(p => `<p>${p}</p>`).join('')}
        </div>

        <div class="devo-divider"><span>✦</span></div>

        <div class="devo-refs">
          <h4>Saiba Mais</h4>
          <div class="devo-refs-list">
            ${devo.references.map(r => `<span class="devo-ref-item">${r}</span>`).join('')}
          </div>
        </div>

        <div class="devo-prayer">
          <h4>Declaração de Fé</h4>
          <p>${devo.prayer}<span class="amen">Amém.</span></p>
        </div>

        <div class="devo-journal">
          <div class="devo-journal-title">Registro Pessoal</div>
          <div class="journal-box">
            <div class="journal-box-header">
              <span class="journal-box-number">1</span>
              <label class="journal-label">Registre 3 coisas que você aprendeu hoje</label>
            </div>
            <textarea class="journal-textarea" data-key="learned" placeholder="1. &#10;2. &#10;3. "></textarea>
          </div>
          <div class="journal-box">
            <div class="journal-box-header">
              <span class="journal-box-number">2</span>
              <label class="journal-label">O que o Espírito Santo te falou hoje</label>
            </div>
            <textarea class="journal-textarea" data-key="spirit" placeholder="Escreva aqui o que o Espírito Santo está falando ao seu coração..."></textarea>
          </div>
          <div class="journal-box">
            <div class="journal-box-header">
              <span class="journal-box-number">3</span>
              <label class="journal-label">Resuma este devocional em 3 palavras chaves</label>
            </div>
            <textarea class="journal-textarea" data-key="keywords" placeholder="Ex: Graça, Identidade, Missão"></textarea>
          </div>
        </div>
      `;

      readerContent.innerHTML = html;

      // Load and wire journal entries
      const journalData = loadJournalEntries(day);
      readerContent.querySelectorAll('.journal-textarea').forEach(textarea => {
        const key = textarea.dataset.key;
        if (journalData[key]) textarea.value = journalData[key];
        textarea.addEventListener('input', () => {
          saveJournalEntry(day, key, textarea.value);
        });
      });

      readerContent.classList.remove('fade-out');
      readerContent.classList.add('fade-in');

      // Scroll to top
      window.scrollTo({ top: 0, behavior: 'smooth' });

      setTimeout(() => readerContent.classList.remove('fade-in'), 300);
    }, 150);
  }

  function updateUI(day) {
    topbarTitle.textContent = `Dia ${day} de 365`;
    daySlider.value = day;
    dayLabel.textContent = `${day}/365`;

    // Favorite button
    if (state.favorites.includes(day)) {
      btnFavorite.classList.add('is-favorite');
    } else {
      btnFavorite.classList.remove('is-favorite');
    }

    // Prev/next buttons
    btnPrev.disabled = day <= 1;
    btnNext.disabled = day >= 365;
  }

  // ========================================
  // Theme
  // ========================================

  function applyTheme(theme) {
    state.theme = theme;
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
      iconMoon.classList.add('hidden');
      iconSun.classList.remove('hidden');
    } else {
      document.documentElement.removeAttribute('data-theme');
      iconMoon.classList.remove('hidden');
      iconSun.classList.add('hidden');
    }
    localStorage.setItem('d365-theme', theme);
  }

  function toggleTheme() {
    applyTheme(state.theme === 'dark' ? 'light' : 'dark');
  }

  // ========================================
  // Favorites
  // ========================================

  function toggleFavorite() {
    const day = state.currentDay;
    const idx = state.favorites.indexOf(day);
    if (idx >= 0) {
      state.favorites.splice(idx, 1);
    } else {
      state.favorites.push(day);
    }
    localStorage.setItem('d365-favorites', JSON.stringify(state.favorites));
    updateUI(day);
  }

  function showFavorites() {
    const list = $('#favorites-list');
    if (state.favorites.length === 0) {
      list.innerHTML = '<p class="fav-empty">Nenhum favorito ainda. Toque no coração para favoritar um devocional.</p>';
    } else {
      const sorted = [...state.favorites].sort((a, b) => a - b);
      list.innerHTML = sorted.map(day => {
        const devo = DEVOTIONALS[day - 1];
        return `<div class="fav-item" data-day="${day}">
          <div class="fav-day-num">${day}</div>
          <div class="fav-title">${devo.title}</div>
        </div>`;
      }).join('');

      list.querySelectorAll('.fav-item').forEach(el => {
        el.addEventListener('click', () => {
          navigateTo(parseInt(el.dataset.day));
          closeModal('favorites');
          closeSidebar();
        });
      });
    }
    openModal('favorites');
  }

  // ========================================
  // Progress
  // ========================================

  function showProgress() {
    const total = 365;
    const read = state.readDays.length;
    const percent = Math.round((read / total) * 100);
    const circumference = 2 * Math.PI * 58;
    const offset = circumference - (percent / 100) * circumference;

    const streakDays = calculateStreak();

    const content = $('#progress-content');
    content.innerHTML = `
      <div class="progress-circle-wrap">
        <svg width="140" height="140" viewBox="0 0 140 140">
          <circle class="progress-circle-bg" cx="70" cy="70" r="58"/>
          <circle class="progress-circle-fill" cx="70" cy="70" r="58"
            stroke-dasharray="${circumference}"
            stroke-dashoffset="${offset}"/>
        </svg>
        <div class="progress-percent">
          <strong>${percent}%</strong>
          <span>completo</span>
        </div>
      </div>
      <div class="progress-stats">
        <div class="progress-stat">
          <strong>${read}</strong>
          <span>Lidos</span>
        </div>
        <div class="progress-stat">
          <strong>${total - read}</strong>
          <span>Restantes</span>
        </div>
        <div class="progress-stat">
          <strong>${streakDays}</strong>
          <span>Sequência</span>
        </div>
      </div>
    `;
    openModal('progress');
  }

  function calculateStreak() {
    if (state.readDays.length === 0) return 0;
    const sorted = [...state.readDays].sort((a, b) => b - a);
    let streak = 1;
    for (let i = 1; i < sorted.length; i++) {
      if (sorted[i] === sorted[i - 1] - 1) {
        streak++;
      } else {
        break;
      }
    }
    return streak;
  }

  // ========================================
  // Calendar
  // ========================================

  function showCalendar() {
    renderCalendar();
    openModal('calendar');
  }

  function renderCalendar() {
    const monthTitle = $('#cal-month-title');
    const daysGrid = $('#cal-days');
    const months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
      'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    const monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    const m = state.calendarMonth;
    monthTitle.textContent = months[m];

    // Calculate first day number of this month
    let firstDayOfYear = 0;
    for (let i = 0; i < m; i++) {
      firstDayOfYear += monthDays[i];
    }

    // First day of month (weekday): we use 2025 as reference year
    const firstDate = new Date(2025, m, 1);
    const startWeekday = firstDate.getDay(); // 0=Sun

    // Now of year
    const now = new Date();
    const startOfYear = new Date(now.getFullYear(), 0, 0);
    const todayDayOfYear = Math.floor((now - startOfYear) / 86400000);

    let html = '';

    // Empty cells before first day
    for (let i = 0; i < startWeekday; i++) {
      html += '<div class="cal-day empty"></div>';
    }

    // Day cells
    for (let d = 1; d <= monthDays[m]; d++) {
      const dayOfYear = firstDayOfYear + d;
      const isToday = dayOfYear === todayDayOfYear;
      const isRead = state.readDays.includes(dayOfYear);
      const isCurrent = dayOfYear === state.currentDay;

      let cls = 'cal-day';
      if (isToday) cls += ' today';
      else if (isRead) cls += ' read';
      if (isCurrent) cls += ' current';

      html += `<div class="${cls}" data-day="${dayOfYear}">${d}</div>`;
    }

    daysGrid.innerHTML = html;

    daysGrid.querySelectorAll('.cal-day:not(.empty)').forEach(el => {
      el.addEventListener('click', () => {
        navigateTo(parseInt(el.dataset.day));
        closeModal('calendar');
      });
    });
  }

  // ========================================
  // Search
  // ========================================

  function performSearch(query) {
    if (!query || query.length < 2) return;

    const q = query.toLowerCase();
    const results = DEVOTIONALS.filter(d =>
      d.title.toLowerCase().includes(q) ||
      d.verse_ref.toLowerCase().includes(q) ||
      d.theme.toLowerCase().includes(q) ||
      d.paragraphs.some(p => p.toLowerCase().includes(q))
    ).slice(0, 30);

    const container = $('#search-results');
    if (results.length === 0) {
      container.innerHTML = '<p class="search-empty">Nenhum resultado encontrado.</p>';
    } else {
      container.innerHTML = results.map(d => `
        <div class="search-item" data-day="${d.day}">
          <div class="search-item-day">Dia ${d.day} — ${d.month}</div>
          <div class="search-item-title">${d.title}</div>
        </div>
      `).join('');

      container.querySelectorAll('.search-item').forEach(el => {
        el.addEventListener('click', () => {
          navigateTo(parseInt(el.dataset.day));
          closeModal('search');
          closeSidebar();
        });
      });
    }

    openModal('search');
  }

  // ========================================
  // Sidebar
  // ========================================

  function openSidebar() {
    sidebar.classList.add('open');
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
  }

  // ========================================
  // Modals
  // ========================================

  function openModal(name) {
    $(`#${name}-modal`).classList.remove('hidden');
  }

  function closeModal(name) {
    $(`#${name}-modal`).classList.add('hidden');
  }

  // ========================================
  // Touch / Swipe
  // ========================================

  let touchStartX = 0;
  let touchEndX = 0;

  function handleSwipe() {
    const diff = touchStartX - touchEndX;
    if (Math.abs(diff) > 60) {
      if (diff > 0) {
        navigateTo(state.currentDay + 1);
      } else {
        navigateTo(state.currentDay - 1);
      }
    }
  }

  // ========================================
  // Event Bindings
  // ========================================

  function bindEvents() {
    // Top bar
    btnMenu.addEventListener('click', openSidebar);
    btnFavorite.addEventListener('click', toggleFavorite);
    btnTheme.addEventListener('click', toggleTheme);

    // Navigation
    btnPrev.addEventListener('click', () => navigateTo(state.currentDay - 1));
    btnNext.addEventListener('click', () => navigateTo(state.currentDay + 1));

    daySlider.addEventListener('input', () => {
      dayLabel.textContent = `${daySlider.value}/365`;
    });
    daySlider.addEventListener('change', () => {
      navigateTo(parseInt(daySlider.value));
    });

    // Sidebar
    sidebarOverlay.addEventListener('click', closeSidebar);
    btnCloseMenu.addEventListener('click', closeSidebar);

    // Sidebar items
    $$('.sidebar-item[data-action]').forEach(btn => {
      btn.addEventListener('click', () => {
        const action = btn.dataset.action;
        closeSidebar();
        switch (action) {
          case 'today': navigateToToday(); break;
          case 'calendar': showCalendar(); break;
          case 'favorites': showFavorites(); break;
          case 'progress': showProgress(); break;
        }
      });
    });

    // Theme items in sidebar
    $$('.theme-item[data-month]').forEach(btn => {
      btn.addEventListener('click', () => {
        const monthDays = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
        const m = parseInt(btn.dataset.month);
        navigateTo(monthDays[m] + 1);
        closeSidebar();
      });
    });

    // Search
    let searchTimeout;
    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        performSearch(searchInput.value.trim());
      }, 400);
    });

    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        performSearch(searchInput.value.trim());
      }
    });

    // Modal close buttons
    $$('[data-close]').forEach(btn => {
      btn.addEventListener('click', () => {
        closeModal(btn.dataset.close);
      });
    });

    // Calendar navigation
    $('#cal-prev').addEventListener('click', () => {
      state.calendarMonth--;
      if (state.calendarMonth < 0) state.calendarMonth = 11;
      renderCalendar();
    });

    $('#cal-next').addEventListener('click', () => {
      state.calendarMonth++;
      if (state.calendarMonth > 11) state.calendarMonth = 0;
      renderCalendar();
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      switch (e.key) {
        case 'ArrowLeft': navigateTo(state.currentDay - 1); break;
        case 'ArrowRight': navigateTo(state.currentDay + 1); break;
        case 'Home': navigateTo(1); break;
        case 'End': navigateTo(365); break;
        case 'd': toggleTheme(); break;
        case 'f': toggleFavorite(); break;
        case 't': navigateToToday(); break;
      }
    });

    // Touch swipe
    const reader = $('#reader');
    reader.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    reader.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    }, { passive: true });
  }

  // ========================================
  // ========================================
  // Journal / Personal Register
  // ========================================

  function saveJournalEntry(day, key, value) {
    const storageKey = `d365-journal-${day}`;
    const existing = JSON.parse(localStorage.getItem(storageKey) || '{}');
    existing[key] = value;
    localStorage.setItem(storageKey, JSON.stringify(existing));
  }

  function loadJournalEntries(day) {
    const storageKey = `d365-journal-${day}`;
    return JSON.parse(localStorage.getItem(storageKey) || '{}');
  }

  // ========================================
  // Start
  // ========================================

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
