import sys
sys.path.insert(0, '.')
import pypdf
import os
import re
from scripts.batch_processor import process_quyen, validate_quality_gates

pdf_path = 'Kinh Bát Nhã/Kinh Đại Bát Nhã - Tập 08.PDF'
reader = pypdf.PdfReader(pdf_path)
total = len(reader.pages)

# 1. Build exact printed page mapping
exact_page_in = [None] * total

# Part 1: pages 0 to 186 (Quyển 390 to 400)
for i in range(187):
    lines = [l.strip() for l in (reader.pages[i].extract_text() or '').split('\n') if l.strip()]
    for l in lines[:3] + lines[-3:]:
        if re.match(r'^\d+$', l):
            val = int(l)
            if val > 10:
                exact_page_in[i] = val
                break

for i in range(187):
    if exact_page_in[i] is None:
        if i + 1 < 187 and exact_page_in[i+1] is not None:
            exact_page_in[i] = exact_page_in[i+1] - 1
        elif i > 0 and exact_page_in[i-1] is not None:
            exact_page_in[i] = exact_page_in[i-1] + 1

for i in range(185, -1, -1):
    if exact_page_in[i] is None and exact_page_in[i+1] is not None:
        exact_page_in[i] = exact_page_in[i+1] - 1

# Part 2: pages 187 to total-1 (Hội 2: Quyển 401 to 435)
for i in range(187, total):
    lines = [l.strip() for l in (reader.pages[i].extract_text() or '').split('\n') if l.strip()]
    for l in lines[:3] + lines[-3:]:
        if re.match(r'^\d+$', l):
            val = int(l)
            if i == 187:
                continue
            exact_page_in[i] = val
            break

for i in range(187, total):
    if exact_page_in[i] is None:
        if i + 1 < total and exact_page_in[i+1] is not None:
            exact_page_in[i] = exact_page_in[i+1] - 1
        elif i > 187 and exact_page_in[i-1] is not None:
            exact_page_in[i] = exact_page_in[i-1] + 1

for i in range(total - 2, 186, -1):
    if exact_page_in[i] is None and exact_page_in[i+1] is not None:
        exact_page_in[i] = exact_page_in[i+1] - 1

page_in_map = {p+1: exact_page_in[p] for p in range(total)}

