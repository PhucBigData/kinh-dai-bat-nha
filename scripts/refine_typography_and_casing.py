import glob
import re
import os

files = sorted(glob.glob('Tap_*/*.md'))
print(f"Refining typography, casing, and OCR artifacts across {len(files)} files...")

total_modified_files = 0

# Transliterated Buddhist hyphenated compounds
hyphen_compounds = [
    ('Bồ', 'đề'), ('ba', 'la'), ('Ba', 'la'), ('Tam', 'ma'), ('Bát', 'nhã'),
    ('Niết', 'bàn'), ('Đà', 'la'), ('A', 'la'), ('Bổ', 'đặc'), ('Bí', 'sô'),
    ('A', 'tu'), ('Dự', 'lưu'), ('Sa', 'môn'), ('Bà', 'la'), ('Dược', 'xoa'),
    ('A', 'tố'), ('Tát', 'đỏa'), ('Tỳ', 'nại'), ('A', 'nan'), ('Xá', 'lợi'),
    ('Thiệm', 'bộ'), ('Sát', 'đế'), ('Khẩn', 'nại'), ('Bạc', 'già'), ('Phật', 'đà'),
    ('sát', 'na'), ('do', 'tuần'), ('Yết', 'lộ'), ('bồ', 'đề'), ('Bồ', 'tát'),
    ('Ma', 'ha'), ('Độc', 'giác'), ('độc', 'giác'), ('Đại', 'thừa'), ('đại', 'thừa'),
    ('la', 'mật'), ('mật', 'đa')
]

# Split syllable mappings (de-spacing)
split_syllables = [
    ('mu ốn', 'muốn'), ('Mu ốn', 'Muốn'),
    ('hu ống', 'huống'), ('Hu ống', 'Huống'),
    ('thừ a', 'thừa'), ('Thừ a', 'Thừa'),
    ('nguyệ n', 'nguyện'), ('Nguyệ n', 'Nguyện'),
    ('thu ốc', 'thuốc'), ('Thu ốc', 'Thuốc'),
    ('tu ổi', 'tuổi'), ('Tu ổi', 'Tuổi'),
    ('chư a', 'chưa'), ('Chư a', 'Chưa'),
    ('xu ống', 'xuống'), ('Xu ống', 'Xuống'),
    ('ki ện', 'kiện'), ('Ki ện', 'Kiện'),
    ('thiệ n', 'thiện'), ('Thiệ n', 'Thiện'),
    ('di ện', 'diện'), ('Di ện', 'Diện'),
    ('thư a', 'thưa'), ('Thư a', 'Thưa'),
    ('ho ạt', 'hoạt'), ('Ho ạt', 'Hoạt'),
    ('ho ảng', 'hoảng'), ('Ho ảng', 'Hoảng'),
    ('thuyế t', 'thuyết'), ('Thuyế t', 'Thuyết'),
    ('khi ếm', 'khiếm'), ('Khi ếm', 'Khiếm'),
    ('phá p', 'pháp'), ('Phá p', 'Pháp'),
    ('vừ a', 'vừa'), ('Vừ a', 'Vừa'),
    ('chi ện', 'chiện'), ('Chi ện', 'Chiện'),
    ('cu ống', 'cuống'), ('Cu ống', 'Cuống'),
    ('bi ên', 'biên'), ('Bi ên', 'Biên'),
    ('ki ếm', 'kiếm'), ('Ki ếm', 'Kiếm'),
    ('lu ống', 'luống'), ('Lu ống', 'Luống'),
    ('thắ ng', 'thắng'), ('Thắ ng', 'Thắng'),
    ('to àn', 'toàn'), ('To àn', 'Toàn'),
    ('ho àn', 'hoàn'), ('Ho àn', 'Hoàn'),
    ('xư a', 'xưa'), ('Xư a', 'Xưa'),
    ('đư a', 'đưa'), ('Đư a', 'Đưa'),
    ('chi ếm', 'chiếm'), ('Chi ếm', 'Chiếm'),
    ('thi ệp', 'thiệp'), ('Thi ệp', 'Thiệp'),
    ('thi ếm', 'thiếm'), ('Thi ếm', 'Thiếm'),
    ('cu ốn', 'cuốn'), ('Cu ốn', 'Cuốn'),
    ('ho ạch', 'hoạch'), ('Ho ạch', 'Hoạch'),
    ('lừ a', 'lừa'), ('Lừ a', 'Lừa'),
    ('vi ện', 'viện'), ('Vi ện', 'Viện'),
    ('giá c', 'giác'), ('Giá c', 'Giác'),
    ('bá t', 'bát'), ('Bá t', 'Bát'),
    ('tu ởng', 'tưởng'), ('Tu ởng', 'Tưởng'),
    ('chuyể n', 'chuyển'), ('Chuyể n', 'Chuyển'),
    ('tướ ng', 'tướng'), ('Tướ ng', 'Tướng'),
    ('khuyế n', 'khuyến'), ('Khuyế n', 'Khuyến'),
    ('vi ên', 'viên'), ('Vi ên', 'Viên'),
    ('ki ên', 'kiên'), ('Ki ên', 'Kiên'),
    ('chu ốc', 'chuốc'), ('Chu ốc', 'Chuốc'),
    ('cu ồng', 'cuồng'), ('Cu ồng', 'Cuồng'),
    ('bu ổi', 'buổi'), ('Bu ổi', 'Buổi'),
    ('mư a', 'mưa'), ('Mư a', 'Mưa')
]

