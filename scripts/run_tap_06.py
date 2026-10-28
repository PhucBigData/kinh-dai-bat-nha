import sys
sys.path.insert(0, '.')
import pypdf
import os
import re
from scripts.batch_processor import process_quyen, validate_quality_gates

pdf_path = 'Kinh Bát Nhã/Kinh Đại Bát Nhã - Tập 06.PDF'
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

ends = {
    285: 18, 286: 38, 287: 60, 288: 76, 289: 89, 290: 102, 291: 118,
    292: 135, 293: 152, 294: 170, 295: 188, 296: 210, 297: 226, 298: 243,
    299: 257, 300: 272, 301: 287, 302: 303, 303: 321, 304: 336, 305: 351,
    306: 368, 307: 387, 308: 406, 309: 423, 310: 443, 311: 460, 312: 477,
    313: 494, 314: 510, 315: 528, 316: 549, 317: 566, 318: 585, 319: 603,
    320: 620, 321: 639, 322: 658, 323: 678, 324: 698, 325: 716, 326: 733,
    327: 751, 328: 771, 329: 788, 330: 806, 331: 824, 332: 840, 333: 857,
    334: 874, 335: 898, 336: 919
}

quyen_data = [
    (285, 1, 18, 'XXXV. PHẨM KHEN NGỢI THANH TỊNH (01)'),
    (286, 19, 38, 'XXXV. PHẨM KHEN NGỢI THANH TỊNH (02)'),
    (287, 39, 60, 'XXXV. PHẨM KHEN NGỢI THANH TỊNH (03) & XXXVI. PHẨM TRƯỚC VÀ KHÔNG TRƯỚC TƯỚNG (01)'),
    (288, 61, 76, 'XXXVI. PHẨM TRƯỚC VÀ KHÔNG TRƯỚC TƯỚNG (02)'),
    (289, 77, 89, 'XXXVI. PHẨM TRƯỚC VÀ KHÔNG TRƯỚC TƯỚNG (03)'),
    (290, 90, 102, 'XXXVI. PHẨM TRƯỚC VÀ KHÔNG TRƯỚC TƯỚNG (04)'),
    (291, 103, 118, 'XXXVI. PHẨM TRƯỚC VÀ KHÔNG TRƯỚC TƯỚNG (05)'),
    (292, 119, 135, 'XXXVI. PHẨM TRƯỚC VÀ KHÔNG TRƯỚC TƯỚNG (06) & XXXVII. PHẨM NÓI TƯỚNG BÁT-NHÃ (01)'),
    (293, 136, 152, 'XXXVII. PHẨM NÓI TƯỚNG BÁT-NHÃ (02)'),
    (294, 153, 170, 'XXXVII. PHẨM NÓI TƯỚNG BÁT-NHÃ (03)'),
    (295, 171, 188, 'XXXVII. PHẨM NÓI TƯỚNG BÁT-NHÃ (04)'),
    (296, 189, 210, 'XXXVII. PHẨM NÓI TƯỚNG BÁT-NHÃ (05) & XXXVIII. PHẨM BA-LA-MẬT-ĐA (01)'),
    (297, 211, 226, 'XXXVIII. PHẨM BA-LA-MẬT-ĐA (02) & XXXIX. PHẨM KHÓ NGHE CÔNG ĐỨC (01)'),
    (298, 227, 243, 'XXXIX. PHẨM KHÓ NGHE CÔNG ĐỨC (02)'),
    (299, 244, 257, 'XXXIX. PHẨM KHÓ NGHE CÔNG ĐỨC (03)'),
    (300, 258, 272, 'XXXIX. PHẨM KHÓ NGHE CÔNG ĐỨC (04)'),
    (301, 273, 287, 'XXXIX. PHẨM KHÓ NGHE CÔNG ĐỨC (05)'),
    (302, 288, 303, 'XXXIX. PHẨM KHÓ NGHE CÔNG ĐỨC (06)'),
    (303, 304, 321, 'XXXX. PHẨM MA SỰ (01)'),
    (304, 322, 336, 'XXXX. PHẨM MA SỰ (02)'),
    (305, 337, 351, 'XXXXI. PHẨM PHẬT MẪU (01)'),
    (306, 352, 368, 'XXXXI. PHẨM PHẬT MẪU (02)'),
    (307, 369, 387, 'XXXXI. PHẨM PHẬT MẪU (03)'),
    (308, 388, 406, 'XXXXI. PHẨM PHẬT MẪU (04) & XXXXII. PHẨM CHẲNG NGHĨ BÀN (01)'),
    (309, 407, 423, 'XXXXII. PHẨM CHẲNG NGHĨ BÀN (02)'),
    (310, 424, 443, 'XXXXII. PHẨM CHẲNG NGHĨ BÀN (03) & XXXXIII. PHẨM BIỆN SỰ (01)'),
    (311, 444, 460, 'XXXXIII. PHẨM BIỆN SỰ (02) & XXXXIV. PHẨM CHÚNG DỤ (01)'),
    (312, 461, 477, 'XXXXIV. PHẨM CHÚNG DỤ (02)'),
    (313, 478, 494, 'XXXXIV. PHẨM CHÚNG DỤ (03) & XXXXV. PHẨM CHƠN THIỆN HỮU (01)'),
    (314, 495, 510, 'XXXXV. PHẨM CHƠN THIỆN HỮU (02)'),
    (315, 511, 528, 'XXXXV. PHẨM CHƠN THIỆN HỮU (03)'),
    (316, 529, 549, 'XXXXV. PHẨM CHƠN THIỆN HỮU (04) & XXXXVI. PHẨM TRÍ HƯỚNG ĐẾN (01)'),
    (317, 550, 566, 'XXXXVI. PHẨM TRÍ HƯỚNG ĐẾN (02)'),
    (318, 567, 585, 'XXXXVI. PHẨM TRÍ HƯỚNG ĐẾN (03) & XXXXVII. PHẨM CHƠN NHƯ (01)'),
    (319, 586, 603, 'XXXXVII. PHẨM CHƠN NHƯ (02)'),
    (320, 604, 620, 'XXXXVII. PHẨM CHƠN NHƯ (03)'),
    (321, 621, 639, 'XXXXVII. PHẨM CHƠN NHƯ (04)'),
    (322, 640, 658, 'XXXXVII. PHẨM CHƠN NHƯ (05)'),
    (323, 659, 678, 'XXXXVII. PHẨM CHƠN NHƯ (06)'),
    (324, 679, 698, 'XXXXVII. PHẨM CHƠN NHƯ (07) & XXXXVIII. PHẨM BỒ-TÁT AN TRỤ (01)'),
    (325, 699, 716, 'XXXXVIII. PHẨM BỒ-TÁT AN TRỤ (02) & XXXXIX. PHẨM BẤT THỐI CHUYỂN (01)'),
    (326, 717, 733, 'XXXXIX. PHẨM BẤT THỐI CHUYỂN (02)'),
    (327, 734, 751, 'XXXXIX. PHẨM BẤT THỐI CHUYỂN (03)'),
    (328, 752, 771, 'XXXXX. PHẨM PHƯƠNG TIỆN THIỆN XẢO (01)'),
    (329, 772, 788, 'XXXXX. PHẨM PHƯƠNG TIỆN THIỆN XẢO (02)'),
    (330, 789, 806, 'XXXXX. PHẨM PHƯƠNG TIỆN THIỆN XẢO (03) & XXXXXI. PHẨM HẠNH NGUYỆN (01)'),
    (331, 807, 824, 'XXXXXI. PHẨM HẠNH NGUYỆN (02) & XXXXXII. PHẨM CĂNG-GIÀ-THIÊN & XXXXXIII. PHẨM KHÉO HỌC (01)'),
    (332, 825, 840, 'XXXXXIII. PHẨM KHÉO HỌC (02)'),
    (333, 841, 857, 'XXXXXIII. PHẨM KHÉO HỌC (03)'),
    (334, 858, 874, 'XXXXXIII. PHẨM KHÉO HỌC (04)'),
    (335, 875, 898, 'XXXXXIII. PHẨM KHÉO HỌC (05) & XXXXXIV. PHẨM ĐOẠN PHÂN BIỆT (01)'),
    (336, 899, 919, 'XXXXXIV. PHẨM ĐOẠN PHÂN BIỆT (02)'),
]

out_dir = 'Tap_06'
os.makedirs(out_dir, exist_ok=True)

passed = 0
failed = 0

print(f'Starting processing Tập 06: {len(quyen_data)} Quyển (285 to 336)...')

for quyen_num, pdf_s, pdf_e, pham_str in quyen_data:
    p_in_s = page_in_map[pdf_s]
    p_in_e = page_in_map[pdf_e]
    ok = process_quyen(
        reader=reader,
        tap_num=6,
        quyen_num=quyen_num,
        pdf_start=pdf_s,
        pdf_end=pdf_e,
        p_in_start=p_in_s,
        p_in_end=p_in_e,
        hoi_str='HỘI THỨ NHẤT: HỘI ĐẦU',
        phan_str='PHẦN ĐẦU',
        pham_str=pham_str,
        out_dir=out_dir,
        tap_range_str='TỪ QUYỂN 285 ĐẾN QUYỂN 336',
        page_in_map=page_in_map
    )
    if ok:
        passed += 1
    else:
        failed += 1

print(f'\n--- SUMMARY TẬP 06 ---')
print(f'Passed: {passed}/{len(quyen_data)}')
print(f'Failed: {failed}/{len(quyen_data)}')
