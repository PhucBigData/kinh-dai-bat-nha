import pypdf
import re
from scripts.batch_processor import clean_vietnamese_text

ranges = [
    (436, 1, 20), (437, 21, 41), (438, 42, 58), (439, 59, 74), (440, 75, 91),
    (441, 92, 107), (442, 108, 125), (443, 126, 143), (444, 144, 159), (445, 160, 174),
    (446, 175, 191), (447, 192, 208), (448, 209, 225), (449, 226, 242), (450, 243, 258),
    (451, 259, 275), (452, 276, 289), (453, 290, 303), (454, 304, 323), (455, 324, 339),
    (456, 340, 356), (457, 357, 372), (458, 373, 389), (459, 390, 404), (460, 405, 421),
    (461, 422, 437), (462, 438, 455), (463, 456, 472), (464, 473, 490), (465, 491, 508),
    (466, 509, 526), (467, 527, 543), (468, 544, 561), (469, 562, 578), (470, 579, 596),
    (471, 597, 614), (472, 615, 631), (473, 632, 649), (474, 650, 666), (475, 667, 683),
    (476, 684, 700), (477, 701, 719), (478, 720, 741), (479, 742, 759), (480, 760, 777),
    (481, 778, 794), (482, 795, 811), (483, 812, 830), (484, 831, 849), (485, 850, 869),
    (486, 870, 888), (487, 889, 905), (488, 906, 923), (489, 924, 939), (490, 940, 956),
    (491, 957, 974), (492, 975, 992), (493, 993, 1007), (494, 1008, 1022), (495, 1023, 1038),
    (496, 1039, 1055), (497, 1056, 1073), (498, 1074, 1086)
]

all_phams = [
    (1, 'XL. PHẨM THANH TỊNH'),
    (17, 'XLI. PHẨM KHÔNG NÊU CỜ'),
    (34, 'XLII. PHẨM BẤT KHẢ ĐẮC'),
    (42, 'XLIII. PHẨM PHƯƠNG ĐÔNG BẮC'),
    (78, 'XLIV. PHẨM MA SỰ'),
    (87, 'XLV. PHẨM KHÔNG HÒA HỢP'),
    (103, 'XLVI. PHẨM PHẬT MẪU'),
    (121, 'XLVII. PHẨM CHỈ TƯỚNG'),
    (144, 'XLVIII. PHẨM THÀNH BIỆN'),
    (154, 'XLIX. PHẨM THUYỀN ĐẲNG DỤ'),
    (164, 'L. PHẨM SƠ NGHIỆP'),
    (182, 'LI. PHẨM ĐIỀU PHỤC THAM ĐẲNG'),
    (188, 'LII. PHẨM CHƠN NHƯ'),
    (215, 'LIII. PHẨM BẤT THỐI CHUYỂN'),
    (226, 'LIV. PHẨM CHUYỂN BẤT CHUYỂN'),
    (243, 'LV. PHẨM NGHĨA THẬM THÂM'),
    (259, 'LVI. PHẨM MỘNG HÀNH'),
    (262, 'LVII. PHẨM HẠNH NGUYỆN'),
    (273, 'LVIII. PHẨM CĂNG-GIÀ THIÊN'),
    (276, 'LIX. PHẨM TẬP CẬN'),
    (290, 'LX. PHẨM TĂNG THƯỢNG MẠN'),
    (318, 'LXI. PHẨM ĐỒNG HỌC'),
    (333, 'LXII. PHẨM ĐỒNG TÁNH'),
    (343, 'LXIII. PHẨM KHÔNG PHÂN BIỆT'),
    (354, 'LXIV. PHẨM KIÊN CỐ CHẲNG KIÊN CỐ'),
    (369, 'LXV. PHẨM THẬT NGỮ'),
    (384, 'LXVI. PHẨM VÔ TẬN'),
    (390, 'LXVII. PHẨM TƯƠNG NHIẾP'),
    (405, 'LXVIII. PHẨM PHƯƠNG TIỆN THIỆN XẢO'),
    (461, 'LXIX. PHẨM THỌ DỤ'),
    (473, 'LXX. PHẨM BỒ-TÁT HẠNH'),
    (478, 'LXXI. PHẨM THÂN CẬN'),
    (484, 'LXXII. PHẨM HỌC TẤT CẢ'),
    (505, 'LXXIII. PHẨM TUẦN TỰ'),
    (520, 'LXXIV. PHẨM VÔ TƯỚNG'),
    (538, 'LXXV. PHẨM KHÔNG TẠP'),
    (555, 'LXXVI. PHẨM CÁC ĐỨC TƯỚNG'),
    (604, 'LXXVII. PHẨM THIỆN ĐẠT'),
    (636, 'LXXVIII. PHẨM THẬT TẾ'),
    (663, 'LXXIX. PHẨM VÔ KHUYẾT'),
    (684, 'LXXX. PHẨM ĐẠO SĨ'),
    (701, 'LXXXI. PHẨM CHÁNH ĐỊNH'),
    (713, 'LXXXII. PHẨM PHẬT PHÁP'),
    (720, 'LXXXIII. PHẨM VÔ SỰ'),
    (727, 'LXXXIV. PHẨM NÓI THẬT'),
    (739, 'LXXXV. PHẨM TÁNH KHÔNG'),
    (742, 'I. PHẨM DUYÊN KHỞI'),
    (750, 'II. PHẨM XÁ-LỢI TỬ'),
    (805, 'III. PHẨM THIỆN HIỆN')
]

for q, s, e in ranges:
    if q < 479:
        # Hoi 2
        active_before = [name for p_start, name in all_phams if p_start <= s and p_start < 742]
        active_at_s = active_before[-1] if active_before else 'PHẨM KHÔNG XÁC ĐỊNH'
        in_range = [name for p_start, name in all_phams if s < p_start <= e and p_start < 742]
    else:
        # Hoi 3
        active_before = [name for p_start, name in all_phams if 742 <= p_start <= s]
        active_at_s = active_before[-1] if active_before else 'PHẨM KHÔNG XÁC ĐỊNH'
        in_range = [name for p_start, name in all_phams if s < p_start <= e and p_start >= 742]
    combined = [active_at_s] + in_range
    joined_name = ' & '.join(combined)
    print(f"    ({q}, {s}, {e}, '{joined_name}'),")
