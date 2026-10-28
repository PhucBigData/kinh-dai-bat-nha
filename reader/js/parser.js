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

/**
 * Standard Buddhist Liturgy: Opening Ritual (Nghi thức Khai kinh)
 */
export function renderOpeningRitual() {
  return `
    <section class="ritual-block ritual-opening" id="ritual-opening">
      <div class="ritual-header">
        <div class="ritual-tag-wrap">
          <span class="ritual-lotus">☸</span>
          <span class="ritual-tag">NGHI THỨC KHAI KINH</span>
        </div>
        <button class="ritual-collapse-btn" data-target="ritual-opening-body" title="Ẩn/Hiện nghi thức khai kinh">
          <span class="collapse-icon">▲</span>
          <span class="collapse-text">Thu gọn</span>
        </button>
      </div>

      <div class="ritual-body" id="ritual-opening-body">
        <div class="ritual-section">
          <h4 class="ritual-section-title">I. NGUYỆN HƯƠNG</h4>
          <p class="ritual-verse">
            Nguyện đem lòng thành kính,<br>
            Gửi theo đám mây hương,<br>
            Phảng phất khắp mười phương,<br>
            Cúng dường ngôi Tam Bảo.<br>
            Thề trọn đời giữ đạo,<br>
            Theo tự tánh làm lành,<br>
            Cùng pháp giới chúng sanh,<br>
            Cầu Phật từ gia hộ:<br>
            Tâm bồ-đề kiên cố,<br>
            Chí tu học vững bền,<br>
            Xa biển khổ nguồn mê,<br>
            Chóng quay về bờ giác.
          </p>
          <p class="ritual-bell-cue"><em>(1 tiếng chuông, xá 1 xá)</em></p>
        </div>

        <div class="ritual-section">
          <h4 class="ritual-section-title">II. TÁN PHẬT & ĐẢNH LỄ</h4>
          <p class="ritual-verse">
            Đấng Pháp Vương vô thượng,<br>
            Ba cõi chẳng ai bằng,<br>
            Thầy dạy khắp trời người,<br>
            Cha lành chung bốn loài.<br>
            Quy y tròn một niệm,<br>
            Dứt sạch nghiệp ba kỳ,<br>
            Xưng dương cùng tán thán,<br>
            Ức kiếp không cùng tận.
          </p>
          <div class="ritual-prose">
            <p><strong>Chí tâm đảnh lễ:</strong> Nam Mô Tận Hư Không Biến Pháp Giới Quá Hiện Vị Lai Thập Phương Chư Phật, Tôn Pháp, Hiền Thánh Tăng Thường Trụ Tam Bảo. <span class="cue"><em>(1 tiếng chuông, lạy 1 lạy)</em></span></p>
            <p><strong>Chí tâm đảnh lễ:</strong> Nam Mô Ta Bà Giáo Chủ Điều Ngự Bổn Sư Thích Ca Mâu Ni Phật, Đương Lai Hạ Sanh Di Lặc Tôn Phật, Đại Trí Văn Thù Sư Lợi Bồ Tát, Đại Hạnh Phổ Hiền Bồ Tát, Hộ Pháp Chư Tôn Bồ Tát, Linh Sơn Hội Thượng Phật Bồ Tát. <span class="cue"><em>(1 tiếng chuông, lạy 1 lạy)</em></span></p>
            <p><strong>Chí tâm đảnh lễ:</strong> Nam Mô Tây Phương Cực Lạc Thế Giới Đại Từ Đại Bi A Di Đà Phật, Đại Bi Quán Thế Âm Bồ Tát, Đại Thế Chí Bồ Tát, Đại Nguyện Địa Tạng Vương Bồ Tát, Thanh Tịnh Đại Hải Chúng Bồ Tát. <span class="cue"><em>(1 tiếng chuông, lạy 1 lạy)</em></span></p>
          </div>
        </div>

        <div class="ritual-section">
          <h4 class="ritual-section-title">III. KỆ KHAI KINH</h4>
          <p class="ritual-verse highlight-verse">
            Vô thượng thậm thâm vi diệu pháp,<br>
            Bá thiên vạn kiếp nan tao ngộ,<br>
            Ngã kim kiến văn đắc thọ trì,<br>
            Nguyện giải Như Lai chân thiệt nghĩa.
          </p>
          <p class="ritual-namo">
            Nam Mô Bát Nhã Hội Thượng Phật Bồ Tát Ma Ha Tát. <span class="cue"><em>(3 lần, 3 tiếng chuông)</em></span>
          </p>
        </div>
      </div>
    </section>
  `;
}

/**
 * Standard Buddhist Liturgy: Closing Ritual (Bát Nhã Tâm Kinh & Hồi Hướng)
 */
