import sys
sys.path.insert(0, '.')
import pypdf
import os
import re
from scripts.batch_processor import process_quyen, validate_quality_gates

pdf_path = 'Kinh Bát Nhã/Kinh Đại Bát Nhã - Tập 11.PDF'
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
    (548, 1, 21, 'HỘI THỨ TƯ', 'PHẦN ĐẦU', 'XIV. PHẨM THÍ DỤ & XV. PHẨM TRỜI KHEN NGỢI & XVI. PHẨM CHƠN NHƯ'),
    (549, 22, 41, 'HỘI THỨ TƯ', 'PHẦN ĐẦU', 'XVI. PHẨM CHƠN NHƯ & XVII. PHẨM TƯỚNG BẤT THỐI & XVIII. PHẨM TƯỚNG KHÔNG'),
    (550, 42, 65, 'HỘI THỨ TƯ', 'PHẦN ĐẦU', 'XVIII. PHẨM TƯỚNG KHÔNG & XIX. PHẨM CÔNG ĐỨC SÂU XA & XX. PHẨM CĂNG-GIÀ THIÊN & XXI. PHẨM BIẾT VIỆC MA'),
    (551, 66, 85, 'HỘI THỨ TƯ', 'PHẦN ĐẦU', 'XXI. PHẨM BIẾT VIỆC MA & XXII. PHẨM THIỆN HỮU'),
    (552, 86, 105, 'HỘI THỨ TƯ', 'PHẦN ĐẦU', 'XXII. PHẨM THIỆN HỮU & XXIII. PHẨM THIÊN CHỦ & XXIV. PHẨM VÔ TẠP VÔ DỊ & XXV. PHẨM TẤN TỐC'),
    (553, 106, 125, 'HỘI THỨ TƯ', 'PHẦN ĐẦU', 'XXV. PHẨM TẤN TỐC & XXVI. PHẨM HUYỄN DỤ & XXVII. PHẨM KIÊN CỐ'),
    (554, 126, 148, 'HỘI THỨ TƯ', 'PHẦN ĐẦU', 'XXVII. PHẨM KIÊN CỐ & XXVIII. PHẨM TÁN HOA'),
    (555, 149, 170, 'HỘI THỨ TƯ', 'PHẦN ĐẦU', 'XXIX. PHẨM TÙY THUẬN'),
    (556, 171, 194, 'HỘI THỨ NĂM', 'PHẦN ĐẦU', 'I. PHẨM THIỆN HIỆN & II. PHẨM THIÊN ĐẾ'),
    (557, 195, 213, 'HỘI THỨ NĂM', 'PHẦN ĐẦU', 'III. PHẨM BẢO THÁP & IV. PHẨM THẦN CHÚ'),
    (558, 214, 234, 'HỘI THỨ NĂM', 'PHẦN ĐẦU', 'V. PHẨM XÁ-LỢI & VI. PHẨM KINH ĐIỂN & VII. PHẨM HỒI HƯỚNG'),
    (559, 235, 257, 'HỘI THỨ NĂM', 'PHẦN ĐẦU', 'VIII. PHẨM ĐỊA NGỤC & IX. PHẨM THANH TỊNH & X. PHẨM BẤT TƯ NGHÌ'),
    (560, 258, 277, 'HỘI THỨ NĂM', 'PHẦN ĐẦU', 'X. PHẨM BẤT TƯ NGHÌ & XI. PHẨM MA SỰ & XII. PHẨM CHƠN NHƯ'),
    (561, 278, 298, 'HỘI THỨ NĂM', 'PHẦN ĐẦU', 'XIII. PHẨM THẬM THÂM TƯỚNG & XIV. PHẨM THUYỀN ĐẲNG DỤ & XV. PHẨM NHƯ LAI'),
    (562, 299, 319, 'HỘI THỨ NĂM', 'PHẦN ĐẦU', 'XV. PHẨM NHƯ LAI & XVI. PHẨM BẤT THỐI & XVII. PHẨM THAM HÀNH'),
    (563, 320, 338, 'HỘI THỨ NĂM', 'PHẦN ĐẦU', 'XVII. PHẨM THAM HÀNH & XVIII. PHẨM TỶ MUỘI & XIX. PHẨM MỘNG HÀNH'),
    (564, 339, 358, 'HỘI THỨ NĂM', 'PHẦN ĐẦU', 'XX. PHẨM THẮNG Ý LẠC & XXI. PHẨM TU HỌC & XXII. PHẨM TRỒNG CĂN LÀNH'),
    (565, 359, 376, 'HỘI THỨ NĂM', 'PHẦN ĐẦU', 'XXII. PHẨM TRỒNG CĂN LÀNH & XXIII. PHẨM PHÓ CHÚC & XXIV. PHẨM KIẾN BẤT ĐỘNG PHẬT'),
    (566, 377, 392, 'HỘI THỨ SÁU', 'PHẦN ĐẦU', 'I. PHẨM DUYÊN KHỞI & II. PHẨM THÔNG ĐẠT'),
    (567, 393, 410, 'HỘI THỨ SÁU', 'PHẦN ĐẦU', 'III. PHẨM HIỂN TƯỚNG & IV. PHẨM PHÁP GIỚI'),
    (568, 411, 428, 'HỘI THỨ SÁU', 'PHẦN ĐẦU', 'IV. PHẨM PHÁP GIỚI & V. PHẨM NIỆM TRỤ'),
    (569, 429, 446, 'HỘI THỨ SÁU', 'PHẦN ĐẦU', 'VI. PHẨM PHÁP TÁNH'),
    (570, 447, 463, 'HỘI THỨ SÁU', 'PHẦN ĐẦU', 'VII. PHẨM BÌNH ĐẲNG & VIII. PHẨM HIỆN TƯỚNG'),
    (571, 464, 483, 'HỘI THỨ SÁU', 'PHẦN ĐẦU', 'IX. PHẨM VÔ SỞ ĐẮC & X. PHẨM CHỨNG KHUYẾN'),
    (572, 484, 503, 'HỘI THỨ SÁU', 'PHẦN ĐẦU', 'XI. PHẨM HIỂN ĐỨC & XII. PHẨM HIỆN HÓA & XIII. PHẨM ĐÀ-LA-NI & XIV. PHẨM KHUYÊN RĂN'),
    (573, 504, 526, 'HỘI THỨ SÁU', 'PHẦN ĐẦU', 'XIV. PHẨM KHUYÊN RĂN & XV. PHẨM NHỊ HẠNH & XVI. PHẨM TÁN THÁN & XVII. PHẨM PHÓ CHÚC'),
    (574, 527, 544, 'HỘI THỨ BẢY', '', 'PHẦN MẠN-THÙ-THẤT-LỢI'),
    (575, 545, 561, 'HỘI THỨ BẢY', '', 'PHẦN MẠN-THÙ-THẤT-LỢI'),
    (576, 562, 579, 'HỘI THỨ TÁM', '', 'PHẦN NA-GIÀ-THẤT-LỢI'),
    (577, 580, 599, 'HỘI THỨ CHÍN', '', 'PHẦN KIM CƯƠNG NĂNG ĐOẠN'),
    (578, 600, 616, 'HỘI THỨ MƯỜI', '', 'PHẦN LÝ THÚ BÁT-NHÃ'),
    (579, 617, 634, 'HỘI THỨ MƯỜI MỘT', '', 'PHẦN BỐ THÍ BA-LA-MẬT-ĐA'),
    (580, 635, 652, 'HỘI THỨ MƯỜI MỘT', '', 'PHẦN BỐ THÍ BA-LA-MẬT-ĐA'),
    (581, 653, 671, 'HỘI THỨ MƯỜI MỘT', '', 'PHẦN BỐ THÍ BA-LA-MẬT-ĐA'),
    (582, 672, 689, 'HỘI THỨ MƯỜI MỘT', '', 'PHẦN BỐ THÍ BA-LA-MẬT-ĐA'),
    (583, 690, 705, 'HỘI THỨ MƯỜI MỘT', '', 'PHẦN BỐ THÍ BA-LA-MẬT-ĐA'),
    (584, 706, 721, 'HỘI THỨ MƯỜI HAI', '', 'PHẦN TỊNH GIỚI BA-LA-MẬT-ĐA'),
    (585, 722, 736, 'HỘI THỨ MƯỜI HAI', '', 'PHẦN TỊNH GIỚI BA-LA-MẬT-ĐA'),
    (586, 737, 753, 'HỘI THỨ MƯỜI HAI', '', 'PHẦN TỊNH GIỚI BA-LA-MẬT-ĐA'),
    (587, 754, 769, 'HỘI THỨ MƯỜI HAI', '', 'PHẦN TỊNH GIỚI BA-LA-MẬT-ĐA'),
    (588, 770, 785, 'HỘI THỨ MƯỜI HAI', '', 'PHẦN TỊNH GIỚI BA-LA-MẬT-ĐA'),
    (589, 786, 802, 'HỘI THỨ MƯỜI BA', '', 'PHẦN AN NHẪN BA-LA-MẬT-ĐA'),
    (590, 803, 817, 'HỘI THỨ MƯỜI BỐN', '', 'PHẦN TINH TẤN BA-LA-MẬT-ĐA'),
    (591, 818, 832, 'HỘI THỨ MƯỜI LĂM', '', 'PHẦN TĨNH LỰ BA-LA-MẬT-ĐA'),
    (592, 833, 847, 'HỘI THỨ MƯỜI LĂM', '', 'PHẦN TĨNH LỰ BA-LA-MẬT-ĐA'),
    (593, 848, 864, 'HỘI THỨ MƯỜI SÁU', '', 'PHẦN BÁT-NHÃ BA-LA-MẬT-ĐA'),
    (594, 865, 881, 'HỘI THỨ MƯỜI SÁU', '', 'PHẦN BÁT-NHÃ BA-LA-MẬT-ĐA'),
    (595, 882, 900, 'HỘI THỨ MƯỜI SÁU', '', 'PHẦN BÁT-NHÃ BA-LA-MẬT-ĐA'),
    (596, 901, 921, 'HỘI THỨ MƯỜI SÁU', '', 'PHẦN BÁT-NHÃ BA-LA-MẬT-ĐA'),
    (597, 922, 938, 'HỘI THỨ MƯỜI SÁU', '', 'PHẦN BÁT-NHÃ BA-LA-MẬT-ĐA'),
    (598, 939, 958, 'HỘI THỨ MƯỜI SÁU', '', 'PHẦN BÁT-NHÃ BA-LA-MẬT-ĐA'),
    (599, 959, 981, 'HỘI THỨ MƯỜI SÁU', '', 'PHẦN BÁT-NHÃ BA-LA-MẬT-ĐA'),
    (600, 982, 998, 'HỘI THỨ MƯỜI SÁU', '', 'PHẦN BÁT-NHÃ BA-LA-MẬT-ĐA'),
]

out_dir = 'Tap_11'
os.makedirs(out_dir, exist_ok=True)

passed = 0
failed = 0

print(f'Starting processing Tập 11: {len(quyen_data)} Quyển (548 to 600)...')

for quyen_num, pdf_s, pdf_e, hoi_str, phan_str, pham_str in quyen_data:
    p_in_s = page_in_map[pdf_s]
    p_in_e = page_in_map[pdf_e]
    ok = process_quyen(
        reader=reader,
        tap_num=11,
        quyen_num=quyen_num,
        pdf_start=pdf_s,
        pdf_end=pdf_e,
        p_in_start=p_in_s,
        p_in_end=p_in_e,
        hoi_str=hoi_str,
        phan_str=phan_str,
        pham_str=pham_str,
        out_dir=out_dir,
        tap_range_str='TỪ QUYỂN 548 ĐẾN QUYỂN 600',
        page_in_map=page_in_map
    )
    if ok:
        passed += 1
    else:
        failed += 1

print(f'\n--- SUMMARY TẬP 11 ---')
print(f'Passed: {passed}/{len(quyen_data)}')
print(f'Failed: {failed}/{len(quyen_data)}')