# OCR consonant fusion mappings
ocr_fusions = [
    # c + h
    (r'\bthành thụ chữu tình\b', 'thành thục hữu tình'),
    (r'\bThành thụ chữu tình\b', 'Thành thục hữu tình'),
    (r'\bhoặ chữu\b', 'hoặc hữu'),
    (r'\bHoặ chữu\b', 'Hoặc hữu'),
    (r'\bCự chỷ\b', 'Cực hỷ'),
    (r'\bcự chỷ\b', 'cực hỷ'),
    (r'\bthự chành\b', 'thực hành'),
    (r'\bThự chành\b', 'Thực hành'),
    (r'\bsắ cho ặc\b', 'sắc hoặc'),
    (r'\bSắ cho ặc\b', 'Sắc hoặc'),
    (r'\bsắ choặc\b', 'sắc hoặc'),
    (r'\bSắ choặc\b', 'Sắc hoặc'),
    (r'\bhoặ chành\b', 'hoặc hành'),
    (r'\bHoặ chành\b', 'Hoặc hành'),
    (r'\bhoặ chợp\b', 'hoặc hợp'),
    (r'\bHoặ chợp\b', 'Hoặc hợp'),
    (r'\blạ chữu\b', 'lạc hữu'),
    (r'\bsắ choàn\b', 'sắc hoàn'),
    (r'\bSắ choàn\b', 'Sắc hoàn'),
    (r'\bthứ cho ặc\b', 'thức hoặc'),
    (r'\bthứ choặc\b', 'thức hoặc'),
    (r'\btrướ chành\b', 'trước hành'),
    (r'\bhọ chành\b', 'học hành'),
    (r'\bứ chữu\b', 'ức hữu'),
    (r'\bSắ chữu\b', 'Sắc hữu'),
    (r'\bđắ chữu\b', 'đắc hữu'),
    (r'\bcá chữu\b', 'các hữu'),
    (r'\bcá chành\b', 'các hành'),
    (r'\bđượ chưởng\b', 'được hưởng'),
    (r'\bsắ chưởng\b', 'sắc hưởng'),
    (r'\blạ choàn\b', 'lạc hoàn'),
    (r'\bhọ choặc\b', 'học hoặc'),
    (r'\bthuộ choàn\b', 'thuộc hoàn'),
    
    # t + h
    (r'\bPhậ thoặc\b', 'Phật hoặc'),
    (r'\bPhậ thoặ chợp\b', 'Phật hoặc hợp'),
    (r'\bthiế thoặc\b', 'thiết hoặc'),
    (r'\bthuậ thoặc\b', 'thuận hoặc'),
    (r'\bBấ thỷ\b', 'Bất hỷ'),
    (r'\bđạ thữu\b', 'đạt hữu'),
    
    # n + h
    (r'\bnguyệ nhoặc\b', 'nguyện hoặc'),
    (r'\bNguyệ nhoặc\b', 'Nguyện hoặc'),
    (r'\bthiệ nhữu\b', 'thiện hữu'),
    (r'\bThiệ nhữu\b', 'Thiện hữu'),
    (r'\bvă nhoặc\b', 'văn hoặc'),
    (r'\bthuậ nhướng\b', 'thuận hướng'),
    (r'\bluậ nhữu\b', 'luận hữu'),
    (r'\bhiệ nhữu\b', 'hiện hữu'),
    (r'\bloạ nhữu\b', 'loạn hữu'),
    (r'\bnguyệ nhữu\b', 'nguyện hữu'),
    (r'\btiệ nhướng\b', 'tiện hướng'),
    (r'\bđế nhoặc\b', 'đến hoặc'),
    (r'\bnhẫ nhoặc\b', 'nhẫn hoặc'),
    (r'\bquá nhữu\b', 'quán hữu'),
    (r'\bthiệ nhoặc\b', 'thiện hoặc'),
    
    # p + h
    (r'\blậ phữu\b', 'lập hữu'),
    (r'\btậ phành\b', 'tập hành'),
    (r'\bhợ phướng\b', 'hợp hướng'),
    (r'\bnhậ phữu\b', 'nhập hữu'),
    
    # prepositions ở / ấy
    (r'\bhoặ cở\b', 'hoặc ở'),
    (r'\bHoặ cở\b', 'Hoặc ở'),
    (r'\bhọ cở\b', 'học ở'),
    (r'\bnghiệ pở\b', 'nghiệp ở'),
    (r'\bđượ cở\b', 'được ở'),
    (r'\bsắ cở\b', 'sắc ở'),
    (r'\bthuộ cở\b', 'thuộc ở'),
    (r'\bmắ tở\b', 'mắt ở'),
    (r'\bsắ cấy\b', 'sắc ấy'),
    (r'\bSắ cấy\b', 'Sắc ấy'),
    (r'\bPhậ tấy\b', 'Phật ấy'),
    (r'\bbắ cấy\b', 'bắc ấy'),
    (r'\bviệ cấy\b', 'việc ấy'),
    (r'\bđứ cấy\b', 'đức ấy'),
    
    # Broken i+a vowels
    (r'\bđị[ \t]+a\b', 'địa'),
    (r'\bĐị[ \t]+a\b', 'Địa'),
    (r'\blì[ \t]+a\b', 'lìa'),
    (r'\bki[ \t]+a\b', 'kia'),
    (r'\btrị[ \t]+a\b', 'trịa')
]

