import sys
sys.path.insert(0, '.')
import pypdf
import os
import re
from scripts.batch_processor import process_quyen, validate_quality_gates

pdf_path = 'Kinh Bát Nhã/Kinh Đại Bát Nhã - Tập 03.PDF'
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
    (104, 1, 15, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (02)'),
    (105, 16, 30, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (03)'),
    (106, 31, 48, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (04)'),
    (107, 49, 68, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (05)'),
    (108, 69, 88, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (06)'),
    (109, 89, 114, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (07)'),
    (110, 115, 135, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (08)'),
    (111, 136, 155, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (09)'),
    (112, 156, 174, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (10)'),
    (113, 175, 194, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (11)'),
    (114, 195, 212, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (12)'),
    (115, 213, 231, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (13)'),
    (116, 232, 249, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (14)'),
    (117, 250, 269, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (15)'),
    (118, 270, 292, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (16)'),
    (119, 293, 312, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (17)'),
    (120, 313, 331, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (18)'),
    (121, 332, 352, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (19)'),
    (122, 353, 372, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (20)'),
    (123, 373, 393, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (21)'),
    (124, 394, 414, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (22)'),
    (125, 415, 432, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (23)'),
    (126, 433, 447, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (24)'),
    (127, 448, 463, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (25)'),
    (128, 464, 479, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (26)'),
    (129, 480, 493, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (27)'),
    (130, 494, 508, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (28)'),
    (131, 509, 522, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (29)'),
    (132, 523, 537, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (30)'),
    (133, 538, 550, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (31)'),
    (134, 551, 564, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (32)'),
    (135, 565, 578, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (33)'),
    (136, 579, 593, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (34)'),
    (137, 594, 607, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (35)'),
    (138, 608, 622, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (36)'),
    (139, 623, 636, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (37)'),
    (140, 637, 650, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (38)'),
    (141, 651, 664, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (39)'),
    (142, 665, 679, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (40)'),
    (143, 680, 694, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (41)'),
    (144, 695, 708, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (42)'),
    (145, 709, 723, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (43)'),
    (146, 724, 737, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (44)'),
    (147, 738, 753, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (45)'),
    (148, 754, 769, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (46)'),
    (149, 770, 783, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (47)'),
    (150, 784, 799, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (48)'),
    (151, 800, 815, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (49)'),
    (152, 816, 831, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (50)'),
    (153, 832, 847, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (51)'),
    (154, 848, 863, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (52)'),
    (155, 864, 877, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (53)'),
    (156, 878, 892, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (54)'),
    (157, 893, 908, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (55)'),
    (158, 909, 923, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (56)'),
    (159, 924, 939, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (57)'),
    (160, 940, 953, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (58)'),
    (161, 954, 971, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (59)'),
    (162, 972, 986, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (60)'),
    (163, 987, 1002, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (61)'),
    (164, 1003, 1018, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (62)'),
    (165, 1019, 1034, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (63)'),
    (166, 1035, 1051, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (64)'),
    (167, 1052, 1066, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC (65)'),
    (168, 1067, 1081, 'XXX. PHẨM SO SÁNH CÔNG ĐỨC & XXXI. PHẨM TÙY HỶ HỒI HƯỚNG (01)'),
]

out_dir = 'Tap_03'
os.makedirs(out_dir, exist_ok=True)

passed = 0
failed = 0

print(f'Starting processing Tập 03: {len(quyen_data)} Quyển (104 to 168)...')

for quyen_num, pdf_s, pdf_e, pham_str in quyen_data:
    p_in_s = page_in_map[pdf_s]
    p_in_e = page_in_map[pdf_e]
    ok = process_quyen(
        reader=reader,
        tap_num=3,
        quyen_num=quyen_num,
        pdf_start=pdf_s,
        pdf_end=pdf_e,
        p_in_start=p_in_s,
        p_in_end=p_in_e,
        hoi_str='HỘI THỨ NHẤT: HỘI ĐẦU',
        phan_str='PHẦN ĐẦU',
        pham_str=pham_str,
        out_dir=out_dir,
        tap_range_str='TỪ QUYỂN 104 ĐẾN QUYỂN 168',
        page_in_map=page_in_map
    )
    if ok:
        passed += 1
    else:
        failed += 1

print(f'\n--- SUMMARY TẬP 03 ---')
print(f'Passed: {passed}/{len(quyen_data)}')
print(f'Failed: {failed}/{len(quyen_data)}')
