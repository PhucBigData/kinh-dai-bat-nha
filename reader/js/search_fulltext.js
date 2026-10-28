/**
 * Prajñā Full-Text Search Engine (Offline Client-Side)
 * Blazing fast inverted index search across all 600 Quyển of Kinh Đại Bát Nhã
 */

let searchIndex = null;
let isIndexLoading = false;

/**
 * Lazy load search index only when the user switches to full-text search
 */
export async function loadSearchIndex() {
  if (searchIndex) return searchIndex;
  if (isIndexLoading) {
    while (isIndexLoading) {
      await new Promise(r => setTimeout(r, 50));
    }
    return searchIndex;
  }

  isIndexLoading = true;
  try {
    const resp = await fetch('data/search_index.json');
    if (!resp.ok) throw new Error('Không thể tải search_index.json');
    searchIndex = await resp.json();
    console.log(`[Prajñā Search] Loaded inverted index with ${Object.keys(searchIndex).length} terms.`);
  } catch (err) {
    console.error('[Prajñā Search] Error loading search index:', err);
    searchIndex = {};
  } finally {
    isIndexLoading = false;
  }
  return searchIndex;
}

/**
 * Search full text across all 600 Quyển
 * @param {string} rawQuery - The search query
 * @param {Array} quyenList - The full list of quyen metadata from toc.json
 * @returns {Array} List of matching results sorted by score/frequency
 */
export async function searchFullText(rawQuery, quyenList = []) {
  if (!rawQuery || !rawQuery.trim()) return [];

  const index = await loadSearchIndex();
  const query = rawQuery.trim().toLowerCase();

  // Normalize query terms
  const terms = query.split(/\s+/).filter(w => w.length >= 2);
  if (terms.length === 0) return [];

  // Check if exact phrase exists in index
  let candidateQuyens = new Map(); // quyen -> total occurrences

  if (index[query]) {
    // Exact compound term match!
    for (const [qNum, cnt] of index[query]) {
      candidateQuyens.set(qNum, (candidateQuyens.get(qNum) || 0) + cnt * 3);
    }
  } else {
    // Intersect all individual words
    let termQuyenSets = [];
    for (const t of terms) {
      if (index[t]) {
        const qMap = new Map(index[t]); // quyen -> count
        termQuyenSets.push(qMap);
      } else {
        // One word not found anywhere in 600 Quyển -> no results
        return [];
      }
    }

    if (termQuyenSets.length === 0) return [];

    // Find intersection of all words
    const firstSet = termQuyenSets[0];
    for (const [qNum, cnt] of firstSet.entries()) {
      let inAll = true;
      let totalCount = cnt;
      for (let i = 1; i < termQuyenSets.length; i++) {
        const otherMap = termQuyenSets[i];
        if (!otherMap.has(qNum)) {
          inAll = false;
          break;
        }
        totalCount += otherMap.get(qNum);
      }

      if (inAll) {
        candidateQuyens.set(qNum, totalCount);
      }
    }
  }

  // Convert to formatted result objects
  const results = [];
  const quyenMap = new Map(quyenList.map(q => [q.quyen, q]));

  for (const [qNum, totalCount] of candidateQuyens.entries()) {
    const meta = quyenMap.get(qNum) || { quyen: qNum, tap: 0, hoi: '', pham: '', p_in: '' };
    results.push({
      quyen: qNum,
      count: totalCount,
      meta,
      excerpts: null // loaded on demand or when expanded
    });
  }

  // Sort descending by count / relevance
  results.sort((a, b) => b.count - a.count);
  return results;
}

/**
 * Fetch a specific Quyển and extract matching sentence excerpts with highlights
 */
export async function fetchQuyenExcerpts(quyenNum, query, quyenList = [], maxExcerpts = 3) {
  const meta = quyenList.find(q => q.quyen === quyenNum);
  if (!meta || !meta.file) return [];

  try {
    const resp = await fetch(meta.file);
    if (!resp.ok) return [];
    const text = await resp.text();

    const qLower = query.toLowerCase().trim();
    const regex = new RegExp(`([^.?!;\n]{0,80})(${escapeRegExp(qLower)})([^.?!;\n]{0,80})`, 'gi');

    const matches = [];
    let match;
    let count = 0;

    // Split text into paragraphs
    const paragraphs = text.split('\n').filter(p => p.trim() && !p.startsWith('#') && !p.startsWith('|') && !p.startsWith('*'));

    for (const p of paragraphs) {
      if (p.toLowerCase().includes(qLower)) {
        // Highlight keyword
        const highlighted = p.replace(
          new RegExp(`(${escapeRegExp(query)})`, 'gi'),
          '<mark class="search-keyword-highlight">$1</mark>'
        );
        matches.push(highlighted);
        count++;
        if (count >= maxExcerpts) break;
      }
    }

    return matches;
  } catch (err) {
    console.error(`Error fetching excerpts for Quyển ${quyenNum}:`, err);
    return [];
  }
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