export function renderClosingRitual() {
  return `
    <section class="ritual-block ritual-closing" id="ritual-closing">
      <div class="ritual-header">
        <div class="ritual-tag-wrap">
          <span class="ritual-lotus">☸</span>
          <span class="ritual-tag">BÁT NHÃ TÂM KINH & HỒI HƯỚNG</span>
        </div>
        <button class="ritual-collapse-btn" data-target="ritual-closing-body" title="Ẩn/Hiện nghi thức hoàn kinh">
          <span class="collapse-icon">▲</span>
          <span class="collapse-text">Thu gọn</span>
        </button>
      </div>

      <div class="ritual-body" id="ritual-closing-body">
        <div class="ritual-section">
          <h4 class="ritual-section-title">I. MA HA BÁT NHÃ BA LA MẬT ĐA TÂM KINH</h4>
          <div class="ritual-prose">
            <p>Khi Quán Tự Tại Bồ Tát hành sâu Bát-nhã Ba-la-mật-đa, soi thấy năm uẩn đều không, qua hết thảy khổ ách.</p>
            <p>Này Xá-lợi Tử! Sắc chẳng khác không, không chẳng khác sắc; sắc tức là không, không tức là sắc. Thọ, tưởng, hành, thức cũng lại như thế.</p>
            <p>Này Xá-lợi Tử! Tướng không của các pháp: không sinh không diệt, không nhơ không sạch, không thêm không bớt. Cho nên trong không: không có sắc, không có thọ, tưởng, hành, thức; không có mắt, tai, mũi, lưỡi, thân, ý; không có sắc, thanh, hương, vị, xúc, pháp; không có giới hạn của mắt, cho đến không có giới hạn của ý thức; không có vô minh, cũng không có hết vô minh; cho đến không có già chết, cũng không có hết già chết; không có khổ, tập, diệt, đạo; không có trí tuệ, cũng không có chứng đắc.</p>
            <p>Vì không có chỗ chứng đắc, Bồ-tát y theo Bát-nhã Ba-la-mật-đa, tâm không ngăn ngại; vì không ngăn ngại nên không sợ hãi, xa lìa điên đảo mộng tưởng, đạt đến cứu cánh Niết-bàn.</p>
            <p>Chư Phật trong ba đời y theo Bát-nhã Ba-la-mật-đa, được đạo quả Vô Thượng Chánh Đẳng Chánh Giác. Nên biết Bát-nhã Ba-la-mật-đa là đại thần chú, là đại minh chú, là vô thượng chú, là vô đẳng đẳng chú, trừ được hết thảy khổ, chân thiệt không hư.</p>
            <p>Vì vậy nói chú Bát-nhã Ba-la-mật-đa, liền nói chú rằng:</p>
            <p class="mantra-text"><strong>Yết-đế yết-đế, ba-la yết-đế, ba-la-tăng yết-đế, bồ-đề tát-bà-ha.</strong> <em>(3 lần)</em></p>
          </div>
        </div>

        <div class="ritual-section">
          <h4 class="ritual-section-title">II. VÃNG SANH QUYẾT ĐỊNH CHÂN NGÔN</h4>
          <p class="ritual-verse">
            Nam-mô a di đa bà dạ, đá tha già đa dạ, đá địa dạ tha.<br>
            A di rị đô bà tỳ, a di rị đa tất đam bà tỳ.<br>
            A di rị đa tì ca lan đế, a di rị đa tì ca lan đá, già di nị, già già na, chỉ đa ca lệ ta-bà-ha. <em>(3 lần)</em>
          </p>
        </div>

        <div class="ritual-section">
          <h4 class="ritual-section-title">III. SÁM HỐI & HỒI HƯỚNG</h4>
          <p class="ritual-verse">
            Tụng kinh công đức thù thắng hạnh,<br>
            Vô biên thắng phước giai hồi hướng,<br>
            Phổ nguyện trầm nịch chư chúng sanh,<br>
            Tốc vãng vô lượng quang Phật sát.<br>
            Nguyện tiêu tam chướng trừ phiền não,<br>
            Nguyện đắc trí tuệ chân minh liễu,<br>
            Phổ nguyện tội chướng tất tiêu trừ,<br>
            Thế thế thường hành Bồ Tát đạo.<br>
            Nguyện sanh Tây phương Tịnh độ trung,<br>
            Cửu phẩm liên hoa vi phụ mẫu,<br>
            Hoa khai kiến Phật ngộ vô sanh,<br>
            Bất thoái Bồ Tát vi bạn lữ.<br>
            Nguyện dĩ thử công đức,<br>
            Phổ cập ư nhất thiết,<br>
            Ngã đẳng dữ chúng sanh,<br>
            Giai cộng thành Phật đạo.
          </p>
        </div>

        <div class="ritual-section">
          <h4 class="ritual-section-title">IV. TAM TỰ QUY Y</h4>
          <div class="ritual-prose">
            <p><strong>Tự quy y Phật:</strong> Xin nguyện chúng sanh, thể theo đạo cả, phát lòng vô thượng. <span class="cue"><em>(1 tiếng chuông, lạy 1 lạy)</em></span></p>
            <p><strong>Tự quy y Pháp:</strong> Xin nguyện chúng sanh, thấu rõ kinh tạng, trí tuệ như biển. <span class="cue"><em>(1 tiếng chuông, lạy 1 lạy)</em></span></p>
            <p><strong>Tự quy y Tăng:</strong> Xin nguyện chúng sanh, thống lý đại chúng, hết thảy không ngại. <span class="cue"><em>(1 tiếng chuông, lạy 1 lạy)</em></span></p>
          </div>
        </div>
      </div>
    </section>
  `;
}
