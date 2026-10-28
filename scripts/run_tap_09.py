import sys
sys.path.insert(0, '.')
import pypdf
import os
import re
from scripts.batch_processor import process_quyen, validate_quality_gates

pdf_path = 'Kinh Bát Nhã/Kinh Đại Bát Nhã - Tập 09.PDF'
reader = pypdf.PdfReader(pdf_path)
total = len(reader.pages)

# 1. Build exact printed page mapping
exact_page_in = [None] * total

for i in range(total):
    lines = [l.strip() for l in (reader.pages[i].extract_text() or '').split('\n') if l.strip()]
    for l in lines[:3] + lines[-3:]:
        if re.match(r'^\d+$', l):
            val = int(l)
            if val > 10: # avoid subnumbers
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
    (436, 1, 20, 'XL. PHẨM THANH TỊNH & XLI. PHẨM KHÔNG NÊU CỜ'),
    (437, 21, 41, 'XLI. PHẨM KHÔNG NÊU CỜ & XLII. PHẨM BẤT KHẢ ĐẮC'),
    (438, 42, 58, 'XLIII. PHẨM PHƯƠNG ĐÔNG BẮC'),
    (439, 59, 74, 'XLIII. PHẨM PHƯƠNG ĐÔNG BẮC'),
    (440, 75, 91, 'XLIII. PHẨM PHƯƠNG ĐÔNG BẮC & XLIV. PHẨM MA SỰ & XLV. PHẨM KHÔNG HÒA HỢP'),
    (441, 92, 107, 'XLV. PHẨM KHÔNG HÒA HỢP & XLVI. PHẨM PHẬT MẪU'),
    (442, 108, 125, 'XLVI. PHẨM PHẬT MẪU & XLVII. PHẨM CHỈ TƯỚNG'),
    (443, 126, 143, 'XLVII. PHẨM CHỈ TƯỚNG'),
    (444, 144, 159, 'XLVIII. PHẨM THÀNH BIỆN & XLIX. PHẨM THUYỀN ĐẲNG DỤ'),
    (445, 160, 174, 'XLIX. PHẨM THUYỀN ĐẲNG DỤ & L. PHẨM SƠ NGHIỆP'),
    (446, 175, 191, 'L. PHẨM SƠ NGHIỆP & LI. PHẨM ĐIỀU PHỤC THAM ĐẲNG & LII. PHẨM CHƠN NHƯ'),
    (447, 192, 208, 'LII. PHẨM CHƠN NHƯ'),
    (448, 209, 225, 'LII. PHẨM CHƠN NHƯ & LIII. PHẨM BẤT THỐI CHUYỂN'),
    (449, 226, 242, 'LIV. PHẨM CHUYỂN BẤT CHUYỂN'),
    (450, 243, 258, 'LV. PHẨM NGHĨA THẬM THÂM'),
    (451, 259, 275, 'LVI. PHẨM MỘNG HÀNH & LVII. PHẨM HẠNH NGUYỆN & LVIII. PHẨM CĂNG-GIÀ THIÊN'),
    (452, 276, 289, 'LIX. PHẨM TẬP CẬN'),
    (453, 290, 303, 'LX. PHẨM TĂNG THƯỢNG MẠN'),
    (454, 304, 323, 'LX. PHẨM TĂNG THƯỢNG MẠN & LXI. PHẨM ĐỒNG HỌC'),
    (455, 324, 339, 'LXI. PHẨM ĐỒNG HỌC & LXII. PHẨM ĐỒNG TÁNH'),
    (456, 340, 356, 'LXII. PHẨM ĐỒNG TÁNH & LXIII. PHẨM KHÔNG PHÂN BIỆT & LXIV. PHẨM KIÊN CỐ CHẲNG KIÊN CỐ'),
    (457, 357, 372, 'LXIV. PHẨM KIÊN CỐ CHẲNG KIÊN CỐ & LXV. PHẨM THẬT NGỮ'),
    (458, 373, 389, 'LXV. PHẨM THẬT NGỮ & LXVI. PHẨM VÔ TẬN'),
    (459, 390, 404, 'LXVII. PHẨM TƯƠNG NHIẾP'),
    (460, 405, 421, 'LXVIII. PHẨM PHƯƠNG TIỆN THIỆN XẢO'),
    (461, 422, 437, 'LXVIII. PHẨM PHƯƠNG TIỆN THIỆN XẢO'),
    (462, 438, 455, 'LXVIII. PHẨM PHƯƠNG TIỆN THIỆN XẢO'),
    (463, 456, 472, 'LXVIII. PHẨM PHƯƠNG TIỆN THIỆN XẢO & LXIX. PHẨM THỌ DỤ'),
    (464, 473, 490, 'LXX. PHẨM BỒ-TÁT HẠNH & LXXI. PHẨM THÂN CẬN & LXXII. PHẨM HỌC TẤT CẢ'),
    (465, 491, 508, 'LXXII. PHẨM HỌC TẤT CẢ & LXXIII. PHẨM TUẦN TỰ'),
    (466, 509, 526, 'LXXIII. PHẨM TUẦN TỰ & LXXIV. PHẨM VÔ TƯỚNG'),
    (467, 527, 543, 'LXXIV. PHẨM VÔ TƯỚNG & LXXV. PHẨM KHÔNG TẠP'),
    (468, 544, 561, 'LXXV. PHẨM KHÔNG TẠP & LXXVI. PHẨM CÁC ĐỨC TƯỚNG'),
    (469, 562, 578, 'LXXVI. PHẨM CÁC ĐỨC TƯỚNG'),
    (470, 579, 596, 'LXXVI. PHẨM CÁC ĐỨC TƯỚNG'),
    (471, 597, 614, 'LXXVI. PHẨM CÁC ĐỨC TƯỚNG & LXXVII. PHẨM THIỆN ĐẠT'),
    (472, 615, 631, 'LXXVII. PHẨM THIỆN ĐẠT'),
    (473, 632, 649, 'LXXVII. PHẨM THIỆN ĐẠT & LXXVIII. PHẨM THẬT TẾ'),
    (474, 650, 666, 'LXXVIII. PHẨM THẬT TẾ & LXXIX. PHẨM VÔ KHUYẾT'),
    (475, 667, 683, 'LXXIX. PHẨM VÔ KHUYẾT'),
    (476, 684, 700, 'LXXX. PHẨM ĐẠO SĨ'),
    (477, 701, 719, 'LXXXI. PHẨM CHÁNH ĐỊNH & LXXXII. PHẨM PHẬT PHÁP'),
    (478, 720, 741, 'LXXXIII. PHẨM VÔ SỰ & LXXXIV. PHẨM NÓI THẬT & LXXXV. PHẨM TÁNH KHÔNG'),
    (479, 742, 759, 'I. PHẨM DUYÊN KHỞI & II. PHẨM XÁ-LỢI TỬ'),
    (480, 760, 777, 'II. PHẨM XÁ-LỢI TỬ'),
    (481, 778, 794, 'II. PHẨM XÁ-LỢI TỬ'),
    (482, 795, 811, 'II. PHẨM XÁ-LỢI TỬ & III. PHẨM THIỆN HIỆN'),
    (483, 812, 830, 'III. PHẨM THIỆN HIỆN'),
    (484, 831, 849, 'III. PHẨM THIỆN HIỆN'),
    (485, 850, 869, 'III. PHẨM THIỆN HIỆN'),
    (486, 870, 888, 'III. PHẨM THIỆN HIỆN'),
    (487, 889, 905, 'III. PHẨM THIỆN HIỆN'),
    (488, 906, 923, 'III. PHẨM THIỆN HIỆN'),
    (489, 924, 939, 'III. PHẨM THIỆN HIỆN'),
    (490, 940, 956, 'III. PHẨM THIỆN HIỆN'),
    (491, 957, 974, 'III. PHẨM THIỆN HIỆN'),
    (492, 975, 992, 'III. PHẨM THIỆN HIỆN'),
    (493, 993, 1007, 'III. PHẨM THIỆN HIỆN'),
    (494, 1008, 1022, 'III. PHẨM THIỆN HIỆN'),
    (495, 1023, 1038, 'III. PHẨM THIỆN HIỆN'),
    (496, 1039, 1055, 'III. PHẨM THIỆN HIỆN'),
    (497, 1056, 1073, 'III. PHẨM THIỆN HIỆN'),
    (498, 1074, 1086, 'III. PHẨM THIỆN HIỆN'),
]

out_dir = 'Tap_09'
os.makedirs(out_dir, exist_ok=True)

passed = 0
failed = 0

print(f'Starting processing Tập 09: {len(quyen_data)} Quyển (436 to 498)...')

for quyen_num, pdf_s, pdf_e, pham_str in quyen_data:
    p_in_s = page_in_map[pdf_s]
    p_in_e = page_in_map[pdf_e]
    hoi_str = 'HỘI THỨ HAI' if quyen_num <= 478 else 'HỘI THỨ BA'
    ok = process_quyen(
        reader=reader,
        tap_num=9,
        quyen_num=quyen_num,
        pdf_start=pdf_s,
        pdf_end=pdf_e,
        p_in_start=p_in_s,
        p_in_end=p_in_e,
        hoi_str=hoi_str,
        phan_str='PHẦN ĐẦU',
        pham_str=pham_str,
        out_dir=out_dir,
        tap_range_str='TỪ QUYỂN 436 ĐẾN QUYỂN 498',
        page_in_map=page_in_map
    )
    if ok:
        passed += 1
    else:
        failed += 1

print(f'\n--- SUMMARY TẬP 09 ---')
print(f'Passed: {passed}/{len(quyen_data)}')
print(f'Failed: {failed}/{len(quyen_data)}')
