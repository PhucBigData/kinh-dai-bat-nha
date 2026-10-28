import sys
sys.path.insert(0, '.')
import pypdf
import os
import re
from scripts.batch_processor import process_quyen, validate_quality_gates

pdf_path = 'Kinh Bát Nhã/Kinh Đại Bát Nhã - Tập 10.PDF'
reader = pypdf.PdfReader(pdf_path)
total = len(reader.pages)

# 1. Build exact printed page mapping
exact_page_in = [None] * total

for i in range(total):
    lines = [l.strip() for l in (reader.pages[i].extract_text() or '').split('\n') if l.strip()]
    for l in lines[:3] + lines[-3:]:
        if re.match(r'^\d+$', l):
            val = int(l)
            if val > 10:
                exact_page_in[i] = val
                break

for i in range(total):
    if exact_page_in[i] is None:
        if i > 0 and exact_page_in[i-1] is not None:
            exact_page_in[i] = exact_page_in[i-1] + 1

for i in range(total-1, -1, -1):
    if exact_page_in[i] is None:
        if i + 1 < total and exact_page_in[i+1] is not None:
            exact_page_in[i] = exact_page_in[i+1] - 1

page_in_map = {p+1: exact_page_in[p] for p in range(total)}

quyen_data = [
    (499, 5, 21, 'IV. PHẨM THIÊN ĐẾ'),
    (500, 22, 39, 'IV. PHẨM THIÊN ĐẾ & V. PHẨM HIỆN BẢO THÁP'),
    (501, 40, 56, 'V. PHẨM HIỆN BẢO THÁP'),
    (502, 57, 75, 'V. PHẨM HIỆN BẢO THÁP & VI. PHẨM XƯNG DƯƠNG CÔNG ĐỨC'),
    (503, 76, 91, 'VII. PHẨM XÁ-LỢI PHẬT & VIII. PHẨM PHƯỚC TỤ'),
    (504, 92, 110, 'VIII. PHẨM PHƯỚC TỤ & IX. PHẨM TÙY HỶ HỒI HƯỚNG'),
    (505, 111, 129, 'IX. PHẨM TÙY HỶ HỒI HƯỚNG & X. PHẨM ĐỊA NGỤC'),
    (506, 130, 150, 'X. PHẨM ĐỊA NGỤC & XI. PHẨM TÁN THÁN THANH TỊNH'),
    (507, 151, 171, 'XI. PHẨM TÁN THÁN THANH TỊNH & XII. PHẨM TÁN THÁN CÔNG ĐỨC'),
    (508, 172, 189, 'XIII. PHẨM ĐÀ-LA-NI'),
    (509, 190, 212, 'XIII. PHẨM ĐÀ-LA-NI & XIV. PHẨM VIỆC MA'),
    (510, 213, 230, 'XV. PHẨM HIỆN THẾ GIAN'),
    (511, 231, 249, 'XVI. PHẨM BẤT TƯ NGHÌ ĐẲNG & XVII. PHẨM THÍ DỤ'),
    (512, 250, 267, 'XVIII. PHẨM BẠN LÀNH'),
    (513, 268, 287, 'XIX. PHẨM CHƠN NHƯ'),
    (514, 288, 307, 'XIX. PHẨM CHƠN NHƯ & XX. PHẨM TƯỚNG BẤT THỐI'),
    (515, 308, 327, 'XX. PHẨM TƯỚNG BẤT THỐI & XXI. PHẨM TƯỚNG KHÔNG'),
    (516, 328, 348, 'XXI. PHẨM TƯỚNG KHÔNG'),
    (517, 349, 368, 'XXI. PHẨM TƯỚNG KHÔNG & XXII. PHẨM CĂNG-GIÀ THIÊN & XXIII. PHẨM XẢO TIỆN'),
    (518, 369, 385, 'XXIII. PHẨM XẢO TIỆN'),
    (519, 386, 411, 'XXIII. PHẨM XẢO TIỆN'),
    (520, 412, 430, 'XXIII. PHẨM XẢO TIỆN & XXIV. PHẨM KHI HỌC'),
    (521, 431, 449, 'XXV. PHẨM THẤY BẤT ĐỘNG'),
    (522, 450, 467, 'XXV. PHẨM THẤY BẤT ĐỘNG'),
    (523, 468, 484, 'XXVI. PHẨM PHƯƠNG TIỆN THIỆN XẢO'),
    (524, 485, 502, 'XXVI. PHẨM PHƯƠNG TIỆN THIỆN XẢO'),
    (525, 503, 526, 'XXVI. PHẨM PHƯƠNG TIỆN THIỆN XẢO'),
    (526, 527, 546, 'XXVI. PHẨM PHƯƠNG TIỆN THIỆN XẢO'),
    (527, 547, 565, 'XXVII. PHẨM TUỆ ĐÁO BỈ NGẠN'),
    (528, 566, 583, 'XXVIII. PHẨM DIỆU TƯỚNG'),
    (529, 584, 599, 'XXVIII. PHẨM DIỆU TƯỚNG'),
    (530, 600, 616, 'XXVIII. PHẨM DIỆU TƯỚNG'),
    (531, 617, 635, 'XXVIII. PHẨM DIỆU TƯỚNG'),
    (532, 636, 656, 'XXVIII. PHẨM DIỆU TƯỚNG & XXIX. PHẨM THÍ BÌNH ĐẲNG'),
    (533, 657, 675, 'XXIX. PHẨM THÍ BÌNH ĐẲNG'),
    (534, 676, 693, 'XXIX. PHẨM THÍ BÌNH ĐẲNG'),
    (535, 694, 711, 'XXIX. PHẨM THÍ BÌNH ĐẲNG & XXX. PHẨM PHẬT QUỐC'),
    (536, 712, 729, 'XXX. PHẨM PHẬT QUỐC & XXXI. PHẨM TUYÊN HÓA'),
    (537, 730, 749, 'XXXI. PHẨM TUYÊN HÓA'),
    (538, 750, 767, 'I. PHẨM DIỆU HẠNH'),
    (539, 768, 787, 'I. PHẨM DIỆU HẠNH & II. PHẨM ĐẾ THÍCH & III. PHẨM CÚNG DƯỜNG BẢO THÁP'),
    (540, 788, 805, 'III. PHẨM CÚNG DƯỜNG BẢO THÁP'),
    (541, 806, 826, 'III. PHẨM CÚNG DƯỜNG BẢO THÁP & IV. PHẨM XƯNG DƯƠNG CÔNG ĐỨC & V. PHẨM PHƯỚC MÔN'),
    (542, 827, 844, 'V. PHẨM PHƯỚC MÔN'),
    (543, 845, 861, 'VI. PHẨM TÙY HỶ HỒI HƯỚNG'),
    (544, 862, 880, 'VI. PHẨM TÙY HỶ HỒI HƯỚNG & VII. PHẨM ĐỊA NGỤC'),
    (545, 881, 903, 'VIII. PHẨM THANH TỊNH & IX. PHẨM KHEN NGỢI & X. PHẨM TỔNG TRÌ'),
    (546, 904, 923, 'X. PHẨM TỔNG TRÌ & XI. PHẨM MA SỰ'),
    (547, 924, 939, 'XI. PHẨM MA SỰ & XII. PHẨM THẾ GIAN'),
]

