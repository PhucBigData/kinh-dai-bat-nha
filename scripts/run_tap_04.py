import sys
sys.path.insert(0, '.')
import pypdf
import os
import re
from scripts.batch_processor import process_quyen, validate_quality_gates

pdf_path = 'Kinh Bát Nhã/Kinh Đại Bát Nhã - Tập 04.PDF'
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
            if val > 10:
                exact_page_in[i] = val
                break

for i in range(total):
    if exact_page_in[i] is None:
        if i + 1 < total and exact_page_in[i+1] is not None:
            exact_page_in[i] = exact_page_in[i+1] - 1
        elif i > 0 and exact_page_in[i-1] is not None:
            exact_page_in[i] = exact_page_in[i-1] + 1

page_in_map = {p+1: exact_page_in[p] for p in range(total)}

quyen_data = [
    (169, 1, 17, 'XXXI. PHẨM TÙY HỶ HỒI HƯỚNG (02)'),
    (170, 18, 32, 'XXXI. PHẨM TÙY HỶ HỒI HƯỚNG (03)'),
    (171, 33, 47, 'XXXI. PHẨM TÙY HỶ HỒI HƯỚNG (04)'),
    (172, 48, 63, 'XXXI. PHẨM TÙY HỶ HỒI HƯỚNG (05) & XXXII. PHẨM KHEN NGỢI BÁT-NHÃ (01)'),
    (173, 64, 79, 'XXXII. PHẨM KHEN NGỢI BÁT-NHÃ (02)'),
    (174, 80, 96, 'XXXII. PHẨM KHEN NGỢI BÁT-NHÃ (03)'),
    (175, 97, 114, 'XXXII. PHẨM KHEN NGỢI BÁT-NHÃ (04)'),
    (176, 115, 131, 'XXXII. PHẨM KHEN NGỢI BÁT-NHÃ (05)'),
    (177, 132, 150, 'XXXII. PHẨM KHEN NGỢI BÁT-NHÃ (06)'),
    (178, 151, 169, 'XXXII. PHẨM KHEN NGỢI BÁT-NHÃ (07)'),
    (179, 170, 185, 'XXXII. PHẨM KHEN NGỢI BÁT-NHÃ (08)'),
    (180, 186, 199, 'XXXII. PHẨM KHEN NGỢI BÁT-NHÃ (09)'),
    (181, 200, 216, 'XXXII. PHẨM KHEN NGỢI BÁT-NHÃ (10) & XXXIII. PHẨM HỦY BÁNG BÁT-NHÃ'),
    (182, 217, 230, 'XXXIV. PHẨM KHÓ TIN HIỂU (01)'),
    (183, 231, 245, 'XXXIV. PHẨM KHÓ TIN HIỂU (02)'),
    (184, 246, 259, 'XXXIV. PHẨM KHÓ TIN HIỂU (03)'),
    (185, 260, 274, 'XXXIV. PHẨM KHÓ TIN HIỂU (04)'),
    (186, 275, 289, 'XXXIV. PHẨM KHÓ TIN HIỂU (05)'),
    (187, 290, 305, 'XXXIV. PHẨM KHÓ TIN HIỂU (06)'),
    (188, 306, 321, 'XXXIV. PHẨM KHÓ TIN HIỂU (07)'),
    (189, 322, 333, 'XXXIV. PHẨM KHÓ TIN HIỂU (08)'),
    (190, 334, 349, 'XXXIV. PHẨM KHÓ TIN HIỂU (09)'),
    (191, 350, 365, 'XXXIV. PHẨM KHÓ TIN HIỂU (10)'),
    (192, 366, 380, 'XXXIV. PHẨM KHÓ TIN HIỂU (11)'),
    (193, 381, 395, 'XXXIV. PHẨM KHÓ TIN HIỂU (12)'),
    (194, 396, 411, 'XXXIV. PHẨM KHÓ TIN HIỂU (13)'),
    (195, 412, 428, 'XXXIV. PHẨM KHÓ TIN HIỂU (14)'),
    (196, 429, 445, 'XXXIV. PHẨM KHÓ TIN HIỂU (15)'),
    (197, 446, 460, 'XXXIV. PHẨM KHÓ TIN HIỂU (16)'),
    (198, 461, 478, 'XXXIV. PHẨM KHÓ TIN HIỂU (17)'),
    (199, 479, 495, 'XXXIV. PHẨM KHÓ TIN HIỂU (18)'),
    (200, 496, 510, 'XXXIV. PHẨM KHÓ TIN HIỂU (19)'),
    (201, 511, 526, 'XXXIV. PHẨM KHÓ TIN HIỂU (20)'),
    (202, 527, 541, 'XXXIV. PHẨM KHÓ TIN HIỂU (21)'),
    (203, 542, 557, 'XXXIV. PHẨM KHÓ TIN HIỂU (22)'),
    (204, 558, 572, 'XXXIV. PHẨM KHÓ TIN HIỂU (23)'),
    (205, 573, 588, 'XXXIV. PHẨM KHÓ TIN HIỂU (24)'),
    (206, 589, 604, 'XXXIV. PHẨM KHÓ TIN HIỂU (25)'),
    (207, 605, 620, 'XXXIV. PHẨM KHÓ TIN HIỂU (26)'),
    (208, 621, 637, 'XXXIV. PHẨM KHÓ TIN HIỂU (27)'),
    (209, 638, 654, 'XXXIV. PHẨM KHÓ TIN HIỂU (28)'),
    (210, 655, 672, 'XXXIV. PHẨM KHÓ TIN HIỂU (29)'),
    (211, 673, 690, 'XXXIV. PHẨM KHÓ TIN HIỂU (30)'),
    (212, 691, 709, 'XXXIV. PHẨM KHÓ TIN HIỂU (31)'),
    (213, 710, 725, 'XXXIV. PHẨM KHÓ TIN HIỂU (32)'),
    (214, 726, 742, 'XXXIV. PHẨM KHÓ TIN HIỂU (33)'),
    (215, 743, 758, 'XXXIV. PHẨM KHÓ TIN HIỂU (34)'),
    (216, 759, 774, 'XXXIV. PHẨM KHÓ TIN HIỂU (35)'),
    (217, 775, 791, 'XXXIV. PHẨM KHÓ TIN HIỂU (36)'),
    (218, 792, 808, 'XXXIV. PHẨM KHÓ TIN HIỂU (37)'),
    (219, 809, 826, 'XXXIV. PHẨM KHÓ TIN HIỂU (38)'),
    (220, 827, 841, 'XXXIV. PHẨM KHÓ TIN HIỂU (39)'),
]

out_dir = 'Tap_04'
os.makedirs(out_dir, exist_ok=True)

passed = 0
failed = 0

print(f'Starting processing Tập 04: {len(quyen_data)} Quyển (169 to 220)...')

for quyen_num, pdf_s, pdf_e, pham_str in quyen_data:
    p_in_s = page_in_map[pdf_s]
    p_in_e = page_in_map[pdf_e]
    ok = process_quyen(
        reader=reader,
        tap_num=4,
        quyen_num=quyen_num,
        pdf_start=pdf_s,
        pdf_end=pdf_e,
        p_in_start=p_in_s,
        p_in_end=p_in_e,
        hoi_str='HỘI THỨ NHẤT: HỘI ĐẦU',
        phan_str='PHẦN ĐẦU',
        pham_str=pham_str,
        out_dir=out_dir,
        tap_range_str='TỪ QUYỂN 169 ĐẾN QUYỂN 220',
        page_in_map=page_in_map
    )
    if ok:
        passed += 1
    else:
        failed += 1

print(f'\n--- SUMMARY TẬP 04 ---')
print(f'Passed: {passed}/{len(quyen_data)}')
print(f'Failed: {failed}/{len(quyen_data)}')
