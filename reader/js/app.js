/**
 * Prajñā Reader Master Controller (v3 - Optimized Reading Edition)
 */

import { parseMarkdown, renderOpeningRitual, renderClosingRitual } from './parser.js?v=9';
import { 
  loadPreferences, 
  savePreferences, 
  updatePreference, 
  saveBookmark, 
  removeBookmark, 
  saveScrollPosition, 
  getScrollPosition,
  toggleQuyenCompleted,
  isQuyenCompleted,
  getCompletedQuyens
} from './storage.js?v=9';
import { filterQuyenList } from './search.js?v=9';
import { 
  playBell, 
  playMokugyo, 
  startMokugyoMetronome, 
  stopMokugyoMetronome, 
  isMetronomeRunning 
} from './audio.js?v=9';
import { searchFullText, fetchQuyenExcerpts } from './search_fulltext.js?v=9';
import { loadGlossary, searchGlossary, renderGlossaryCard, renderGlossaryModalContent } from './glossary.js?v=9';

class PrajnaApp {
  constructor() {
    this.tocData = null;
    this.quyenList = [];
    this.filteredList = [];
    this.currentQuyenNum = 1;
    this.catalogMode = 'tap'; // 'tap' | 'hoi' | 'fullsearch' | 'glossary'
    this.activeTapId = 0;     // 0 = Tất cả
    this.activeHoiId = 0;     // 0 = Tất cả
    this.activeGlossaryCategory = 'Tất cả';
    this.glossaryCategories = ['Tất cả', 'Bát Nhã Căn Bản', 'Tánh Không', 'Bồ Tát Đạo', 'Pháp Tướng & Nhận Thức', 'Cứu Cánh'];
    this.prefs = loadPreferences();
    this.scrollSaveTimer = null;

    // Auto-scroll state
    this.isAutoScrolling = false;
    this.isAutoScrollPaused = false;
    this.autoScrollSpeed = 1; // 1 = chậm, 2 = vừa, 3 = nhanh
    this.autoScrollRAF = null;

    // TAP Definitions for 11 Volumes
    this.tapMeta = [
      { id: 1, name: 'Tập 01', range: 'Q.01 – 51', count: 51 },
      { id: 2, name: 'Tập 02', range: 'Q.52 – 103', count: 52 },
      { id: 3, name: 'Tập 03', range: 'Q.104 – 168', count: 65 },
      { id: 4, name: 'Tập 04', range: 'Q.169 – 220', count: 52 },
      { id: 5, name: 'Tập 05', range: 'Q.221 – 284', count: 64 },
      { id: 6, name: 'Tập 06', range: 'Q.285 – 336', count: 52 },
      { id: 7, name: 'Tập 07', range: 'Q.337 – 389', count: 53 },
      { id: 8, name: 'Tập 08', range: 'Q.390 – 435', count: 46 },
      { id: 9, name: 'Tập 09', range: 'Q.436 – 498', count: 63 },
      { id: 10, name: 'Tập 10', range: 'Q.499 – 547', count: 49 },
      { id: 11, name: 'Tập 11', range: 'Q.548 – 600', count: 53 }
    ];

    // DOM Elements
    this.el = {
      sidebar: document.getElementById('sidebar'),
      sidebarBackdrop: document.getElementById('sidebar-backdrop'),
      sidebarToggleBtn: document.getElementById('btn-sidebar-toggle'),
      quyenListContainer: document.getElementById('quyen-list'),
      searchInput: document.getElementById('search-input'),
      searchClearBtn: document.getElementById('search-clear'),
      searchGoBtn: document.getElementById('search-go-btn'),
      filterChipsBar: document.getElementById('filter-chips-bar'),
      tabTap: document.getElementById('tab-tap'),
      tabHoi: document.getElementById('tab-hoi'),
      tabFullsearch: document.getElementById('tab-fullsearch'),
      tabGlossary: document.getElementById('tab-glossary'),
      fullsearchContainer: document.getElementById('fullsearch-container'),
      fullsearchStatus: document.getElementById('fullsearch-status'),
      fullsearchResults: document.getElementById('fullsearch-results'),
      glossaryContainer: document.getElementById('glossary-container'),
      glossaryCategoryFilter: document.getElementById('glossary-category-filter'),
      glossaryList: document.getElementById('glossary-list'),
      glossaryBackdrop: document.getElementById('glossary-backdrop'),
      glossaryModal: document.getElementById('glossary-modal'),
      glossaryModalInner: document.getElementById('glossary-modal-inner'),
      btnCloseGlossaryModal: document.getElementById('btn-close-glossary-modal'),

      contentArea: document.getElementById('content-area'),
      contentInner: document.getElementById('content-inner'),
      progressBar: document.getElementById('reading-progress-bar'),
      headerTitleBadge: document.getElementById('header-title-badge'),
      btnPrevQuyenTop: document.getElementById('btn-prev-quyen-top'),
      btnNextQuyenTop: document.getElementById('btn-next-quyen-top'),
      
      // Quick Controls on Header
      quickThemeDots: document.querySelectorAll('.quick-theme-dot'),
      btnFontMinusTop: document.getElementById('btn-font-minus-top'),
      btnFontPlusTop: document.getElementById('btn-font-plus-top'),
      fontSizeValTop: document.getElementById('font-size-val-top'),
      btnAutoscroll: document.getElementById('btn-autoscroll'),

      // Floating Auto-Scroll Bar
      autoScrollBar: document.getElementById('autoscroll-bar'),
      autoScrollStatusText: document.getElementById('autoscroll-status-text'),
      btnAutoScrollPause: document.getElementById('btn-autoscroll-pause'),
      btnAutoScrollClose: document.getElementById('btn-autoscroll-close'),
      speedBtns: document.querySelectorAll('.speed-btn'),

      // Audio & Modals
      btnBell: document.getElementById('btn-bell'),
      btnMokugyo: document.getElementById('btn-mokugyo'),
      btnSettings: document.getElementById('btn-settings'),
      btnZen: document.getElementById('btn-zen'),
      btnZenExit: document.getElementById('btn-zen-exit'),
      btnBookmark: document.getElementById('btn-bookmark'),
      
      settingsDrawer: document.getElementById('settings-drawer'),
      drawerCloseBtn: document.getElementById('btn-drawer-close'),
      drawerBackdrop: document.getElementById('drawer-backdrop'),
      themeBtns: document.querySelectorAll('.theme-btn, .theme-btn-card'),
      fontFamilyBtns: document.querySelectorAll('.font-family-btn'),
      bookmarksList: document.getElementById('bookmarks-list'),

      // Drawer Large Senior Controls
      btnFontMinusLarge: document.getElementById('btn-font-minus'),
      btnFontPlusLarge: document.getElementById('btn-font-plus'),
      fontSizeValLarge: document.getElementById('font-size-val'),
      sheetBtnBell: document.getElementById('sheet-btn-bell'),
      sheetBtnMokugyo: document.getElementById('sheet-btn-mokugyo'),
      btnShareLink: document.getElementById('btn-share-link'),

      // Mobile Bottom Bar Navigation
      mBtnToc: document.getElementById('m-btn-toc'),
      mBtnPrev: document.getElementById('m-btn-prev'),
      mBtnAutoscroll: document.getElementById('m-btn-autoscroll'),
      mBtnNext: document.getElementById('m-btn-next'),
      mBtnDisplay: document.getElementById('m-btn-display'),
      btnSidebarClose: document.getElementById('btn-sidebar-close'),

      // Liturgy, Practice Tracker & Metronome
      toggleRitual: document.getElementById('toggle-ritual'),
      toggleMetronome: document.getElementById('toggle-metronome'),
      btnAutoscrollMetronome: document.getElementById('btn-autoscroll-metronome'),
      trackerCount: document.getElementById('tracker-count'),
      trackerPct: document.getElementById('tracker-pct'),
      trackerProgressFill: document.getElementById('tracker-progress-fill'),
      trackerSummaryPill: document.getElementById('tracker-summary-pill')
    };
  }