quyen_data = [
    (390, 1, 18, 'LXX. PHẨM BẤT KHẢ ĐỘNG (05) & LXXI. PHẨM THÀNH THỤC HỮU TÌNH (01)'),
    (391, 19, 34, 'LXXI. PHẨM THÀNH THỤC HỮU TÌNH (02)'),
    (392, 35, 49, 'LXXI. PHẨM THÀNH THỤC HỮU TÌNH (03)'),
    (393, 50, 67, 'LXXI. PHẨM THÀNH THỤC HỮU TÌNH (04) & LXXII. PHẨM NGHIÊM TỊNH CÕI PHẬT (01)'),
    (394, 68, 86, 'LXXII. PHẨM NGHIÊM TỊNH CÕI PHẬT (02) & LXXIII. PHẨM TỊNH ĐỘ PHƯƠNG TIỆN (01)'),
    (395, 87, 103, 'LXXIII. PHẨM TỊNH ĐỘ PHƯƠNG TIỆN (02) & LXXIV. PHẨM VÔ TÁNH TỰ TÁNH (01)'),
    (396, 104, 124, 'LXXIV. PHẨM VÔ TÁNH TỰ TÁNH (02) & LXXV. PHẨM THẮNG NGHĨA DU-GIÀ (01)'),
    (397, 125, 143, 'LXXV. PHẨM THẮNG NGHĨA DU-GIÀ (02) & LXXVI. PHẨM PHÁP TÁNH VÔ ĐỘNG (01)'),
    (398, 144, 157, 'LXXVII. PHẨM BỒ-TÁT THƯỜNG ĐỀ (01)'),
    (399, 158, 172, 'LXXVII. PHẨM BỒ-TÁT THƯỜNG ĐỀ (02) & LXXVIII. PHẨM BỒ-TÁT PHÁP DŨNG (01)'),
    (400, 173, 187, 'LXXVIII. PHẨM BỒ-TÁT PHÁP DŨNG (02) & LXXIX. PHẨM KẾT KHUYẾN'),
    (401, 188, 206, 'I. PHẨM DUYÊN KHỞI'),
    (402, 207, 221, 'II. PHẨM HOAN HỶ & III. PHẨM QUÁN CHIẾU (01)'),
    (403, 222, 237, 'III. PHẨM QUÁN CHIẾU (02)'),
    (404, 238, 254, 'III. PHẨM QUÁN CHIẾU (03)'),
    (405, 255, 271, 'IV. PHẨM VÔ ĐẲNG ĐẲNG & V. PHẨM TƯỚNG THIỆT CĂN'),
    (406, 272, 291, 'VI. PHẨM THIỆN HIỆN (01)'),
    (407, 292, 319, 'VI. PHẨM THIỆN HIỆN (02)'),
    (408, 320, 341, 'VII. PHẨM LY SANH & VIII. PHẨM THẮNG QUÂN (01)'),
    (409, 342, 358, 'VIII. PHẨM THẮNG QUÂN (02) & IX. PHẨM HÀNH TƯỚNG (01)'),
    (410, 359, 376, 'IX. PHẨM HÀNH TƯỚNG (02) & X. PHẨM HUYỄN DỤ'),
    (411, 377, 394, 'XI. PHẨM THÍ DỤ & XII. PHẨM ĐOẠN CHƯ KIẾN & XIII. PHẨM LỤC ĐÁO BỈ NGẠN (01)'),
    (412, 395, 411, 'XIII. PHẨM LỤC ĐÁO BỈ NGẠN (02) & XIV. PHẨM NƯƠNG ĐẠI THỪA'),
    (413, 412, 430, 'XV. PHẨM KHÔNG BUỘC, KHÔNG MỞ & XVI. PHẨM TAM-MA-ĐỊA (01)'),
    (414, 431, 448, 'XVI. PHẨM TAM-MA-ĐỊA (02) & XVII. PHẨM NIỆM TRỤ ĐẲNG'),
    (415, 449, 466, 'XVIII. PHẨM TU TRỊ ĐỊA (01)'),
    (416, 467, 483, 'XIX. PHẨM XUẤT TRỤ'),
    (417, 484, 502, 'XX. PHẨM SIÊU THẮNG'),
    (418, 503, 518, 'XXI. PHẨM VÔ SỞ HỮU (01)'),
    (419, 519, 534, 'XXI. PHẨM VÔ SỞ HỮU (02)'),
    (420, 535, 551, 'XXII. PHẨM TÙY THUẬN & XXIII. PHẨM VÔ BIÊN TẾ (01)'),
    (421, 552, 565, 'XXIII. PHẨM VÔ BIÊN TẾ (02)'),
    (422, 566, 581, 'XXIII. PHẨM VÔ BIÊN TẾ (03)'),
    (423, 582, 598, 'XXIII. PHẨM VÔ BIÊN TẾ (04) & XXIV. PHẨM VIỄN LY (01)'),
    (424, 599, 613, 'XXIV. PHẨM VIỄN LY (02)'),
    (425, 614, 628, 'XXV. PHẨM ĐẾ THÍCH'),
    (426, 629, 639, 'XXVI. PHẨM TÍN THỌ & XXVII. PHẨM TÁN HOA'),
    (427, 640, 660, 'XXVIII. PHẨM THỌ KÝ & XXIX. PHẨM NHIẾP THỌ (01)'),
    (428, 661, 681, 'XXIX. PHẨM NHIẾP THỌ (02) & XXX. PHẨM BẢO THÁP'),
    (429, 682, 699, 'XXXI. PHẨM PHƯỚC SANH & XXXII. PHẨM CÔNG ĐỨC & XXXIII. PHẨM NGOẠI ĐẠO & XXXIV. PHẨM TRỜI ĐẾN (01)'),
    (430, 700, 717, 'XXXIV. PHẨM TRỜI ĐẾN (02) & XXXV. PHẨM THIẾT-LỢI-LA'),
    (431, 718, 735, 'XXXVI. PHẨM KINH VĂN (01)'),
    (432, 736, 751, 'XXXVI. PHẨM KINH VĂN (02) & XXXVII. PHẨM TÙY HỶ HỒI HƯỚNG (01)'),
    (433, 752, 767, 'XXXVII. PHẨM TÙY HỶ HỒI HƯỚNG (02)'),
    (434, 768, 785, 'XXXVIII. PHẨM ĐẠI SƯ & XXXIX. PHẨM ĐỊA NGỤC (01)'),
    (435, 786, 802, 'XXXIX. PHẨM ĐỊA NGỤC (02)'),
]

out_dir = 'Tap_08'
os.makedirs(out_dir, exist_ok=True)

passed = 0
failed = 0

print(f'Starting processing Tập 08: {len(quyen_data)} Quyển (390 to 435)...')

for quyen_num, pdf_s, pdf_e, pham_str in quyen_data:
    p_in_s = page_in_map[pdf_s]
    p_in_e = page_in_map[pdf_e]
    hoi_str = 'HỘI THỨ NHẤT: HỘI ĐẦU' if quyen_num <= 400 else 'HỘI THỨ HAI'
    ok = process_quyen(
        reader=reader,
        tap_num=8,
        quyen_num=quyen_num,
        pdf_start=pdf_s,
        pdf_end=pdf_e,
        p_in_start=p_in_s,
        p_in_end=p_in_e,
        hoi_str=hoi_str,
        phan_str='PHẦN ĐẦU',
        pham_str=pham_str,
        out_dir=out_dir,
        tap_range_str='TỪ QUYỂN 390 ĐẾN QUYỂN 435',
        page_in_map=page_in_map
    )
    if ok:
        passed += 1
    else:
        failed += 1

print(f'\n--- SUMMARY TẬP 08 ---')
print(f'Passed: {passed}/{len(quyen_data)}')
print(f'Failed: {failed}/{len(quyen_data)}')
