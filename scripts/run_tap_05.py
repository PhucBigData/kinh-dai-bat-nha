import sys
sys.path.insert(0, '.')
import pypdf
import os
import re
from scripts.batch_processor import process_quyen, validate_quality_gates

pdf_path = 'Kinh Bát Nhã/Kinh Đại Bát Nhã - Tập 05.PDF'
reader = pypdf.PdfReader(pdf_path)
total = len(reader.pages)

# 1. Build exact printed page mapping
exact_page_in = [None] * total
for i in range(total):
    t = reader.pages[i].extract_text() or ''
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    for l in lines[:3] + lines[-3:]:
        if re.match(r'^\d+$', l):
            val = int(l)
            if val >= 200: # Page numbers in Tập 05 start around 352
                exact_page_in[i] = val
                break

for i in range(total):
    if exact_page_in[i] is None:
        if i + 1 < total and exact_page_in[i+1] is not None:
            exact_page_in[i] = exact_page_in[i+1] - 1
        elif i > 0 and exact_page_in[i-1] is not None:
            exact_page_in[i] = exact_page_in[i-1] + 1

for i in range(total - 2, -1, -1):
    if exact_page_in[i] is None and exact_page_in[i+1] is not None:
        exact_page_in[i] = exact_page_in[i+1] - 1

page_in_map = {p+1: exact_page_in[p] for p in range(total)}

ends = {
    221: 15, 222: 31, 223: 47, 224: 63, 225: 81, 226: 97, 227: 114, 228: 130,
    229: 148, 230: 163, 231: 179, 232: 196, 233: 214, 234: 230, 235: 246,
    236: 262, 237: 279, 238: 295, 239: 312, 240: 327, 241: 343, 242: 359,
    243: 375, 244: 392, 245: 408, 246: 423, 247: 438, 248: 454, 249: 471,
    250: 488, 251: 507, 252: 525, 253: 541, 254: 558, 255: 575, 256: 591,
    257: 607, 258: 624, 259: 640, 260: 656, 261: 672, 262: 688, 263: 705,
    264: 721, 265: 736, 266: 754, 267: 770, 268: 786, 269: 803, 270: 819,
    271: 835, 272: 851, 273: 867, 274: 884, 275: 900, 276: 916, 277: 934,
    278: 950, 279: 965, 280: 982, 281: 1000, 282: 1018, 283: 1037, 284: 1054
}

quyen_data = []
cur_start = 1
for q in range(221, 285):
    cur_end = ends[q]
    sub = q - 221 + 40
    pham = f'XXXIV. PHẨM KHÓ TIN HIỂU ({sub:02d})'
    quyen_data.append((q, cur_start, cur_end, pham))
    cur_start = cur_end + 1

out_dir = 'Tap_05'
os.makedirs(out_dir, exist_ok=True)

passed = 0
failed = 0

print(f'Starting processing Tập 05: {len(quyen_data)} Quyển (221 to 284)...')

for quyen_num, pdf_s, pdf_e, pham_str in quyen_data:
    p_in_s = page_in_map[pdf_s]
    p_in_e = page_in_map[pdf_e]
    ok = process_quyen(
        reader=reader,
        tap_num=5,
        quyen_num=quyen_num,
        pdf_start=pdf_s,
        pdf_end=pdf_e,
        p_in_start=p_in_s,
        p_in_end=p_in_e,
        hoi_str='HỘI THỨ NHẤT: HỘI ĐẦU',
        phan_str='PHẦN ĐẦU',
        pham_str=pham_str,
        out_dir=out_dir,
        tap_range_str='TỪ QUYỂN 221 ĐẾN QUYỂN 284',
        page_in_map=page_in_map
    )
    if ok:
        passed += 1
    else:
        failed += 1

print(f'\n--- SUMMARY TẬP 05 ---')
print(f'Passed: {passed}/{len(quyen_data)}')
print(f'Failed: {failed}/{len(quyen_data)}')