# Uppercase VNI corrections
vni_uppercase_map = [
    ('PHAÅM CHUYEÅN SANH', 'PHẨM CHUYỂN SANH'),
    ('PHAÅM HIEÄN TÖÔÙNG LÖÔÕI', 'PHẨM HIỆN TƯỚNG LƯỠI'),
    ('PHAÅM KHUYEÂN HOÏC', 'PHẨM KHUYÊN HỌC'),
    ('PHAÅM VOÂ TRUÏ', 'PHẨM VÔ TRỤ'),
    ('PHAÅM BOÀ-TAÙT', 'PHẨM BỒ-TÁT'),
    ('PHẨM THAÙN CHUÙNG ÑÖÙC', 'PHẨM THÁN CHÚNG ĐỨC'),
    ('CHAÚNG TRÖÔÙC TÖÔÙNG', 'CHẲNG TRƯỚC TƯỚNG'),
    ('HIEÄN BẢO THÁP', 'HIỆN BẢO THÁP'),
    ('PHẨM TRÔØI KHEN NGỢI', 'PHẨM TRỜI KHEN NGỢI'),
    ('PHẨM TÖÔÙNG BẤT THỐI', 'PHẨM TƯỚNG BẤT THỐI'),
    ('PHAÅM', 'PHẨM'),
    ('CHUYEÅN', 'CHUYỂN'),
    ('HIEÄN', 'HIỆN'),
    ('TÖÔÙNG', 'TƯỚNG'),
    ('LÖÔÕI', 'LƯỠI'),
    ('KHUYEÂN', 'KHUYÊN'),
    ('HOÏC', 'HỌC'),
    ('VOÂ', 'VÔ'),
    ('TRUÏ', 'TRỤ'),
    ('BOÀ', 'BỒ'),
    ('TAÙT', 'TÁT'),
    ('THAÙN', 'THÁN'),
    ('CHUÙNG', 'CHÚNG'),
    ('ÑÖÙC', 'ĐỨC'),
    ('CHAÚNG', 'CHẲNG'),
    ('TRÖÔÙC', 'TRƯỚC'),
    ('TRÔØI', 'TRỜI')
]

