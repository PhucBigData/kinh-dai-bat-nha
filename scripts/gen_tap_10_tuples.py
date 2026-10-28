import pypdf
import re

ranges = [
    (499, 5, 21), (500, 22, 39), (501, 40, 56), (502, 57, 75), (503, 76, 91),
    (504, 92, 110), (505, 111, 129), (506, 130, 150), (507, 151, 171), (508, 172, 189),
    (509, 190, 212), (510, 213, 230), (511, 231, 249), (512, 250, 267), (513, 268, 287),
    (514, 288, 307), (515, 308, 327), (516, 328, 348), (517, 349, 368), (518, 369, 385),
    (519, 386, 411), (520, 412, 430), (521, 431, 449), (522, 450, 467), (523, 468, 484),
    (524, 485, 502), (525, 503, 526), (526, 527, 546), (527, 547, 565), (528, 566, 583),
    (529, 584, 599), (530, 600, 616), (531, 617, 635), (532, 636, 656), (533, 657, 675),
    (534, 676, 693), (535, 694, 711), (536, 712, 729), (537, 730, 749), (538, 750, 767),
    (539, 768, 787), (540, 788, 805), (541, 806, 826), (542, 827, 844), (543, 845, 861),
    (544, 862, 880), (545, 881, 903), (546, 904, 923), (547, 924, 939)
]

all_phams = [
    (1, 'IV. PHẨM THIÊN ĐẾ'),
    (32, 'V. PHẨM HIỆN BẢO THÁP'),
    (60, 'VI. PHẨM XƯNG DƯƠNG CÔNG ĐỨC'),
    (76, 'VII. PHẨM XÁ-LỢI PHẬT'),
    (85, 'VIII. PHẨM PHƯỚC TỤ'),
    (107, 'IX. PHẨM TÙY HỶ HỒI HƯỚNG'),
    (125, 'X. PHẨM ĐỊA NGỤC'),
    (144, 'XI. PHẨM TÁN THÁN THANH TỊNH'),
    (164, 'XII. PHẨM TÁN THÁN CÔNG ĐỨC'),
    (172, 'XIII. PHẨM ĐÀ-LA-NI'),
    (194, 'XIV. PHẨM VIỆC MA'),
    (213, 'XV. PHẨM HIỆN THẾ GIAN'),
    (231, 'XVI. PHẨM BẤT TƯ NGHÌ ĐẲNG'),
    (236, 'XVII. PHẨM THÍ DỤ'),
    (250, 'XVIII. PHẨM BẠN LÀNH'),
    (268, 'XIX. PHẨM CHƠN NHƯ'),
    (293, 'XX. PHẨM TƯỚNG BẤT THỐI'),
    (322, 'XXI. PHẨM TƯỚNG KHÔNG'),
    (358, 'XXII. PHẨM CĂNG-GIÀ THIÊN'),
    (361, 'XXIII. PHẨM XẢO TIỆN'),
    (422, 'XXIV. PHẨM KHI HỌC'),
    (431, 'XXV. PHẨM THẤY BẤT ĐỘNG'),
    (468, 'XXVI. PHẨM PHƯƠNG TIỆN THIỆN XẢO'),
    (547, 'XXVII. PHẨM TUỆ ĐÁO BỈ NGẠN'),
    (566, 'XXVIII. PHẨM DIỆU TƯỚNG'),
    (640, 'XXIX. PHẨM THÍ BÌNH ĐẲNG'),
    (703, 'XXX. PHẨM PHẬT QUỐC'),
    (714, 'XXXI. PHẨM TUYÊN HÓA'),
    (750, 'I. PHẨM DIỆU HẠNH'),
    (772, 'II. PHẨM ĐẾ THÍCH'),
    (783, 'III. PHẨM CÚNG DƯỜNG BẢO THÁP'),
    (813, 'IV. PHẨM XƯNG DƯƠNG CÔNG ĐỨC'),
    (819, 'V. PHẨM PHƯỚC MÔN'),
    (845, 'VI. PHẨM TÙY HỶ HỒI HƯỚNG'),
    (870, 'VII. PHẨM ĐỊA NGỤC'),
    (881, 'VIII. PHẨM THANH TỊNH'),
    (892, 'IX. PHẨM KHEN NGỢI'),
    (898, 'X. PHẨM TỔNG TRÌ'),
    (913, 'XI. PHẨM MA SỰ'),
    (928, 'XII. PHẨM THẾ GIAN')
]

for q, s, e in ranges:
    if q < 538:
        # Hoi 3
        active_before = [name for p_start, name in all_phams if p_start <= s and p_start < 750]
        active_at_s = active_before[-1] if active_before else 'PHẨM KHÔNG XÁC ĐỊNH'
        in_range = [name for p_start, name in all_phams if s < p_start <= e and p_start < 750]
    else:
        # Hoi 4
        active_before = [name for p_start, name in all_phams if 750 <= p_start <= s]
        active_at_s = active_before[-1] if active_before else 'PHẨM KHÔNG XÁC ĐỊNH'
        in_range = [name for p_start, name in all_phams if s < p_start <= e and p_start >= 750]
    combined = [active_at_s] + in_range
    joined_name = ' & '.join(combined)
    print(f"    ({q}, {s}, {e}, '{joined_name}'),")
