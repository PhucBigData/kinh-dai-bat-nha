/**
 * Prajñā Search Engine
 * Instant, zero-latency in-memory search across all 600 Quyển
 */

// Helper to remove Vietnamese diacritics for flexible fuzzy searching
export function removeDiacritics(str) {
  if (!str) return '';
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd')
    .replace(/Đ/g, 'D');
}

export function filterQuyenList(quyenList, query) {
  if (!query || !query.trim()) {
    return quyenList;
  }

  const qRaw = query.trim().toLowerCase();
  const qNorm = removeDiacritics(qRaw);

  // Exact number search (e.g. "45", "045", "quyen 45", "q45")
  const numMatch = qRaw.match(/^(?:quyen|q|quyển)?\s*(\d+)$/);
  if (numMatch) {
    const targetQ = parseInt(numMatch[1], 10);
    return quyenList.filter(item => item.quyen === targetQ);
  }

  return quyenList.filter(item => {
    // 1. Match Quyển number
    if (String(item.quyen) === qRaw) return true;

    // 2. Match Phẩm
    const phamNorm = removeDiacritics((item.pham || '').toLowerCase());
    if (phamNorm.includes(qNorm)) return true;

    // 3. Match Hội
    const hoiNorm = removeDiacritics((item.hoi || '').toLowerCase());
    if (hoiNorm.includes(qNorm)) return true;

    // 4. Match Phần
    const phanNorm = removeDiacritics((item.phan || '').toLowerCase());
    if (phanNorm.includes(qNorm)) return true;

    // 5. Match Tập
    if (`tap ${item.tap}`.includes(qNorm) || `tập ${item.tap}`.includes(qRaw)) return true;

    // 6. Match page
    if (item.p_in && item.p_in.includes(qRaw)) return true;

    return false;
  });
}