out_dir = 'Tap_10'
os.makedirs(out_dir, exist_ok=True)

passed = 0
failed = 0

print(f'Starting processing Tập 10: {len(quyen_data)} Quyển (499 to 547)...')

for quyen_num, pdf_s, pdf_e, pham_str in quyen_data:
    p_in_s = page_in_map[pdf_s]
    p_in_e = page_in_map[pdf_e]
    hoi_str = 'HỘI THỨ BA' if quyen_num <= 537 else 'HỘI THỨ TƯ'
    ok = process_quyen(
        reader=reader,
        tap_num=10,
        quyen_num=quyen_num,
        pdf_start=pdf_s,
        pdf_end=pdf_e,
        p_in_start=p_in_s,
        p_in_end=p_in_e,
        hoi_str=hoi_str,
        phan_str='PHẦN ĐẦU',
        pham_str=pham_str,
        out_dir=out_dir,
        tap_range_str='TỪ QUYỂN 499 ĐẾN QUYỂN 547',
        page_in_map=page_in_map
    )
    if ok:
        passed += 1
    else:
        failed += 1

print(f'\n--- SUMMARY TẬP 10 ---')
print(f'Passed: {passed}/{len(quyen_data)}')
print(f'Failed: {failed}/{len(quyen_data)}')
