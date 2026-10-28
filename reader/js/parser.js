/**
 * Prajñā Markdown Parser (Master Buddhist Typography Edition)
 * Zero duplicate dividers, pure sacred scripture typography
 */

export function parseMarkdown(mdText) {
  if (!mdText) return '';

  const lines = mdText.split('\n');
  const items = [];
  let inMetaList = false;
  let inScripture = false;
  let dropCapApplied = false;
  let skippingAuditBlock = false;

  for (let i = 0; i < lines.length; i++) {
    const rawLine = lines[i];
    const line = rawLine.trim();

    // Skip empty lines
    if (!line) continue;

    // Detect audit block: skip from "BẢNG ĐỐI CHIẾU" until "NỘI DUNG KINH VĂN"
    if (line.startsWith('### BẢNG ĐỐI CHIẾU TRANG NGUYÊN BẢN')) {
      skippingAuditBlock = true;
      continue;
    }

    if (skippingAuditBlock) {
      if (line.startsWith('### NỘI DUNG KINH VĂN')) {
        skippingAuditBlock = false;
        inScripture = true;
        // Introduce scripture with a single sacred divider
        items.push({ type: 'divider', content: '<div class="lotus-divider"><span class="lotus-symbol">☸</span></div>' });
      }
      continue;
    }

    // Skip markdown tables entirely
    if (line.startsWith('|') && line.endsWith('|')) {
      continue;
    }

    // Skip "NỘI DUNG KINH VĂN" heading if reached normally
    if (line.startsWith('### NỘI DUNG KINH VĂN')) {
      inScripture = true;
      items.push({ type: 'divider', content: '<div class="lotus-divider"><span class="lotus-symbol">☸</span></div>' });
      continue;
    }

    // Metadata Translator List
    if (line.startsWith('* ') || line.startsWith('- ')) {
      if (!inMetaList) {
        inMetaList = true;
        items.push({ type: 'meta-open', content: '<div class="scripture-tribute-card"><ul class="meta-list">' });
      }
      const itemText = line.substring(2);
      items.push({ type: 'meta-item', content: `<li>${inlineFormat(itemText)}</li>` });
      continue;
    } else if (inMetaList) {
      inMetaList = false;
      items.push({ type: 'meta-close', content: '</ul></div>' });
    }

    // Dividers: check and debounce
    if (line === '---' || line === '***') {
      items.push({ type: 'divider', content: '<div class="lotus-divider"><span class="lotus-symbol">☸</span></div>' });
      continue;
    }

    // End of Fascicle Marker
    if (line.startsWith('**QUYỂN THỨ') && line.includes('(HẾT)**')) {
      items.push({
        type: 'end-marker',
        content: `
          <div class="quyen-end-marker">
            <div class="end-ornament">❖</div>
            <div class="end-text">${inlineFormat(line.replace(/\*\*/g, ''))}</div>
            <div class="end-sub">Nam Mô Bát Nhã Hội Thượng Phật Bồ Tát Ma Ha Tát</div>
          </div>
        `
      });
      continue;
    }

    // Headings
    if (line.startsWith('# ')) {
      items.push({ type: 'h1', content: `<h1 class="kinh-main-title">${inlineFormat(line.substring(2))}</h1>` });
      continue;
    }
    if (line.startsWith('## ')) {
      items.push({ type: 'h2', content: `<h2 class="tap-sub-title">${inlineFormat(line.substring(3))}</h2>` });
      continue;
    }
    if (line.startsWith('### ')) {
      items.push({ type: 'h3', content: `<h3 class="hoi-banner">${inlineFormat(line.substring(4))}</h3>` });
      continue;
    }
    if (line.startsWith('#### ')) {
      items.push({ type: 'h4', content: `<h4 class="phan-banner">${inlineFormat(line.substring(5))}</h4>` });
      continue;
    }
    if (line.startsWith('##### ')) {
      items.push({ type: 'h5', content: `<h5 class="pham-banner">${inlineFormat(line.substring(6))}</h5>` });
      continue;
    }
    if (line.startsWith('###### ')) {
      items.push({ type: 'h6', content: `<h6 class="quyen-banner">${inlineFormat(line.substring(7))}</h6>` });
      continue;
    }

    // Scope note (convert to subtle text instead of bulky pill)
    if (line.startsWith('*(') && line.endsWith(')*')) {
      // Skip or render very discreetly without dividers
      continue;
    }

    // Dialogue format (lines starting with dash)
    if (line.startsWith('-') || line.startsWith('—')) {
      const dialogueText = line.replace(/^[-—]\s*/, '');
      items.push({
        type: 'p-dialogue',
        content: `<p class="kinh-paragraph dialogue"><span class="dash">—</span>${inlineFormat(dialogueText)}</p>`
      });
      continue;
    }

    // Normal scripture paragraph
    // Apply Drop-Cap to the FIRST scripture paragraph of every fascicle
    if (inScripture && !dropCapApplied && line.length > 5) {
      dropCapApplied = true;
      const firstChar = line.charAt(0);
      const rest = line.substring(1);
      items.push({
        type: 'p-dropcap',
        content: `<p class="kinh-paragraph has-drop-cap"><span class="drop-cap">${firstChar}</span>${inlineFormat(rest)}</p>`
      });
      continue;
    }

    items.push({
      type: 'p',
      content: `<p class="kinh-paragraph">${inlineFormat(line)}</p>`
    });
  }

  if (inMetaList) {
    items.push({ type: 'meta-close', content: '</ul></div>' });
  }

  // Debounce consecutive dividers: ensure NO TWO DIVIDERS appear consecutively
  const finalHtml = [];
  let lastWasDivider = false;

  for (const item of items) {
    if (item.type === 'divider') {
      if (lastWasDivider) {
        continue; // Discard consecutive divider!
      }
      lastWasDivider = true;
    } else {
      lastWasDivider = false;
    }
    finalHtml.push(item.content);
  }

  return finalHtml.join('\n');
}

function inlineFormat(text) {
  if (!text) return '';
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\(卍\)/g, '<span class="swastika-badge" title="Vạn tự cát tường">卍</span>');
}
