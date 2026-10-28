import sys
sys.path.insert(0, '.')
import pypdf
import os
from scripts.batch_processor import process_quyen, validate_quality_gates

pdf_path = 'Kinh Bát Nhã/Kinh Đại Bát Nhã - Tập 02.PDF'
reader = pypdf.PdfReader(pdf_path)

quyen_data = [
    (52, 1, 21, 20, 40, 'XV. PHẨM BIỆN ĐẠI-THỪA (02)'),
    (53, 22, 39, 42, 59, 'XV. PHẨM BIỆN ĐẠI-THỪA (03)'),
    (54, 40, 57, 61, 78, 'XV. PHẨM BIỆN ĐẠI-THỪA (04)'),
    (55, 58, 76, 80, 98, 'XV. PHẨM BIỆN ĐẠI-THỪA (05)'),
    (56, 77, 96, 100, 119, 'XV. PHẨM BIỆN ĐẠI-THỪA (06) & XVI. PHẨM TÁN ĐẠI-THỪA (01)'),
    (57, 97, 113, 121, 137, 'XVI. PHẨM TÁN ĐẠI-THỪA (02)'),
    (58, 114, 128, 139, 153, 'XVI. PHẨM TÁN ĐẠI-THỪA (03)'),
    (59, 129, 146, 155, 172, 'XVI. PHẨM TÁN ĐẠI-THỪA (04)'),
    (60, 147, 165, 174, 192, 'XVI. PHẨM TÁN ĐẠI-THỪA (05)'),
    (61, 166, 183, 194, 210, 'XVI. PHẨM TÁN ĐẠI-THỪA (06) & XVII. PHẨM TÙY THUẬN & XVIII. PHẨM VÔ SỞ ĐẮC (01)'),
    (62, 184, 198, 212, 226, 'XVIII. PHẨM VÔ SỞ ĐẮC (02)'),
    (63, 199, 215, 228, 244, 'XVIII. PHẨM VÔ SỞ ĐẮC (03)'),
    (64, 216, 231, 246, 261, 'XVIII. PHẨM VÔ SỞ ĐẮC (04)'),
    (65, 232, 251, 263, 282, 'XVIII. PHẨM VÔ SỞ ĐẮC (05)'),
    (66, 252, 268, 284, 300, 'XVIII. PHẨM VÔ SỞ ĐẮC (06)'),
    (67, 269, 286, 302, 319, 'XVIII. PHẨM VÔ SỞ ĐẮC (07)'),
    (68, 287, 305, 321, 339, 'XVIII. PHẨM VÔ SỞ ĐẮC (08)'),
    (69, 306, 324, 341, 359, 'XVIII. PHẨM VÔ SỞ ĐẮC (09)'),
    (70, 325, 342, 361, 378, 'XVIII. PHẨM VÔ SỞ ĐẮC (10) & XIX. PHẨM QUÁN HẠNH (01)'),
    (71, 343, 361, 380, 398, 'XIX. PHẨM QUÁN HẠNH (02)'),
    (72, 362, 378, 400, 416, 'XIX. PHẨM QUÁN HẠNH (03)'),
    (73, 379, 396, 418, 435, 'XIX. PHẨM QUÁN HẠNH (04)'),
    (74, 397, 414, 437, 454, 'XIX. PHẨM QUÁN HẠNH (05) & XX. PHẨM VÔ SANH (01)'),
    (75, 415, 431, 456, 472, 'XX. PHẨM VÔ SANH (02) & XXI. PHẨM TỊNH ĐẠO (01)'),
    (76, 432, 443, 474, 485, 'XXI. PHẨM TỊNH ĐẠO (02)'),
    (77, 444, 457, 487, 500, 'XXII. PHẨM THIÊN ĐẾ (01)'),
    (78, 458, 473, 502, 517, 'XXII. PHẨM THIÊN ĐẾ (02)'),
    (79, 474, 488, 519, 533, 'XXII. PHẨM THIÊN ĐẾ (03)'),
    (80, 489, 503, 535, 549, 'XXII. PHẨM THIÊN ĐẾ (04)'),
    (81, 504, 522, 551, 569, 'XXII. PHẨM THIÊN ĐẾ (05) & XXIII. PHẨM CHƯ THIÊN TỬ (01)'),
    (82, 523, 537, 571, 585, 'XXIII. PHẨM CHƯ THIÊN TỬ (02) & XXIV. PHẨM THỌ GIÁO (01)'),
    (83, 538, 552, 587, 601, 'XXIV. PHẨM THỌ GIÁO (02)'),
    (84, 553, 569, 603, 619, 'XXIV. PHẨM THỌ GIÁO (03) & XXV. PHẨM TÁN HOA'),
    (85, 570, 584, 621, 635, 'XXVI. PHẨM HỌC BÁT-NHÃ (01)'),
    (86, 585, 599, 637, 651, 'XXVI. PHẨM HỌC BÁT-NHÃ (02)'),
    (87, 600, 614, 653, 667, 'XXVI. PHẨM HỌC BÁT-NHÃ (03)'),
    (88, 615, 630, 669, 684, 'XXVI. PHẨM HỌC BÁT-NHÃ (04)'),
    (89, 631, 647, 686, 702, 'XXVI. PHẨM HỌC BÁT-NHÃ (05) & XXVII. PHẨM CẦU BÁT-NHÃ (01)'),
    (90, 648, 664, 704, 720, 'XXVII. PHẨM CẦU BÁT-NHÃ (02)'),
    (91, 665, 683, 722, 740, 'XXVII. PHẨM CẦU BÁT-NHÃ (03)'),
    (92, 684, 702, 742, 760, 'XXVII. PHẨM CẦU BÁT-NHÃ (04)'),
    (93, 703, 721, 762, 780, 'XXVII. PHẨM CẦU BÁT-NHÃ (05)'),
    (94, 722, 735, 782, 795, 'XXVII. PHẨM CẦU BÁT-NHÃ (06)'),
    (95, 736, 749, 797, 810, 'XXVII. PHẨM CẦU BÁT-NHÃ (07)'),
    (96, 750, 764, 812, 826, 'XXVII. PHẨM CẦU BÁT-NHÃ (08)'),
    (97, 765, 779, 828, 842, 'XXVII. PHẨM CẦU BÁT-NHÃ (09)'),
    (98, 780, 794, 844, 858, 'XXVII. PHẨM CẦU BÁT-NHÃ (10) & XXVIII. PHẨM THÁN CHÚNG CÔNG ĐỨC (01)'),
    (99, 795, 813, 860, 878, 'XXVIII. PHẨM THÁN CHÚNG CÔNG ĐỨC (02) & XXIX. PHẨM NHIẾP THỌ (01)'),
    (100, 814, 830, 880, 896, 'XXIX. PHẨM NHIẾP THỌ (02)'),
    (101, 831, 847, 898, 914, 'XXIX. PHẨM NHIẾP THỌ (03)'),
    (102, 848, 863, 916, 931, 'XXIX. PHẨM NHIẾP THỌ (04)'),
    (103, 864, 879, 933, 948, 'XXIX. PHẨM NHIẾP THỌ (05) & XXX. PHẨM SO SÁNH CÔNG ĐỨC'),
]

out_dir = 'Tap_02'
os.makedirs(out_dir, exist_ok=True)

results = {}
for q, s, e, p_s, p_e, pham in quyen_data:
    ok = process_quyen(
        reader=reader,
        tap_num=2,
        quyen_num=q,
        pdf_start=s,
        pdf_end=e,
        p_in_start=p_s,
        p_in_end=p_e,
        hoi_str='HỘI THỨ NHẤT: HỘI ĐẦU',
        phan_str='PHẦN ĐẦU',
        pham_str=pham,
        out_dir=out_dir,
        tap_range_str='TỪ QUYỂN 52 ĐẾN QUYỂN 103'
    )
    results[q] = ok

print('=== TAP 02 EXECUTION SUMMARY ===')
passed_cnt = sum(results.values())
total_cnt = len(quyen_data)
print(f'Total: {total_cnt} Quyển | Passed: {passed_cnt} / {total_cnt}')
if passed_cnt == total_cnt:
    print('ALL 52 QUYỂN OF TẬP 02 PASSED 100% QUALITY GATES!')
