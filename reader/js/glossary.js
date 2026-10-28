/**
 * Prajñā Buddhist Glossary Engine (Từ Điển Thuật Ngữ Bát Nhã)
 * Authoritative Buddhist philosophy dictionary with instant offline search
 */

let glossaryData = null;
let isGlossaryLoading = false;

/**
 * Lazy load glossary data
 */
export async function loadGlossary() {
  if (glossaryData) return glossaryData;
  if (isGlossaryLoading) {
    while (isGlossaryLoading) {
      await new Promise(r => setTimeout(r, 50));
    }
    return glossaryData;
  }

  isGlossaryLoading = true;
  try {
    const resp = await fetch('data/glossary.json');
    if (!resp.ok) throw new Error('Không thể tải glossary.json');
    glossaryData = await resp.json();
    console.log(`[Prajñā Glossary] Loaded ${glossaryData.length} authoritative terms.`);
  } catch (err) {
    console.error('[Prajñā Glossary] Error loading glossary:', err);
    glossaryData = [];
  } finally {
    isGlossaryLoading = false;
  }
  return glossaryData;
}

function stripDiacritics(str) {
  if (!str) return '';
  return str.normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[đĐ]/g, 'd')
    .replace(/[śŚṣṢ]/g, 's')
    .replace(/[ūŪ]/g, 'u')
    .replace(/[īĪ]/g, 'i')
    .replace(/[āĀ]/g, 'a')
    .replace(/[ṛṚ]/g, 'r')
    .replace(/[ñÑ]/g, 'n')
    .replace(/[ṭṬ]/g, 't')
    .toLowerCase();
}

/**
 * Search glossary terms (with diacritic-insensitive matching for Sanskrit & Vietnamese)
 */
export async function searchGlossary(query = '') {
  const list = await loadGlossary();
  if (!query || !query.trim()) return list;

  const q = query.trim().toLowerCase();
  const qNorm = stripDiacritics(q);

  return list.filter(item => {
    const rawMatch = 
      item.term.toLowerCase().includes(q) ||
      (item.sanskrit && item.sanskrit.toLowerCase().includes(q)) ||
      (item.chinese && item.chinese.includes(q)) ||
      (item.category && item.category.toLowerCase().includes(q)) ||
      (item.brief && item.brief.toLowerCase().includes(q));

    if (rawMatch) return true;

    // Diacritic-free check
    const termNorm = stripDiacritics(item.term);
    const sktNorm = stripDiacritics(item.sanskrit);
    const briefNorm = stripDiacritics(item.brief);

    return termNorm.includes(qNorm) || sktNorm.includes(qNorm) || briefNorm.includes(qNorm);
  });
}

/**
 * Render HTML for a Glossary Term Card in the sidebar or list
 */
export function renderGlossaryCard(item) {
  return `
    <li class="glossary-item-card" data-term-id="${item.id}">
      <div class="glossary-item-header">
        <h4 class="glossary-term-name">${item.term}</h4>
        <span class="glossary-category-pill">${item.category}</span>
      </div>
      <div class="glossary-meta-row">
        ${item.sanskrit ? `<span class="glossary-sanskrit">IAST: <em>${item.sanskrit}</em></span>` : ''}
        ${item.chinese ? `<span class="glossary-chinese">Hán: <strong>${item.chinese}</strong></span>` : ''}
      </div>
      <p class="glossary-brief">${item.brief}</p>
      <div class="glossary-actions">
        <button class="btn-glossary-view" data-term-id="${item.id}">Chi tiết & Tra cứu ➔</button>
      </div>
    </li>
  `;
}

/**
 * Render the full detail Modal dialog for a Glossary Term
 */
export function renderGlossaryModalContent(item) {
  return `
    <div class="glossary-modal-header">
      <div class="modal-badge-group">
        <span class="modal-lotus-icon">☸</span>
        <span class="modal-category-badge">${item.category}</span>
      </div>
      <h3 class="glossary-modal-title">${item.term}</h3>
      <div class="glossary-modal-langs">
        ${item.sanskrit ? `<div class="lang-row"><span class="lang-label">Phạn ngữ (Sanskrit):</span> <em>${item.sanskrit}</em></div>` : ''}
        ${item.chinese ? `<div class="lang-row"><span class="lang-label">Hán tự:</span> <strong>${item.chinese}</strong></div>` : ''}
      </div>
    </div>
    
    <div class="glossary-modal-body">
      <div class="definition-box">
        <h5 class="def-heading">Định nghĩa căn bản:</h5>
        <p class="def-brief">${item.brief}</p>
      </div>
      
      <div class="explanation-box">
        <h5 class="def-heading">Giáo nghĩa Phật học Bát Nhã:</h5>
        <p class="def-detail">${item.detail}</p>
      </div>
    </div>

    <div class="glossary-modal-footer">
      <button id="btn-search-term-in-sutra" class="btn-search-term" data-term="${item.term}">
        🔍 Tra cứu từ khóa "${item.term}" trong 600 Quyển
      </button>
    </div>
  `;
}
