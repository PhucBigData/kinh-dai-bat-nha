/**
 * Prajñā Storage Manager
 * Handles local state persistence via localStorage
 */

const STORAGE_KEY = 'prajna_reader_prefs_v1';

const defaultPrefs = {
  currentQuyen: 1,
  theme: 'sepia', // 'light' | 'sepia' | 'dark'
  fontSize: 20,   // in px
  lineHeight: 1.85,
  fontFamily: 'serif', // 'serif' | 'sans'
  zenMode: false,
  showRitual: true, // Khung nghi thức khai kinh & hồi hướng
  completedQuyens: [], // Danh sách các quyển đã hoàn thành [1, 2, ...]
  metronomeEnabled: false, // Gõ mõ tự động theo nhịp
  metronomeBpm: 45, // Nhịp tụng kinh bình hòa (45 nhịp/phút)
  bookmarks: [],
  scrollPositions: {} // { [quyen]: scrollPercent }
};

export function loadPreferences() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...defaultPrefs };
    const parsed = JSON.parse(raw);
    return { ...defaultPrefs, ...parsed };
  } catch (e) {
    console.warn('Could not load preferences from localStorage', e);
    return { ...defaultPrefs };
  }
}

export function savePreferences(prefs) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
  } catch (e) {
    console.warn('Could not save preferences to localStorage', e);
  }
}

export function updatePreference(key, value) {
  const prefs = loadPreferences();
  prefs[key] = value;
  savePreferences(prefs);
  return prefs;
}

export function saveBookmark(quyen, scrollPercent, title) {
  const prefs = loadPreferences();
  // Filter out any existing bookmark for the same quyen
  prefs.bookmarks = prefs.bookmarks.filter(b => b.quyen !== quyen);
  prefs.bookmarks.unshift({
    quyen,
    scrollPercent,
    title: title || `Quyển ${quyen}`,
    timestamp: Date.now()
  });
  // Keep maximum 20 bookmarks
  if (prefs.bookmarks.length > 20) {
    prefs.bookmarks = prefs.bookmarks.slice(0, 20);
  }
  savePreferences(prefs);
  return prefs.bookmarks;
}

export function removeBookmark(quyen) {
  const prefs = loadPreferences();
  prefs.bookmarks = prefs.bookmarks.filter(b => b.quyen !== quyen);
  savePreferences(prefs);
  return prefs.bookmarks;
}

export function saveScrollPosition(quyen, scrollPercent) {
  const prefs = loadPreferences();
  if (!prefs.scrollPositions) prefs.scrollPositions = {};
  prefs.scrollPositions[quyen] = scrollPercent;
  savePreferences(prefs);
}

export function getScrollPosition(quyen) {
  const prefs = loadPreferences();
  return (prefs.scrollPositions && prefs.scrollPositions[quyen]) || 0;
}

export function toggleQuyenCompleted(quyen) {
  const prefs = loadPreferences();
  if (!Array.isArray(prefs.completedQuyens)) {
    prefs.completedQuyens = [];
  }
  const qNum = parseInt(quyen, 10);
  const idx = prefs.completedQuyens.indexOf(qNum);
  let isCompleted = false;
  if (idx >= 0) {
    prefs.completedQuyens.splice(idx, 1);
    isCompleted = false;
  } else {
    prefs.completedQuyens.push(qNum);
    isCompleted = true;
  }
  savePreferences(prefs);
  return isCompleted;
}

export function isQuyenCompleted(quyen) {
  const prefs = loadPreferences();
  const qNum = parseInt(quyen, 10);
  return Array.isArray(prefs.completedQuyens) && prefs.completedQuyens.includes(qNum);
}

export function getCompletedQuyens() {
  const prefs = loadPreferences();
  return Array.isArray(prefs.completedQuyens) ? prefs.completedQuyens : [];
}
