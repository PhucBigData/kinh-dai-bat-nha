import pypdf
import re

ranges = [
    (548, 1, 21), (549, 22, 41), (550, 42, 65), (551, 66, 85), (552, 86, 105),
    (553, 106, 125), (554, 126, 148), (555, 149, 170), (556, 171, 194), (557, 195, 213),
    (558, 214, 234), (559, 235, 257), (560, 258, 277), (561, 278, 298), (562, 299, 319),
    (563, 320, 338), (564, 339, 358), (565, 359, 376), (566, 377, 392), (567, 393, 410),
    (568, 411, 428), (569, 429, 446), (570, 447, 463), (571, 464, 483), (572, 484, 503),
    (573, 504, 526), (574, 527, 544), (575, 545, 561), (576, 562, 579), (577, 580, 599),
    (578, 600, 616), (579, 617, 634), (580, 635, 652), (581, 653, 671), (582, 672, 689),
    (583, 690, 705), (584, 706, 721), (585, 722, 736), (586, 737, 753), (587, 754, 769),
    (588, 770, 785), (589, 786, 802), (590, 803, 817), (591, 818, 832), (592, 833, 847),
    (593, 848, 864), (594, 865, 881), (595, 882, 900), (596, 901, 921), (597, 922, 938),
    (598, 939, 958), (599, 959, 981), (600, 982, 998)
]

all_phams = [
    # Hoi 4: p1-170
    (1, 'XIV. PHẨM THÍ DỤ'),
    (8, 'XV. PHẨM TRỜI KHEN NGỢI'),
    (17, 'XVI. PHẨM CHƠN NHƯ'),
    (28, 'XVII. PHẨM TƯỚNG BẤT THỐI'),
    (38, 'XVIII. PHẨM TƯỚNG KHÔNG'),
    (46, 'XIX. PHẨM CÔNG ĐỨC SÂU XA'),
    (57, 'XX. PHẨM CĂNG-GIÀ THIÊN'),
    (60, 'XXI. PHẨM BIẾT VIỆC MA'),
    (78, 'XXII. PHẨM THIỆN HỮU'),
    (91, 'XXIII. PHẨM THIÊN CHỦ'),
    (95, 'XXIV. PHẨM VÔ TẠP VÔ DỊ'),
    (102, 'XXV. PHẨM TẤN TỐC'),
    (111, 'XXVI. PHẨM HUYỄN DỤ'),
    (119, 'XXVII. PHẨM KIÊN CỐ'),
    (132, 'XXVIII. PHẨM TÁN HOA'),
    (149, 'XXIX. PHẨM TÙY THUẬN'),

    # Hoi 5: p171-376
    (171, 'I. PHẨM THIỆN HIỆN'),
    (188, 'II. PHẨM THIÊN ĐẾ'),
    (195, 'III. PHẨM BẢO THÁP'),
    (204, 'IV. PHẨM THẦN CHÚ'),
    (214, 'V. PHẨM XÁ-LỢI'),
    (219, 'VI. PHẨM KINH ĐIỂN'),
    (225, 'VII. PHẨM HỒI HƯỚNG'),
    (235, 'VIII. PHẨM ĐỊA NGỤC'),
    (243, 'IX. PHẨM THANH TỊNH'),
    (253, 'X. PHẨM BẤT TƯ NGHÌ'),
    (265, 'XI. PHẨM MA SỰ'),
    (272, 'XII. PHẨM CHƠN NHƯ'),
    (278, 'XIII. PHẨM THẬM THÂM TƯỚNG'),
    (287, 'XIV. PHẨM THUYỀN ĐẲNG DỤ'),
    (289, 'XV. PHẨM NHƯ LAI'),
    (303, 'XVI. PHẨM BẤT THỐI'),
    (311, 'XVII. PHẨM THAM HÀNH'),
    (326, 'XVIII. PHẨM TỶ MUỘI'),
    (333, 'XIX. PHẨM MỘNG HÀNH'),
    (339, 'XX. PHẨM THẮNG Ý LẠC'),
    (348, 'XXI. PHẨM TU HỌC'),
    (353, 'XXII. PHẨM TRỒNG CĂN LÀNH'),
    (364, 'XXIII. PHẨM PHÓ CHÚC'),
    (371, 'XXIV. PHẨM KIẾN BẤT ĐỘNG PHẬT'),

    # Hoi 6: p377-526
    (377, 'I. PHẨM DUYÊN KHỞI'),
    (381, 'II. PHẨM THÔNG ĐẠT'),
    (393, 'III. PHẨM HIỂN TƯỚNG'),
    (404, 'IV. PHẨM PHÁP GIỚI'),
    (418, 'V. PHẨM NIỆM TRỤ'),
    (429, 'VI. PHẨM PHÁP TÁNH'),
    (447, 'VII. PHẨM BÌNH ĐẲNG'),
    (454, 'VIII. PHẨM HIỆN TƯỚNG'),
    (464, 'IX. PHẨM VÔ SỞ ĐẮC'),
    (476, 'X. PHẨM CHỨNG KHUYẾN'),
    (484, 'XI. PHẨM HIỂN ĐỨC'),
    (491, 'XII. PHẨM HIỆN HÓA'),
    (496, 'XIII. PHẨM ĐÀ-LA-NI'),
    (501, 'XIV. PHẨM KHUYÊN RĂN'),
    (508, 'XV. PHẨM NHỊ HẠNH'),
    (517, 'XVI. PHẨM TÁN THÁN'),
    (523, 'XVII. PHẨM PHÓ CHÚC'),

    # Hoi 7 to 16
    (527, 'PHẦN MẠN-THÙ-THẤT-LỢI'),
    (562, 'PHẦN NA-GIÀ-THẤT-LỢI'),
    (580, 'PHẦN KIM CƯƠNG NĂNG ĐOẠN'),
    (600, 'PHẦN LÝ THÚ BÁT-NHÃ'),
    (617, 'PHẦN BỐ THÍ BA-LA-MẬT-ĐA'),
    (706, 'PHẦN TỊNH GIỚI BA-LA-MẬT-ĐA'),
    (786, 'PHẦN AN NHẪN BA-LA-MẬT-ĐA'),
    (803, 'PHẦN TINH TẤN BA-LA-MẬT-ĐA'),
    (818, 'PHẦN TĨNH LỰ BA-LA-MẬT-ĐA'),
    (848, 'PHẦN BÁT-NHÃ BA-LA-MẬT-ĐA')
]