  async init() {
    this.applyPreferences();
    this.bindEvents();

    if (window.innerWidth <= 900) {
      this.el.sidebar.classList.add('closed');
      if (this.el.sidebarBackdrop) {
        this.el.sidebarBackdrop.classList.remove('active');
      }
    }

    try {
      const resp = await fetch('data/toc.json');
      if (!resp.ok) throw new Error('Không thể tải mục lục toc.json');
      this.tocData = await resp.json();
      this.quyenList = this.tocData.quyen_list || [];
      this.filteredList = [...this.quyenList];

      this.renderFilterChips();
      this.renderSidebarList();

      // Check URL hash for initial Quyển
      const hash = window.location.hash;
      const match = hash.match(/#quyen-(\d+)/);
      let initialQuyen = this.prefs.currentQuyen || 1;
      if (match) {
        const qFromHash = parseInt(match[1], 10);
        if (qFromHash >= 1 && qFromHash <= 600) {
          initialQuyen = qFromHash;
        }
      }

      await this.loadQuyen(initialQuyen);
      this.registerServiceWorker();
    } catch (err) {
      console.error('Lỗi khởi tạo ứng dụng:', err);
      this.el.contentInner.innerHTML = `
        <div class="loading-indicator">
          <p style="color: var(--accent); font-weight: bold;">Không thể tải dữ liệu kinh văn.</p>
          <p style="font-size: 0.9rem;">Vui lòng kiểm tra lại đường dẫn máy chủ cục bộ.</p>
        </div>
      `;
    }
  }

  applyPreferences() {
    document.documentElement.setAttribute('data-theme', this.prefs.theme);
    document.documentElement.setAttribute('data-font', this.prefs.fontFamily || 'serif');
    
    // Default comfortable font size: 21px
    const currentSize = this.prefs.fontSize || 21;
    document.documentElement.style.setProperty('--font-size', `${currentSize}px`);
    document.documentElement.style.setProperty('--line-height', this.prefs.lineHeight || '1.9');

    if (this.el.fontSizeValTop) {
      this.el.fontSizeValTop.textContent = `${currentSize}px`;
    }
    if (this.el.fontSizeValLarge) {
      this.el.fontSizeValLarge.textContent = `${currentSize}px`;
    }

    if (this.prefs.zenMode) {
      document.body.classList.add('zen-mode');
    }

    // Update active quick theme dot
    this.el.quickThemeDots.forEach(dot => {
      dot.classList.toggle('active', dot.dataset.theme === this.prefs.theme);
    });

    // Update theme buttons in drawer
    this.el.themeBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.theme === this.prefs.theme);
    });

    if (this.el.toggleRitual) {
      this.el.toggleRitual.checked = this.prefs.showRitual !== false;
    }
    if (this.el.toggleMetronome) {
      this.el.toggleMetronome.checked = !!this.prefs.metronomeEnabled;
    }
    if (this.el.btnAutoscrollMetronome) {
      this.el.btnAutoscrollMetronome.textContent = this.prefs.metronomeEnabled ? '🪘 Mõ: Bật' : '🪘 Mõ: Tắt';
      this.el.btnAutoscrollMetronome.classList.toggle('active', !!this.prefs.metronomeEnabled);
    }

    this.updateTrackerUI();
    this.renderBookmarksList();
  }

  bindEvents() {
    // 1. Sidebar toggle
    this.el.sidebarToggleBtn.addEventListener('click', () => {
      const isClosed = this.el.sidebar.classList.toggle('closed');
      if (this.el.sidebarBackdrop) {
        this.el.sidebarBackdrop.classList.toggle('active', !isClosed && window.innerWidth <= 900);
      }
    });

    if (this.el.sidebarBackdrop) {
      this.el.sidebarBackdrop.addEventListener('click', () => {
        this.el.sidebar.classList.add('closed');
        this.el.sidebarBackdrop.classList.remove('active');
      });
    }

    // 2. Audio Chime (Bell & Mokugyo)
    if (this.el.btnBell) {
      this.el.btnBell.addEventListener('click', () => playBell());
    }
    if (this.el.btnMokugyo) {
      this.el.btnMokugyo.addEventListener('click', () => playMokugyo());
    }

    // 3. Header Prev / Next Navigation
    if (this.el.btnPrevQuyenTop) {
      this.el.btnPrevQuyenTop.addEventListener('click', () => {
        if (this.currentQuyenNum > 1) this.loadQuyen(this.currentQuyenNum - 1);
      });
    }
    if (this.el.btnNextQuyenTop) {
      this.el.btnNextQuyenTop.addEventListener('click', () => {
        if (this.currentQuyenNum < 600) this.loadQuyen(this.currentQuyenNum + 1);
      });
    }

    // 4. Quick Theme Switcher Dots (Header)
    this.el.quickThemeDots.forEach(dot => {
      dot.addEventListener('click', () => {
        const theme = dot.dataset.theme;
        this.prefs.theme = theme;
        updatePreference('theme', theme);
        this.applyPreferences();
      });
    });

    // 5. Font Size Steppers (Header & Drawer Large Controls)
    const updateFontSize = (delta) => {
      let size = (this.prefs.fontSize || 21) + delta;
      if (size >= 16 && size <= 36) {
        this.prefs.fontSize = size;
        updatePreference('fontSize', size);
        this.applyPreferences();
      }
    };

    if (this.el.btnFontMinusTop) {
      this.el.btnFontMinusTop.addEventListener('click', () => updateFontSize(-1));
    }
    if (this.el.btnFontPlusTop) {
      this.el.btnFontPlusTop.addEventListener('click', () => updateFontSize(1));
    }
    if (this.el.btnFontMinusLarge) {
      this.el.btnFontMinusLarge.addEventListener('click', () => updateFontSize(-1));
    }
    if (this.el.btnFontPlusLarge) {
      this.el.btnFontPlusLarge.addEventListener('click', () => updateFontSize(1));
    }

    // 6. Unified Smart Search & Jump
    const parseQuyenNumber = (val) => {
      if (!val) return null;
      const match = val.trim().match(/^(?:quyen|q|quyển)?\s*(\d+)$/i);
      if (match) {
        const num = parseInt(match[1], 10);
        if (num >= 1 && num <= 600) return num;
      }
      return null;
    };

    const handleSmartJump = () => {
      const qNum = parseQuyenNumber(this.el.searchInput.value);
      if (qNum) {
        this.loadQuyen(qNum);
        this.el.searchInput.blur();
        if (window.innerWidth <= 900) {
          this.el.sidebar.classList.add('closed');
          if (this.el.sidebarBackdrop) this.el.sidebarBackdrop.classList.remove('active');
        }
      }
    };

    if (this.el.searchGoBtn) {
      this.el.searchGoBtn.addEventListener('click', handleSmartJump);
    }

    // 7. Catalog View Mode Tabs (11 Tập, 16 Hội, Tra Cứu Toàn Văn, Từ Điển Bát Nhã)
    if (this.el.tabTap) this.el.tabTap.addEventListener('click', () => this.setCatalogMode('tap'));
    if (this.el.tabHoi) this.el.tabHoi.addEventListener('click', () => this.setCatalogMode('hoi'));
    if (this.el.tabFullsearch) this.el.tabFullsearch.addEventListener('click', () => this.setCatalogMode('fullsearch'));
    if (this.el.tabGlossary) this.el.tabGlossary.addEventListener('click', () => this.setCatalogMode('glossary'));

    // Glossary Modal Close Handlers
    if (this.el.btnCloseGlossaryModal) {
      this.el.btnCloseGlossaryModal.addEventListener('click', () => this.closeGlossaryModal());
    }
    if (this.el.glossaryBackdrop) {
      this.el.glossaryBackdrop.addEventListener('click', () => this.closeGlossaryModal());
    }

    // 8. Auto-Scroll Controller
    if (this.el.btnAutoscroll) {
      this.el.btnAutoscroll.addEventListener('click', () => {
        this.toggleAutoScroll();
      });
    }

    if (this.el.btnAutoScrollPause) {
      this.el.btnAutoScrollPause.addEventListener('click', () => {
        this.toggleAutoScrollPause();
      });
    }

    if (this.el.btnAutoScrollClose) {
      this.el.btnAutoScrollClose.addEventListener('click', () => {
        this.stopAutoScroll();
      });
    }

    this.el.speedBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const spd = parseInt(btn.dataset.speed, 10);
        this.autoScrollSpeed = spd;
        this.el.speedBtns.forEach(b => b.classList.toggle('active', b === btn));
      });
    });

    // 9. Zen Mode
    if (this.el.btnZen) {
      this.el.btnZen.addEventListener('click', () => this.toggleZenMode(true));
    }
    if (this.el.btnZenExit) {
      this.el.btnZenExit.addEventListener('click', () => this.toggleZenMode(false));
    }

    // 10. Settings Drawer
    this.el.btnSettings.addEventListener('click', () => this.openSettingsDrawer());
    this.el.drawerCloseBtn.addEventListener('click', () => this.closeSettingsDrawer());
    this.el.drawerBackdrop.addEventListener('click', () => this.closeSettingsDrawer());

    // Audio Tools inside Drawer (Accessible on Mobile)
    if (this.el.sheetBtnBell) {
      this.el.sheetBtnBell.addEventListener('click', () => playBell());
    }
    if (this.el.sheetBtnMokugyo) {
      this.el.sheetBtnMokugyo.addEventListener('click', () => playMokugyo());
    }

    // 11. Mobile Bottom Bar Navigation
    if (this.el.mBtnToc) {
      this.el.mBtnToc.addEventListener('click', () => {
        const isClosed = this.el.sidebar.classList.toggle('closed');
        if (this.el.sidebarBackdrop) {
          this.el.sidebarBackdrop.classList.toggle('active', !isClosed);
        }
      });
    }

    if (this.el.btnSidebarClose) {
      this.el.btnSidebarClose.addEventListener('click', () => {
        this.el.sidebar.classList.add('closed');
        if (this.el.sidebarBackdrop) this.el.sidebarBackdrop.classList.remove('active');
      });
    }

    if (this.el.mBtnPrev) {
      this.el.mBtnPrev.addEventListener('click', () => {
        if (this.currentQuyenNum > 1) this.loadQuyen(this.currentQuyenNum - 1);
      });
    }

    if (this.el.mBtnNext) {
      this.el.mBtnNext.addEventListener('click', () => {
        if (this.currentQuyenNum < 600) this.loadQuyen(this.currentQuyenNum + 1);
      });
    }

    if (this.el.mBtnAutoscroll) {
      this.el.mBtnAutoscroll.addEventListener('click', () => {
        this.toggleAutoScroll();
      });
    }

    if (this.el.mBtnDisplay) {
      this.el.mBtnDisplay.addEventListener('click', () => {
        this.openSettingsDrawer();
      });
    }

    // Share link to current chapter
    if (this.el.btnShareLink) {
      this.el.btnShareLink.addEventListener('click', async () => {
        const shareUrl = `${window.location.origin}${window.location.pathname}#quyen-${this.currentQuyenNum}`;
        try {
          if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(shareUrl);
          } else {
            const tempInput = document.createElement('input');
            tempInput.value = shareUrl;
            document.body.appendChild(tempInput);
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);
          }
          this.showToast(`Đã sao chép liên kết Quyển ${this.currentQuyenNum}!`);
        } catch (e) {
          this.showToast(`Liên kết: ${shareUrl}`);
        }
      });
    }

    // Liturgy and Metronome settings
    if (this.el.toggleRitual) {
      this.el.toggleRitual.addEventListener('change', (e) => {
        this.prefs.showRitual = e.target.checked;
        updatePreference('showRitual', this.prefs.showRitual);
        this.loadQuyen(this.currentQuyenNum);
        this.showToast(this.prefs.showRitual ? 'Đã bật khung nghi thức khai kinh & hồi hướng' : 'Đã ẩn khung nghi thức');
      });
    }

    const setMetronomeState = (enabled) => {
      this.prefs.metronomeEnabled = enabled;
      updatePreference('metronomeEnabled', enabled);
      if (this.el.toggleMetronome) this.el.toggleMetronome.checked = enabled;
      if (this.el.btnAutoscrollMetronome) {
        this.el.btnAutoscrollMetronome.textContent = enabled ? '🪘 Mõ: Bật' : '🪘 Mõ: Tắt';
        this.el.btnAutoscrollMetronome.classList.toggle('active', enabled);
      }
      if (this.isAutoScrolling && !this.isAutoScrollPaused) {
        if (enabled) {
          startMokugyoMetronome(this.prefs.metronomeBpm || 45);
        } else {
          stopMokugyoMetronome();
        }
      }
      this.showToast(enabled ? 'Đã bật gõ mõ theo nhịp (45 nhịp/phút)' : 'Đã tắt gõ mõ');
    };

    if (this.el.toggleMetronome) {
      this.el.toggleMetronome.addEventListener('change', (e) => setMetronomeState(e.target.checked));
    }

    if (this.el.btnAutoscrollMetronome) {
      this.el.btnAutoscrollMetronome.addEventListener('click', () => setMetronomeState(!this.prefs.metronomeEnabled));
    }

    // Theme selector inside drawer
    this.el.themeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const theme = btn.dataset.theme;
        this.prefs.theme = theme;
        updatePreference('theme', theme);
        this.applyPreferences();
      });
    });

    // Font Family selector
    if (this.el.fontFamilyBtns) {
      this.el.fontFamilyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          const font = btn.dataset.font;
          this.prefs.fontFamily = font;
          updatePreference('fontFamily', font);
          this.applyPreferences();
          this.el.fontFamilyBtns.forEach(b => b.classList.toggle('active', b === btn));
        });
      });
    }

    // Bookmark
    if (this.el.btnBookmark) {
      this.el.btnBookmark.addEventListener('click', () => {
        const scrollPercent = this.getScrollPercent();
        const currentMeta = this.quyenList.find(q => q.quyen === this.currentQuyenNum);
        const title = currentMeta ? `Quyển ${currentMeta.quyen} - ${currentMeta.pham.split('&')[0].trim()}` : `Quyển ${this.currentQuyenNum}`;
        saveBookmark(this.currentQuyenNum, scrollPercent, title);
        this.renderBookmarksList();
        this.showToast(`Đã đánh dấu Quyển ${this.currentQuyenNum}`);
      });
    }

    // Search Input with Smart Jump & Full-Text Search
    let searchDebounceTimer = null;
    this.el.searchInput.addEventListener('input', (e) => {
      const q = e.target.value;
      this.el.searchClearBtn.classList.toggle('visible', !!q);
      const isNum = !!parseQuyenNumber(q);
      if (this.el.searchGoBtn) {
        this.el.searchGoBtn.classList.toggle('visible', isNum && (this.catalogMode === 'tap' || this.catalogMode === 'hoi'));
      }
      if (this.catalogMode === 'fullsearch') {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(() => {
          this.handleSearch(q);
        }, 180);
      } else {
        this.handleSearch(q);
      }
    });

    this.el.searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        if (this.catalogMode === 'tap' || this.catalogMode === 'hoi') {
          const qNum = parseQuyenNumber(this.el.searchInput.value);
          if (qNum) {
            handleSmartJump();
          } else if (this.filteredList.length > 0) {
            this.loadQuyen(this.filteredList[0].quyen);
            this.el.searchInput.blur();
            if (window.innerWidth <= 900) {
              this.el.sidebar.classList.add('closed');
              if (this.el.sidebarBackdrop) this.el.sidebarBackdrop.classList.remove('active');
            }
          }
        } else if (this.catalogMode === 'fullsearch') {
          clearTimeout(searchDebounceTimer);
          this.handleSearch(this.el.searchInput.value);
        }
      }
    });

    this.el.searchClearBtn.addEventListener('click', () => {
      this.el.searchInput.value = '';
      this.el.searchClearBtn.classList.remove('visible');
      if (this.el.searchGoBtn) this.el.searchGoBtn.classList.remove('visible');
      this.handleSearch('');
    });

    // Scroll progress tracker
    this.el.contentArea.addEventListener('scroll', () => {
      const pct = this.getScrollPercent();
      this.el.progressBar.style.width = `${pct}%`;

      // Debounce saving scroll position
      clearTimeout(this.scrollSaveTimer);
      this.scrollSaveTimer = setTimeout(() => {
        saveScrollPosition(this.currentQuyenNum, pct);
      }, 350);
    });

    // Hash change listener
    window.addEventListener('hashchange', () => {
      const match = window.location.hash.match(/#quyen-(\d+)/);
      if (match) {
        const qNum = parseInt(match[1], 10);
        if (qNum !== this.currentQuyenNum) {
          this.loadQuyen(qNum);
        }
      }
    });

    // Keyboard shortcuts
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT') return;
      if (e.key === 'ArrowRight' || e.key === 'j') {
        if (this.currentQuyenNum < 600) this.loadQuyen(this.currentQuyenNum + 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'k') {
        if (this.currentQuyenNum > 1) this.loadQuyen(this.currentQuyenNum - 1);
      } else if (e.key === 'b') {
        playBell();
      } else if (e.key === 'm') {
        playMokugyo();
      } else if (e.key === 'z') {
        this.toggleZenMode(!document.body.classList.contains('zen-mode'));
      } else if (e.key === 'Escape') {
        this.closeGlossaryModal();
        this.closeSettingsDrawer();
      } else if (e.key === ' ') {
        e.preventDefault();
        if (this.isAutoScrolling) {
          this.toggleAutoScrollPause();
        } else {
          this.toggleAutoScroll();
        }
      }
    });
  }

  // Auto-scroll engine
  toggleAutoScroll() {
    if (this.isAutoScrolling) {
      this.stopAutoScroll();
    } else {
      this.startAutoScroll();
    }
  }

  startAutoScroll() {
    this.isAutoScrolling = true;
    this.isAutoScrollPaused = false;
    
    // Use floating-point accumulator to prevent integer truncation on mobile WebKit
    this.autoScrollAccumulator = this.el.contentArea.scrollTop;

    // Temporarily bypass CSS smooth-scrolling so rAF doesn't fight smooth interpolation
    this.el.contentArea.style.scrollBehavior = 'auto';

    if (this.el.btnAutoscroll) {
      this.el.btnAutoscroll.classList.add('active');
      const pill = this.el.btnAutoscroll.querySelector('.pill-label');
      if (pill) pill.textContent = 'Đang cuộn';
    }

    if (this.el.mBtnAutoscroll) {
      this.el.mBtnAutoscroll.classList.add('active');
      const label = this.el.mBtnAutoscroll.querySelector('.m-autoscroll-label');
      if (label) label.textContent = 'Dừng';
    }

    this.el.autoScrollBar.classList.remove('hidden');
    this.el.btnAutoScrollPause.textContent = '⏸ Tạm dừng';
    this.el.autoScrollStatusText.textContent = 'Đang tự cuộn...';

    if (this.prefs.metronomeEnabled) {
      startMokugyoMetronome(this.prefs.metronomeBpm || 45);
    }

    const scrollStep = () => {
      if (!this.isAutoScrolling) return;

      if (!this.isAutoScrollPaused) {
        // Speed step in pixels per animation frame (60fps)
        const speedMap = { 1: 0.85, 2: 1.65, 3: 2.85 };
        const step = speedMap[this.autoScrollSpeed] || 0.85;

        this.autoScrollAccumulator += step;
        this.el.contentArea.scrollTop = Math.floor(this.autoScrollAccumulator);

        // If user manually touched & scrolled, re-sync accumulator smoothly
        if (Math.abs(this.el.contentArea.scrollTop - this.autoScrollAccumulator) > 40) {
          this.autoScrollAccumulator = this.el.contentArea.scrollTop;
        }

        // Check if reached bottom
        const maxScroll = this.el.contentArea.scrollHeight - this.el.contentArea.clientHeight;
        if (maxScroll > 10 && this.el.contentArea.scrollTop >= maxScroll - 4) {
          this.stopAutoScroll();
          this.showToast('Đã viên mãn thời kinh quyển này.');
          return;
        }
      }

      this.autoScrollRAF = requestAnimationFrame(scrollStep);
    };

    cancelAnimationFrame(this.autoScrollRAF);
    this.autoScrollRAF = requestAnimationFrame(scrollStep);
  }

  toggleAutoScrollPause() {
    this.isAutoScrollPaused = !this.isAutoScrollPaused;
    if (this.isAutoScrollPaused) {
      stopMokugyoMetronome();
      this.el.btnAutoScrollPause.textContent = '▶ Tiếp tục';
      this.el.autoScrollStatusText.textContent = 'Đã tạm dừng';
      if (this.el.mBtnAutoscroll) {
        const label = this.el.mBtnAutoscroll.querySelector('.m-autoscroll-label');
        if (label) label.textContent = 'Tiếp tục';
      }
    } else {
      this.autoScrollAccumulator = this.el.contentArea.scrollTop;
      this.el.btnAutoScrollPause.textContent = '⏸ Tạm dừng';
      this.el.autoScrollStatusText.textContent = 'Đang tự cuộn...';
      if (this.prefs.metronomeEnabled) {
        startMokugyoMetronome(this.prefs.metronomeBpm || 45);
      }
      if (this.el.mBtnAutoscroll) {
        const label = this.el.mBtnAutoscroll.querySelector('.m-autoscroll-label');
        if (label) label.textContent = 'Dừng';
      }
    }
  }

  stopAutoScroll() {
    this.isAutoScrolling = false;
    this.isAutoScrollPaused = false;
    cancelAnimationFrame(this.autoScrollRAF);
    stopMokugyoMetronome();

    // Restore CSS smooth-scrolling for normal jumps
    this.el.contentArea.style.scrollBehavior = '';

    if (this.el.btnAutoscroll) {
      this.el.btnAutoscroll.classList.remove('active');
      const pill = this.el.btnAutoscroll.querySelector('.pill-label');
      if (pill) pill.textContent = 'Tự cuộn';
    }

    if (this.el.mBtnAutoscroll) {
      this.el.mBtnAutoscroll.classList.remove('active');
      const label = this.el.mBtnAutoscroll.querySelector('.m-autoscroll-label');
      if (label) label.textContent = 'Tự cuộn';
    }

    this.el.autoScrollBar.classList.add('hidden');
  }

  getScrollPercent() {
    const el = this.el.contentArea;
    const maxScroll = el.scrollHeight - el.clientHeight;
    if (maxScroll <= 0) return 0;
    return Math.min(100, Math.max(0, (el.scrollTop / maxScroll) * 100));
  }

  toggleZenMode(enable) {
    document.body.classList.toggle('zen-mode', enable);
    updatePreference('zenMode', enable);
    if (enable) {
      this.showToast('Đã bật chế độ thiền định (Zen Mode). Nhấn phím Z để thoát.');
    }
  }

  openSettingsDrawer() {
    this.el.settingsDrawer.classList.add('open');
    this.el.drawerBackdrop.classList.add('active');
  }

  closeSettingsDrawer() {
    this.el.settingsDrawer.classList.remove('open');
    this.el.drawerBackdrop.classList.remove('active');
  }

  setCatalogMode(mode) {
    this.catalogMode = mode;

    // Update tab button active states
    const tabs = [this.el.tabTap, this.el.tabHoi, this.el.tabFullsearch, this.el.tabGlossary];
    tabs.forEach(tab => {
      if (tab) tab.classList.toggle('active', tab.dataset.mode === mode);
    });

    if (mode === 'tap' || mode === 'hoi') {
      if (this.el.filterChipsBar) this.el.filterChipsBar.classList.remove('hidden');
      if (this.el.quyenListContainer) this.el.quyenListContainer.classList.remove('hidden');
      if (this.el.fullsearchContainer) this.el.fullsearchContainer.classList.add('hidden');
      if (this.el.glossaryContainer) this.el.glossaryContainer.classList.add('hidden');
      if (this.el.searchInput) {
        this.el.searchInput.placeholder = 'Gõ số Quyển (1–600) hoặc tên Phẩm...';
      }
      if (mode === 'tap') this.activeTapId = 0;
      if (mode === 'hoi') this.activeHoiId = 0;
      this.renderFilterChips();
      this.handleSearch(this.el.searchInput.value);
    } else if (mode === 'fullsearch') {
      if (this.el.filterChipsBar) this.el.filterChipsBar.classList.add('hidden');
      if (this.el.quyenListContainer) this.el.quyenListContainer.classList.add('hidden');
      if (this.el.fullsearchContainer) this.el.fullsearchContainer.classList.remove('hidden');
      if (this.el.glossaryContainer) this.el.glossaryContainer.classList.add('hidden');
      if (this.el.searchInput) {
        this.el.searchInput.placeholder = 'Tìm câu kinh trong 600 Quyển (vd: tánh không, vô sở đắc)...';
        this.el.searchInput.focus();
      }
      if (this.el.searchGoBtn) this.el.searchGoBtn.classList.remove('visible');
      this.handleSearch(this.el.searchInput.value);
    } else if (mode === 'glossary') {
      if (this.el.filterChipsBar) this.el.filterChipsBar.classList.add('hidden');
      if (this.el.quyenListContainer) this.el.quyenListContainer.classList.add('hidden');
      if (this.el.fullsearchContainer) this.el.fullsearchContainer.classList.add('hidden');
      if (this.el.glossaryContainer) this.el.glossaryContainer.classList.remove('hidden');
      if (this.el.searchInput) {
        this.el.searchInput.placeholder = 'Tìm thuật ngữ Bát Nhã (Việt, Phạn, Hán)...';
        this.el.searchInput.focus();
      }
      if (this.el.searchGoBtn) this.el.searchGoBtn.classList.remove('visible');
      this.renderGlossaryCategories();
      this.handleSearch(this.el.searchInput.value);
    }
  }

  renderFilterChips() {
    if (this.catalogMode === 'tap') {
      let html = `<button class="filter-chip ${this.activeTapId === 0 ? 'active' : ''}" data-tap-id="0">Tất cả (600)</button>`;
      this.tapMeta.forEach(t => {
        html += `<button class="filter-chip ${this.activeTapId === t.id ? 'active' : ''}" data-tap-id="${t.id}">${t.name} (${t.range})</button>`;
      });
      this.el.filterChipsBar.innerHTML = html;

      this.el.filterChipsBar.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', () => {
          const tId = parseInt(chip.dataset.tapId, 10);
          this.activeTapId = tId;
          this.el.filterChipsBar.querySelectorAll('.filter-chip').forEach(c => c.classList.toggle('active', c === chip));
          this.handleSearch(this.el.searchInput.value);
        });
      });
    } else {
      let html = `<button class="filter-chip ${this.activeHoiId === 0 ? 'active' : ''}" data-hoi-id="0">Tất cả (600)</button>`;
      (this.tocData.hoi_list || []).forEach(h => {
        html += `<button class="filter-chip ${this.activeHoiId === h.id ? 'active' : ''}" data-hoi-id="${h.id}">Hội ${h.id} (${h.count})</button>`;
      });
      this.el.filterChipsBar.innerHTML = html;

      this.el.filterChipsBar.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', () => {
          const hId = parseInt(chip.dataset.hoiId, 10);
          this.activeHoiId = hId;
          this.el.filterChipsBar.querySelectorAll('.filter-chip').forEach(c => c.classList.toggle('active', c === chip));
          this.handleSearch(this.el.searchInput.value);
        });
      });
    }
  }

  async handleSearch(query) {
    if (this.catalogMode === 'tap' || this.catalogMode === 'hoi') {
      let list = this.quyenList;

      if (this.catalogMode === 'tap' && this.activeTapId > 0) {
        list = list.filter(q => q.tap === this.activeTapId);
      } else if (this.catalogMode === 'hoi' && this.activeHoiId > 0) {
        list = list.filter(q => q.hoi_id === this.activeHoiId);
      }

      this.filteredList = filterQuyenList(list, query);
      this.renderSidebarList();
    } else if (this.catalogMode === 'fullsearch') {
      await this.handleFullTextSearch(query);
    } else if (this.catalogMode === 'glossary') {
      await this.handleGlossarySearch(query);
    }
  }

  async handleFullTextSearch(query) {
    if (!this.el.fullsearchResults || !this.el.fullsearchStatus) return;

    const trimmed = (query || '').trim();
    if (trimmed.length < 2) {
      this.el.fullsearchStatus.innerHTML = `
        <span class="fullsearch-hint">💡 Nhập từ khóa (tối thiểu 2 ký tự, vd: <em>vô sở đắc, tánh không, bát nhã, chân như</em>) để tìm câu kinh trong 600 Quyển.</span>
      `;
      this.el.fullsearchResults.innerHTML = '';
      return;
    }

    this.el.fullsearchStatus.innerHTML = `
      <div style="display: flex; align-items: center; gap: 8px;">
        <span class="modal-lotus-icon" style="display: inline-block; animation: spin 2s linear infinite;">☸</span>
        <span>Đang tra cứu 600 Quyển cho từ khóa "<strong>${escapeHtml(trimmed)}</strong>"...</span>
      </div>
    `;

    try {
      const results = await searchFullText(trimmed, this.quyenList);

      if (results.length === 0) {
        this.el.fullsearchStatus.innerHTML = `
          <span style="color: var(--text-muted);">Không tìm thấy đoạn kinh nào chứa từ khóa "<strong>${escapeHtml(trimmed)}</strong>".</span>
        `;
        this.el.fullsearchResults.innerHTML = '';
        return;
      }

      const totalHits = results.reduce((acc, r) => acc + r.count, 0);
      this.el.fullsearchStatus.innerHTML = `
        <div style="font-weight: 600; color: var(--text-primary);">
          Tìm thấy <strong>${results.length}</strong> Quyển (${totalHits} lần xuất hiện) chứa "<strong>${escapeHtml(trimmed)}</strong>"
        </div>
      `;

      // Render top results (up to 80 to keep smooth rendering)
      const renderCount = Math.min(results.length, 80);
      const itemsHtml = results.slice(0, renderCount).map(r => `
        <li class="fullsearch-item-card" data-quyen="${r.quyen}">
          <div class="fullsearch-card-header">
            <div class="fullsearch-q-title">Quyển ${String(r.quyen).padStart(2, '0')}</div>
            <span class="fullsearch-hit-badge">${r.count} lần</span>
          </div>
          <div class="fullsearch-q-sub">
            Tập ${r.meta.tap} · Hội ${r.meta.hoi_id} · ${escapeHtml(r.meta.pham || r.meta.hoi)}
          </div>
          <div class="fullsearch-card-actions">
            <button class="btn-read-quyen-direct" data-quyen="${r.quyen}">Đọc Quyển này ➔</button>
            <button class="btn-view-excerpt-toggle" data-quyen="${r.quyen}">Xem trích đoạn ▾</button>
          </div>
          <div class="fullsearch-excerpts-box hidden" id="excerpts-box-${r.quyen}"></div>
        </li>
      `).join('');

      this.el.fullsearchResults.innerHTML = itemsHtml;

      // Bind events for fullsearch items
      this.el.fullsearchResults.querySelectorAll('.btn-read-quyen-direct').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const qNum = parseInt(btn.dataset.quyen, 10);
          this.loadQuyen(qNum);
          if (window.innerWidth <= 900) {
            this.el.sidebar.classList.add('closed');
            if (this.el.sidebarBackdrop) this.el.sidebarBackdrop.classList.remove('active');
          }
        });
      });

      this.el.fullsearchResults.querySelectorAll('.btn-view-excerpt-toggle').forEach(btn => {
        btn.addEventListener('click', async (e) => {
          e.stopPropagation();
          const qNum = parseInt(btn.dataset.quyen, 10);
          const box = document.getElementById(`excerpts-box-${qNum}`);
          if (!box) return;

          const isHidden = box.classList.toggle('hidden');
          btn.textContent = isHidden ? 'Xem trích đoạn ▾' : 'Ẩn trích đoạn ▴';

          if (!isHidden && !box.dataset.loaded) {
            box.innerHTML = '<p class="fullsearch-excerpt-p" style="font-style: italic; color: var(--text-muted);">Đang nạp trích đoạn...</p>';
            const excerpts = await fetchQuyenExcerpts(qNum, trimmed, this.quyenList, 3);
            if (excerpts.length === 0) {
              box.innerHTML = '<p class="fullsearch-excerpt-p" style="color: var(--text-muted);">Từ khóa xuất hiện trong các đoạn trùng tụng của phẩm này.</p>';
            } else {
              box.innerHTML = excerpts.map(ex => `<p class="fullsearch-excerpt-p">...${ex}...</p>`).join('');
            }
            box.dataset.loaded = 'true';
          }
        });
      });

      this.el.fullsearchResults.querySelectorAll('.fullsearch-item-card').forEach(card => {
        card.addEventListener('click', (e) => {
          if (e.target.closest('.fullsearch-card-actions') || e.target.closest('.fullsearch-excerpts-box')) return;
          const qNum = parseInt(card.dataset.quyen, 10);
          this.loadQuyen(qNum);
          if (window.innerWidth <= 900) {
            this.el.sidebar.classList.add('closed');
            if (this.el.sidebarBackdrop) this.el.sidebarBackdrop.classList.remove('active');
          }
        });
      });

    } catch (err) {
      console.error('Lỗi tìm kiếm toàn văn:', err);
      this.el.fullsearchStatus.innerHTML = `<span style="color: var(--accent);">Có lỗi xảy ra khi tra cứu: ${escapeHtml(err.message)}</span>`;
    }
  }

  renderGlossaryCategories() {
    if (!this.el.glossaryCategoryFilter) return;
    const html = this.glossaryCategories.map(cat => `
      <button class="filter-chip ${this.activeGlossaryCategory === cat ? 'active' : ''}" data-category="${cat}">
        ${cat}
      </button>
    `).join('');
    this.el.glossaryCategoryFilter.innerHTML = html;

    this.el.glossaryCategoryFilter.querySelectorAll('.filter-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        this.activeGlossaryCategory = chip.dataset.category;
        this.el.glossaryCategoryFilter.querySelectorAll('.filter-chip').forEach(c => c.classList.toggle('active', c === chip));
        this.handleGlossarySearch(this.el.searchInput.value);
      });
    });
  }

  async handleGlossarySearch(query) {
    if (!this.el.glossaryList) return;

    try {
      const list = await searchGlossary(query);
      const filtered = (this.activeGlossaryCategory && this.activeGlossaryCategory !== 'Tất cả')
        ? list.filter(item => item.category === this.activeGlossaryCategory)
        : list;

      if (filtered.length === 0) {
        this.el.glossaryList.innerHTML = `
          <li style="padding: 24px; text-align: center; color: var(--text-muted); font-size: 0.9rem;">
            Không tìm thấy thuật ngữ nào phù hợp với "${escapeHtml(query)}".
          </li>
        `;
        return;
      }

      this.el.glossaryList.innerHTML = filtered.map(renderGlossaryCard).join('');

      // Bind click to open detail modal
      this.el.glossaryList.querySelectorAll('.glossary-item-card').forEach(card => {
        card.addEventListener('click', async () => {
          const termId = card.dataset.termId;
          const allTerms = await loadGlossary();
          const found = allTerms.find(t => t.id === termId);
          if (found) {
            this.openGlossaryModal(found);
          }
        });
      });
    } catch (err) {
      console.error('Lỗi tra cứu từ điển:', err);
      this.el.glossaryList.innerHTML = `<li style="padding: 16px; color: var(--accent);">Lỗi tải từ điển: ${escapeHtml(err.message)}</li>`;
    }
  }

  openGlossaryModal(item) {
    if (!this.el.glossaryModal || !this.el.glossaryModalInner) return;
    this.el.glossaryModalInner.innerHTML = renderGlossaryModalContent(item);
    this.el.glossaryModal.classList.add('open');
    if (this.el.glossaryBackdrop) this.el.glossaryBackdrop.classList.add('active');

    // Bind deep search trigger button inside modal
    const btnSearchTerm = document.getElementById('btn-search-term-in-sutra');
    if (btnSearchTerm) {
      btnSearchTerm.addEventListener('click', () => {
        const term = btnSearchTerm.dataset.term;
        this.closeGlossaryModal();
        this.setCatalogMode('fullsearch');
        if (this.el.searchInput) {
          this.el.searchInput.value = term;
          if (this.el.searchClearBtn) this.el.searchClearBtn.classList.add('visible');
        }
        this.handleSearch(term);
      });
    }
  }

  closeGlossaryModal() {
    if (this.el.glossaryModal) this.el.glossaryModal.classList.remove('open');
    if (this.el.glossaryBackdrop) this.el.glossaryBackdrop.classList.remove('active');
  }

  updateTrackerUI() {
    const completed = getCompletedQuyens();
    const count = completed.length;
    const pct = Math.round((count / 600) * 100);
    if (this.el.trackerCount) this.el.trackerCount.textContent = `${count} / 600 Quyển`;
    if (this.el.trackerPct) this.el.trackerPct.textContent = `${pct}%`;
    if (this.el.trackerProgressFill) this.el.trackerProgressFill.style.width = `${pct}%`;
    if (this.el.trackerSummaryPill) this.el.trackerSummaryPill.textContent = `✓ ${count}/600`;
  }

  renderSidebarList() {
    if (this.filteredList.length === 0) {
      this.el.quyenListContainer.innerHTML = `
        <li style="padding: 24px; text-align: center; color: var(--text-muted); font-size: 0.9rem;">
          Không tìm thấy quyển nào phù hợp.
        </li>
      `;
      return;
    }

    const itemsHtml = this.filteredList.map(q => {
      const isActive = q.quyen === this.currentQuyenNum;
      const isCompleted = isQuyenCompleted(q.quyen);
      return `
        <li class="quyen-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}" data-quyen="${q.quyen}">
          <div class="quyen-item-header">
            <span class="quyen-number">Quyển ${String(q.quyen).padStart(2, '0')}${isCompleted ? '<span class="quyen-check-badge" title="Đã hoàn thành quyển này">✓</span>' : ''}</span>
            <span class="quyen-pages">tr. ${q.p_in}</span>
          </div>
          <div class="quyen-title" title="${q.pham || q.hoi}">
            ${q.pham || q.hoi}
          </div>
        </li>
      `;
    }).join('');

    this.el.quyenListContainer.innerHTML = itemsHtml;

    // Attach click events
    this.el.quyenListContainer.querySelectorAll('.quyen-item').forEach(item => {
      item.addEventListener('click', () => {
        const qNum = parseInt(item.dataset.quyen, 10);
        this.loadQuyen(qNum);
        if (window.innerWidth <= 900) {
          this.el.sidebar.classList.add('closed');
          if (this.el.sidebarBackdrop) this.el.sidebarBackdrop.classList.remove('active');
        }
      });
    });

    // Auto-scroll active item into view
    const activeEl = this.el.quyenListContainer.querySelector('.quyen-item.active');
    if (activeEl) {
      activeEl.scrollIntoView({ block: 'nearest' });
    }
  }

  async loadQuyen(quyenNum) {
    this.stopAutoScroll();
    this.currentQuyenNum = quyenNum;
    window.location.hash = `quyen-${quyenNum}`;
    updatePreference('currentQuyen', quyenNum);

    const meta = this.quyenList.find(q => q.quyen === quyenNum);
    if (!meta) return;

    // Update Header Badges & Buttons
    const pad = (n) => String(n).padStart(2, '0');
    this.el.headerTitleBadge.innerHTML = `
      <span class="hoi-pill">TẬP ${pad(meta.tap)} · HỘI ${pad(meta.hoi_id)}</span>
      <span class="quyen-pill-text">Quyển ${quyenNum}</span>
      <span class="page-pill-text">(Trang ${meta.p_in})</span>
    `;

    if (this.el.btnPrevQuyenTop) this.el.btnPrevQuyenTop.disabled = quyenNum <= 1;
    if (this.el.btnNextQuyenTop) this.el.btnNextQuyenTop.disabled = quyenNum >= 600;

    // Highlight active item in sidebar
    this.el.quyenListContainer.querySelectorAll('.quyen-item').forEach(el => {
      el.classList.toggle('active', parseInt(el.dataset.quyen, 10) === quyenNum);
    });

    // Show loading
    this.el.contentInner.innerHTML = `
      <div class="loading-indicator">
        <div class="spinner-lotus-wrap">
          <svg class="lotus-spinner-svg" width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"></circle>
            <circle cx="12" cy="12" r="3"></circle>
            <line x1="12" y1="2" x2="12" y2="9"></line>
            <line x1="12" y1="15" x2="12" y2="22"></line>
            <line x1="2" y1="12" x2="9" y2="12"></line>
            <line x1="15" y1="12" x2="22" y2="12"></line>
          </svg>
        </div>
        <p class="loading-text">Đang cung thỉnh Quyển ${quyenNum}...</p>
      </div>
    `;

    try {
      const resp = await fetch(meta.file);
      if (!resp.ok) throw new Error(`Không thể nạp file ${meta.file}`);
      const mdText = await resp.text();
      const parsedHtml = parseMarkdown(mdText);

      // Prepend Opening Ritual if enabled
      const openingHtml = (this.prefs.showRitual !== false) ? renderOpeningRitual() : '';
      
      // Append Closing Ritual if enabled
      const closingHtml = (this.prefs.showRitual !== false) ? renderClosingRitual() : '';

      // Completion tracker action bar
      const isCompleted = isQuyenCompleted(quyenNum);
      const completionHtml = `
        <div class="completion-action-bar">
          <div class="completion-info">
            <span class="completion-icon">☸</span>
            <span class="completion-label">Công đức tu tập Quyển ${quyenNum}:</span>
          </div>
          <button id="btn-toggle-completion" class="btn-mark-completed ${isCompleted ? 'completed' : ''}">
            <span class="check-icon">${isCompleted ? '✓' : '○'}</span>
            <span class="btn-text">${isCompleted ? 'Đã hoàn thành quyển này' : 'Đánh dấu ĐÃ TỤNG XONG'}</span>
          </button>
        </div>
      `;

      // Bottom chapter navigation with large friendly buttons
      const prevDisabled = quyenNum <= 1 ? 'disabled' : '';
      const nextDisabled = quyenNum >= 600 ? 'disabled' : '';

      const navBottomHtml = `
        <div class="chapter-nav-bottom">
          <button class="btn-nav-page" id="btn-prev-quyen" ${prevDisabled}>
            ← Quyển ${quyenNum - 1}
          </button>
          <div class="nav-center-status">
            <span class="nav-quyen-count">Quyển ${quyenNum} / 600</span>
            <span class="nav-quyen-sub">Tập ${meta.tap} · Trang ${meta.p_in}</span>
          </div>
          <button class="btn-nav-page" id="btn-next-quyen" ${nextDisabled}>
            Quyển ${quyenNum + 1} →
          </button>
        </div>
      `;

      this.el.contentInner.innerHTML = openingHtml + parsedHtml + closingHtml + completionHtml + navBottomHtml;

      // Update dynamic document title for browser tabs & history
      const shortPham = (meta.pham || '').split('&')[0].replace(/^[IVXLCDM]+\.\s*/, '').trim();
      document.title = shortPham 
        ? `Quyển ${quyenNum}: ${shortPham} — Kinh Đại Bát Nhã`
        : `Quyển ${quyenNum} — Kinh Đại Bát Nhã`;

      // Scroll to top
      this.el.contentArea.scrollTop = 0;

      // Bind completion toggle
      const btnComp = document.getElementById('btn-toggle-completion');
      if (btnComp) {
        btnComp.addEventListener('click', () => {
          const nowCompleted = toggleQuyenCompleted(quyenNum);
          btnComp.classList.toggle('completed', nowCompleted);
          const icon = btnComp.querySelector('.check-icon');
          if (icon) icon.textContent = nowCompleted ? '✓' : '○';
          const txt = btnComp.querySelector('.btn-text');
          if (txt) txt.textContent = nowCompleted ? 'Đã hoàn thành quyển này' : 'Đánh dấu ĐÃ TỤNG XONG';
          this.updateTrackerUI();
          this.renderSidebarList();
          this.showToast(nowCompleted ? `Đã lưu: Viên mãn Quyển ${quyenNum} vào Sổ Tinh Tấn!` : `Đã bỏ đánh dấu Quyển ${quyenNum}`);
        });
      }

      // Bind ritual collapse buttons
      this.el.contentInner.querySelectorAll('.ritual-collapse-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const targetId = btn.dataset.target;
          const body = document.getElementById(targetId);
          if (body) {
            const isCollapsed = body.classList.toggle('collapsed');
            const icon = btn.querySelector('.collapse-icon');
            if (icon) icon.textContent = isCollapsed ? '▼' : '▲';
            const txt = btn.querySelector('.collapse-text');
            if (txt) txt.textContent = isCollapsed ? 'Mở rộng' : 'Thu gọn';
          }
        });
      });

      // Bind bottom nav buttons
      const btnPrev = document.getElementById('btn-prev-quyen');
      const btnNext = document.getElementById('btn-next-quyen');
      if (btnPrev && quyenNum > 1) {
        btnPrev.addEventListener('click', () => this.loadQuyen(quyenNum - 1));
      }
      if (btnNext && quyenNum < 600) {
        btnNext.addEventListener('click', () => this.loadQuyen(quyenNum + 1));
      }

    } catch (err) {
      console.error('Lỗi nạp file kinh:', err);
      this.el.contentInner.innerHTML = `
        <div class="loading-indicator">
          <p style="color: var(--accent); font-weight: bold;">Không thể tải kinh văn Quyển ${quyenNum}.</p>
          <p style="font-size: 0.9rem;">${err.message}</p>
        </div>
      `;
    }
  }

  renderBookmarksList() {
    if (!this.el.bookmarksList) return;
    const bookmarks = this.prefs.bookmarks || [];
    if (bookmarks.length === 0) {
      this.el.bookmarksList.innerHTML = '<p style="font-size: 0.85rem; color: var(--text-muted); font-style: italic;">Chưa có trang nào được đánh dấu.</p>';
      return;
    }

    const html = bookmarks.map(b => `
      <div class="bookmark-item">
        <span class="bookmark-link" data-quyen="${b.quyen}" data-scroll="${b.scrollPercent}">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>
          ${b.title} (${Math.round(b.scrollPercent)}%)
        </span>
        <button class="btn-del-bookmark" data-quyen="${b.quyen}" title="Xóa dấu trang">✕</button>
      </div>
    `).join('');

    this.el.bookmarksList.innerHTML = html;

    this.el.bookmarksList.querySelectorAll('.bookmark-link').forEach(el => {
      el.addEventListener('click', () => {
        const qNum = parseInt(el.dataset.quyen, 10);
        this.loadQuyen(qNum);
        this.closeSettingsDrawer();
      });
    });

    this.el.bookmarksList.querySelectorAll('.btn-del-bookmark').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const qNum = parseInt(btn.dataset.quyen, 10);
        removeBookmark(qNum);
        this.prefs = loadPreferences();
        this.renderBookmarksList();
      });
    });
  }

  showToast(msg) {
    let toast = document.getElementById('prajna-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'prajna-toast';
      toast.className = 'prajna-toast';
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(this.toastTimer);
    this.toastTimer = setTimeout(() => {
      toast.classList.remove('show');
    }, 2800);
  }

  registerServiceWorker() {
    if ('serviceWorker' in navigator && window.location.protocol.startsWith('http')) {
      navigator.serviceWorker.register('sw.js').catch(err => {
        console.log('SW registration note:', err);
      });
    }
  }
}

// Boot application
window.addEventListener('DOMContentLoaded', () => {
  const app = new PrajnaApp();
  app.init();
});

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[m]);
}