for p in files:
    with open(p, 'r', encoding='utf-8') as f:
        original = f.read()
    
    modified = original
    
    # 1. Standardize Icelandic Eth 'Ð' (U+00D0) & merge detached 'Đ'
    modified = re.sub(r'\b[ÐĐ][ \t]+(?=[a-zà-ỹđA-ZÀ-ỸĐ])', 'Đ', modified)
    modified = modified.replace('Ð', 'Đ')
    
    # 2. Clean leaked PDF running headers (in tables and body text)
    # Inside summary table row:
    modified = re.sub(r'(\|\s*\*\*\d+\*\*\s*\|\s*\d+\s*\|\s*)Kinh Đại Bát[- ]Nhã Ba[- ]La[- ]Mật[- ]Đa\s*', r'\1', modified)
    # At start of line:
    modified = re.sub(r'(?:^|\n)Kinh Đại Bát[- ]Nhã Ba[- ]La[- ]Mật[- ]Đa(?:\s+\d+|\s+Tập\s+\d+)?\s*', r'\n', modified)
    # Inside body paragraph:
    modified = re.sub(r'\s*Kinh Đại Bát[- ]Nhã Ba[- ]La[- ]Mật[- ]Đa(?:\s+\d+|\s+Tập\s+\d+)?\s*', ' ', modified)
    # Specific Tap 09 page headers
    modified = re.sub(r'Tập\s+09,\s+Quyển\s+450,\s+Phẩm\s+Nghĩa\s+Thậm\s+Thâm\s+', '', modified)
    modified = re.sub(r'Tập\s+09,\s+Quyển\s+453,\s+Phẩm\s+Tăng\s+Thượng\s+Mạn\s+', '', modified)
    
    # 3. Uppercase VNI corrections
    for vni, uni in vni_uppercase_map:
        modified = modified.replace(vni, uni)
        
    # 4. OCR consonant fusions
    for pat, rep in ocr_fusions:
        modified = re.sub(pat, rep, modified)
        
    # 5. Split syllables
    for s_split, s_join in split_syllables:
        modified = modified.replace(s_split, s_join)
        
    # 6. Broken hyphens in Buddhist terms
    for w1, w2 in hyphen_compounds:
        modified = re.sub(rf'\b{w1}[ \t]*-[ \t]*{w2}\b', f'{w1}-{w2}', modified)
        
    # 7. Buddhist Honorifics & Names Casing
    modified = re.sub(r'\bnhư Lai\b', 'Như Lai', modified)
    modified = re.sub(r'\bNày thiện Hiện\b', 'Này Thiện Hiện', modified)
    modified = re.sub(r'\bThiện hiện thưa:', 'Thiện Hiện thưa:', modified)
    modified = re.sub(r'\bThiện hiện đáp:', 'Thiện Hiện đáp:', modified)
    modified = re.sub(r'\bThiện hiện bảo:', 'Thiện Hiện bảo:', modified)
    modified = re.sub(r'\bThiện hiện bạch Phật:', 'Thiện Hiện bạch Phật:', modified)
    modified = re.sub(r'-Thiện hiện!', '-Thiện Hiện!', modified)
    modified = re.sub(r'\btôn giả thiện Hiện\b', 'tôn giả Thiện Hiện', modified)
    modified = re.sub(r'\bđức phật\b', 'đức Phật', modified)
    modified = re.sub(r'\bnhư lai Ứng Chánh Đẳng Giác\b', 'Như Lai Ứng Chánh Đẳng Giác', modified)
    modified = re.sub(r'\bnhư lai và tự tánh\b', 'Như Lai và tự tánh', modified)
    modified = re.sub(r'\bbậc như lai\b', 'bậc Như Lai', modified)
    modified = re.sub(r'\bbồ-tát\b', 'Bồ-tát', modified)
    modified = re.sub(r'\bTam-ma-đị[ \t]+a\b', 'Tam-ma-địa', modified)
    modified = re.sub(r'[Tt]huyế[ \t]+tgi[ \t]+ảng', 'thuyết giảng', modified)
    modified = re.sub(r'\bNhư lai\b', 'Như Lai', modified)
    modified = re.sub(r'\bThế tôn\b', 'Thế Tôn', modified)
    modified = re.sub(r'\bBồ tát\b', 'Bồ-tát', modified)
    
    # 8. Tone and Quote Corrections
    modified = re.sub(r'\btuởng\b', 'tưởng', modified)
    modified = re.sub(r'\bđuợc\b', 'được', modified)
    modified = re.sub(r'\bĐuợc\b', 'Được', modified)
    modified = re.sub(r'\bthuờng\b', 'thường', modified)
    modified = re.sub(r'\bThuờng\b', 'Thường', modified)
    modified = re.sub(r'\bluợng\b', 'lượng', modified)
    modified = re.sub(r'\btruớc\b', 'trước', modified)
    modified = re.sub(r'\bphuơng\b', 'phương', modified)
    modified = modified.replace('„rốt ráo‟', '"rốt ráo"')
    modified = modified.replace('„tự nhiên tính‟', '"tự nhiên tính"')
    
    # 9. Punctuation noise & table truncation fixes
    modified = modified.replace('Như Lai Ứng Chánh Đ... |', 'Như Lai Ứng Chánh Đẳng Giác... |')
    modified = modified.replace('thiết độc-giác hướng, Đ... |', 'thiết độc-giác hướng, độc-giác quả... |')
    modified = modified.replace(',.', ', ')
    modified = modified.replace(',;', '; ')
    modified = modified.replace(',,', ', ')
    
    # 10. Sentence-initial & Dialogue Capitalization
    modified = re.sub(r'(?<!v\.v)(?<!\.\.\.)\.\s+như vậy\b', '. Như vậy', modified)
    modified = re.sub(r'(?<!v\.v)(?<!\.\.\.)\.\s+lại nữa\b', '. Lại nữa', modified)
    modified = re.sub(r'(?<!v\.v)(?<!\.\.\.)\.\s+cả hai\b', '. Cả hai', modified)
    modified = re.sub(r'(?<!v\.v)(?<!\.\.\.)\.\s+cả ba\b', '. Cả ba', modified)
    modified = re.sub(r'(?<!v\.v)(?<!\.\.\.)\.\s+vì sao\b', '. Vì sao', modified)
    modified = re.sub(r'(?<!v\.v)(?<!\.\.\.)\.\s+tất cả\b', '. Tất cả', modified)
    modified = re.sub(r'(?<!v\.v)(?<!\.\.\.)\.\s+người (muốn|cầu|tu|thuyết)\b', r'. Người \1', modified)
    modified = re.sub(r'(?<!v\.v)(?<!\.\.\.)\.\s+hữu tình\b', '. Hữu tình', modified)
    modified = re.sub(r'\n-như tâm\b', '\n-Như tâm', modified)
    
    if modified != original:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(modified)
        total_modified_files += 1

print(f"Refinement complete! Successfully updated {total_modified_files} files.")