# Section limits:
# Hoi 4: [1, 170]
# Hoi 5: [171, 376]
# Hoi 6: [377, 526]
# Hoi 7: [527, 561]
# Hoi 8: [562, 579]
# Hoi 9: [580, 599]
# Hoi 10: [600, 616]
# Hoi 11: [617, 705]
# Hoi 12: [706, 785]
# Hoi 13: [786, 802]
# Hoi 14: [803, 817]
# Hoi 15: [818, 847]
# Hoi 16: [848, 998]

for q, s, e in ranges:
    if q <= 555:
        hoi_str = 'HỘI THỨ TƯ'
        sec_s, sec_e = 1, 170
    elif q <= 565:
        hoi_str = 'HỘI THỨ NĂM'
        sec_s, sec_e = 171, 376
    elif q <= 573:
        hoi_str = 'HỘI THỨ SÁU'
        sec_s, sec_e = 377, 526
    elif q <= 575:
        hoi_str = 'HỘI THỨ BẢY'
        sec_s, sec_e = 527, 561
    elif q <= 576:
        hoi_str = 'HỘI THỨ TÁM'
        sec_s, sec_e = 562, 579
    elif q <= 577:
        hoi_str = 'HỘI THỨ CHÍN'
        sec_s, sec_e = 580, 599
    elif q <= 578:
        hoi_str = 'HỘI THỨ MƯỜI'
        sec_s, sec_e = 600, 616
    elif q <= 583:
        hoi_str = 'HỘI THỨ MƯỜI MỘT'
        sec_s, sec_e = 617, 705
    elif q <= 588:
        hoi_str = 'HỘI THỨ MƯỜI HAI'
        sec_s, sec_e = 706, 785
    elif q <= 589:
        hoi_str = 'HỘI THỨ MƯỜI BA'
        sec_s, sec_e = 786, 802
    elif q <= 590:
        hoi_str = 'HỘI THỨ MƯỜI BỐN'
        sec_s, sec_e = 803, 817
    elif q <= 592:
        hoi_str = 'HỘI THỨ MƯỜI LĂM'
        sec_s, sec_e = 818, 847
    else:
        hoi_str = 'HỘI THỨ MƯỜI SÁU'
        sec_s, sec_e = 848, 998

    active_before = [name for p_start, name in all_phams if sec_s <= p_start <= s]
    active_at_s = active_before[-1] if active_before else 'PHẨM KHÔNG XÁC ĐỊNH'
    in_range = [name for p_start, name in all_phams if s < p_start <= e and p_start <= sec_e]
    combined = [active_at_s] + in_range
    joined_name = ' & '.join(combined)
    print(f"    ({q}, {s}, {e}, '{hoi_str}', '{joined_name}'),")
