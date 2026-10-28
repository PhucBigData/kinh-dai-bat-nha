import sys
sys.path.insert(0, '.')
import pypdf
import os
import re
from scripts.batch_processor import process_quyen, validate_quality_gates

pdf_path = 'Kinh Bát Nhã/Kinh Đại Bát Nhã - Tập 07.PDF'
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
        if i + 1 < total and exact_page_in[i+1] is not None:
            exact_page_in[i] = exact_page_in[i+1] - 1
        elif i > 0 and exact_page_in[i-1] is not None:
            exact_page_in[i] = exact_page_in[i-1] + 1

for i in range(total - 2, -1, -1):
    if exact_page_in[i] is None and exact_page_in[i+1] is not None:
        exact_page_in[i] = exact_page_in[i+1] - 1

page_in_map = {p+1: exact_page_in[p] for p in range(total)}

quyen_data = [
    (337, 1, 15, 'LV. PHẨM HỌC PHƯƠNG TIỆN THIỆN XẢO (01)'),
    (338, 16, 30, 'LV. PHẨM HỌC PHƯƠNG TIỆN THIỆN XẢO (02)'),
    (339, 31, 45, 'LV. PHẨM HỌC PHƯƠNG TIỆN THIỆN XẢO (03)'),
    (340, 46, 62, 'LV. PHẨM HỌC PHƯƠNG TIỆN THIỆN XẢO (04)'),
    (341, 63, 80, 'LV. PHẨM HỌC PHƯƠNG TIỆN THIỆN XẢO (05) & LVI. PHẨM NGUYỆN DỤ (01)'),
    (342, 81, 100, 'LVI. PHẨM NGUYỆN DỤ (02) & LVII. PHẨM KHEN TÁNH CHẮC THẬT (01)'),
    (343, 101, 118, 'LVII. PHẨM KHEN TÁNH CHẮC THẬT (02)'),
    (344, 119, 136, 'LVII. PHẨM KHEN TÁNH CHẮC THẬT (03)'),
    (345, 137, 154, 'LVII. PHẨM KHEN TÁNH CHẮC THẬT (04)'),
    (346, 155, 171, 'LVII. PHẨM KHEN TÁNH CHẮC THẬT (05) & LVIII. PHẨM CHÚC LỤY (01)'),
    (347, 172, 189, 'LVIII. PHẨM CHÚC LỤY (02) & LIX. PHẨM VÔ TẬN (01)'),
    (348, 190, 204, 'LIX. PHẨM VÔ TẬN (02)'),
    (349, 205, 219, 'LX. PHẨM DẪN NHIẾP NHAU (01)'),
    (350, 220, 234, 'LX. PHẨM DẪN NHIẾP NHAU (02)'),
    (351, 235, 250, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (01)'),
    (352, 251, 267, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (02)'),
    (353, 268, 284, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (03)'),
    (354, 285, 302, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (04)'),
    (355, 303, 318, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (05)'),
    (356, 319, 335, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (06)'),
    (357, 336, 354, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (07)'),
    (358, 355, 372, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (08)'),
    (359, 373, 389, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (09)'),
    (360, 390, 406, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (10)'),
    (361, 407, 423, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (11)'),
    (362, 424, 440, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (12)'),
    (363, 441, 459, 'LXI. PHẨM ĐA VẤN BẤT NHỊ (13) & LXII. PHẨM NÓI THẬT (01)'),
    (364, 460, 477, 'LXII. PHẨM NÓI THẬT (02)'),
    (365, 478, 494, 'LXII. PHẨM NÓI THẬT (03) & LXIII. PHẨM XẢO TIỆN HÀNH (01)'),
    (366, 495, 510, 'LXIII. PHẨM XẢO TIỆN HÀNH (02) & LXIV. PHẨM HỌC ĐẠO KHẮP (01)'),
    (367, 511, 525, 'LXIV. PHẨM HỌC ĐẠO KHẮP (02)'),
    (368, 526, 539, 'LXIV. PHẨM HỌC ĐẠO KHẮP (03)'),
    (369, 540, 555, 'LXIV. PHẨM HỌC ĐẠO KHẮP (04)'),
    (370, 556, 570, 'LXIV. PHẨM HỌC ĐẠO KHẮP (05)'),
    (371, 571, 586, 'LXIV. PHẨM HỌC ĐẠO KHẮP (06)'),
    (372, 587, 588, 'LXIV. PHẨM HỌC ĐẠO KHẮP (07)'),
    (373, 589, 593, 'LXVI. PHẨM VÔ TƯỚNG VÔ ĐẮC (01)'),
    (374, 594, 610, 'LXVI. PHẨM VÔ TƯỚNG VÔ ĐẮC (02)'),
    (375, 611, 627, 'LXVI. PHẨM VÔ TƯỚNG VÔ ĐẮC (03)'),
    (376, 628, 643, 'LXVI. PHẨM VÔ TƯỚNG VÔ ĐẮC (04)'),
    (377, 644, 658, 'LXVI. PHẨM VÔ TƯỚNG VÔ ĐẮC (05)'),
    (378, 659, 674, 'LXVI. PHẨM VÔ TƯỚNG VÔ ĐẮC (06) & LXVII. PHẨM PHÁP NGHĨA VÔ TẠP (01)'),
    (379, 675, 690, 'LXVII. PHẨM PHÁP NGHĨA VÔ TẠP (02) & LXVIII. PHẨM TƯỚNG CÁC CÔNG ĐỨC (01)'),
    (380, 691, 706, 'LXVIII. PHẨM TƯỚNG CÁC CÔNG ĐỨC (02)'),
    (381, 707, 723, 'LXVIII. PHẨM TƯỚNG CÁC CÔNG ĐỨC (03)'),
    (382, 724, 741, 'LXVIII. PHẨM TƯỚNG CÁC CÔNG ĐỨC (04)'),
    (383, 742, 760, 'LXVIII. PHẨM TƯỚNG CÁC CÔNG ĐỨC (05) & LXIX. PHẨM CÁC PHÁP BÌNH ĐẲNG (01)'),
    (384, 761, 778, 'LXIX. PHẨM CÁC PHÁP BÌNH ĐẲNG (02)'),
    (385, 779, 795, 'LXIX. PHẨM CÁC PHÁP BÌNH ĐẲNG (03)'),
    (386, 796, 811, 'LXIX. PHẨM CÁC PHÁP BÌNH ĐẲNG (04) & LXX. PHẨM BẤT KHẢ ĐỘNG (01)'),
    (387, 812, 828, 'LXX. PHẨM BẤT KHẢ ĐỘNG (02)'),
    (388, 829, 846, 'LXX. PHẨM BẤT KHẢ ĐỘNG (03)'),
    (389, 847, 864, 'LXX. PHẨM BẤT KHẢ ĐỘNG (04)'),
]

out_dir = 'Tap_07'
os.makedirs(out_dir, exist_ok=True)

passed = 0
failed = 0

print(f'Starting processing Tập 07: {len(quyen_data)} Quyển (337 to 389)...')

for quyen_num, pdf_s, pdf_e, pham_str in quyen_data:
    p_in_s = page_in_map[pdf_s]
    p_in_e = page_in_map[pdf_e]
    ok = process_quyen(
        reader=reader,
        tap_num=7,
        quyen_num=quyen_num,
        pdf_start=pdf_s,
        pdf_end=pdf_e,
        p_in_start=p_in_s,
        p_in_end=p_in_e,
        hoi_str='HỘI THỨ NHẤT: HỘI ĐẦU',
        phan_str='PHẦN ĐẦU',
        pham_str=pham_str,
        out_dir=out_dir,
        tap_range_str='TỪ QUYỂN 337 ĐẾN QUYỂN 389',
        page_in_map=page_in_map
    )
    if ok:
        passed += 1
    else:
        failed += 1

print(f'\n--- SUMMARY TẬP 07 ---')
print(f'Passed: {passed}/{len(quyen_data)}')
print(f'Failed: {failed}/{len(quyen_data)}')
