import pypdf
import os
import re

vowels = 'aàáảãạăằắẳẵặâầấẩẫậeèéẻẽẹêềếểễệiìíỉĩịoòóỏõọôồốổỗộơờớởỡợuùúủũụưừứửữựyỳýỷỹỵ'
VOWELS = vowels + vowels.upper()
onsets = 'ch|gh|gi|kh|nh|ng|ngh|ph|qu|th|tr|[bcdđghklmnpqrstvx]'
UPPER_VN = 'A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬEÉÈẺẼẸÊẾỀỂỄỆIÍÌỈĨỊOÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢUÚÙỦŨỤƯỨỪỬỮỰYÝỲỶỸỴĐ'
LOWER_VN = 'a-zàáảãạăằắẳẵặâầấẩẫậeèéẻẽẹêềếểễệiìíỉĩịoòóỏõọôồốổỗộơờớởỡợuùúủũụưừứửữựyỳýỷỹỵđ'
rhymes = 'ộc|ệc|ết|ệu|ỡng|ược|ượt|ướng|ượng|ền|ệm|ến|ếng|ễm|ềm|ếp|ỷu|ếu|ễn|ệt|ếc'

split_pairs = [
    (r'\bhu[ \t]+ệ\b', 'huệ'),
    (r'\btu[ \t]+ệ\b', 'tuệ'),
    (r'\bcủ[ \t]+a\b', 'của'),
    (r'\bđ[ \t]+à\b', 'đà'),
    (r'\bs[ \t]+ố\b', 'số'),
    (r'\bt[ \t]+ừ\b', 'từ'),
    (r'\bb[ \t]+ỏ\b', 'bỏ'),
    (r'\bch[ \t]+ớ\b', 'chớ'),
    (r'\bch[ \t]+ỗ\b', 'chỗ'),
    (r'\bs[ \t]+ự\b', 'sự'),
    (r'\bnh[ \t]+ư\b', 'như'),
    (r'\bv[ \t]+ới\b', 'với'),
    (r'\bl[ \t]+ại\b', 'lại'),
    (r'\bm[ \t]+ột\b', 'một'),
    (r'\bth[ \t]+ời\b', 'thời'),
    (r'\bv[ \t]+ầy\b', 'vầy'),
    (r'\bl[ \t]+ậu\b', 'lậu'),
    (r'\br[ \t]+ốt\b', 'rốt'),
    (r'\bt[ \t]+ột\b', 'tột'),
    (r'\bh[ \t]+ạnh\b', 'hạnh'),
    (r'\bc[ \t]+ắt\b', 'cắt'),
    (r'\bt[ \t]+ại\b', 'tại'),
    (r'\bl[ \t]+ượng\b', 'lượng'),
    (r'\bt[ \t]+ất\b', 'tất'),
    (r'\bc[ \t]+ả\b', 'cả'),
    (r'\bB[ \t]+ồ\b', 'Bồ'),
    (r'\bv[ \t]+ui\b', 'vui'),
    (r'\bkh[ \t]+ởi\b', 'khởi'),
    (r'\bth[ \t]+ật\b', 'thật'),
    (r'\bđ[ \t]+ỉnh\b', 'đỉnh'),
    (r'\bph[ \t]+áp\b', 'pháp'),
    (r'\bPh[ \t]+ật\b', 'Phật'),
    (r'\bV[ \t]+ương\b', 'Vương'),
    (r'\bTh[ \t]+ứu\b', 'Thứu'),
    (r'\bư[ \t]+ớc\b', 'ước'),
    (r'\btr[ \t]+ước\b', 'trước'),
    (r'\bn[ \t]+ước\b', 'nước'),
    (r'\bkh[ \t]+ông\b', 'không'),
    (r'\bngh[ \t]+ĩ\b', 'nghĩ'),
    (r'\bngh[ \t]+e\b', 'nghe'),
    (r'\bn[ \t]+ghe\b', 'nghe'),
    (r'\bn[ \t]+ghĩ\b', 'nghĩ'),
    (r'\bnh[ \t]+ận\b', 'nhận'),
    (r'\bth[ \t]+ấy\b', 'thấy'),
    (r'\bth[ \t]+ể\b', 'thể'),
    (r'\bđ[ \t]+ược\b', 'được'),
    (r'\bng[ \t]+ười\b', 'người'),
    (r'\bh[ \t]+ữu\b', 'hữu'),
    (r'\bh[ \t]+iện\b', 'hiện'),
    (r'\bđ[ \t]+iềm\b', 'điềm'),
    (r'\bl[ \t]+ành\b', 'lành'),
    (r'\bl[ \t]+ễ\b', 'lễ'),
    (r'\bb[ \t]+ái\b', 'bái'),
    (r'\bc[ \t]+úng\b', 'cúng'),
    (r'\bd[ \t]+ường\b', 'dường'),
    (r'\bgi[ \t]+ã\b', 'giã'),
    (r'\bv[ \t]+ân\b', 'vân'),
    (r'\bt[ \t]+ập\b', 'tập'),
    (r'\bt[ \t]+oàn\b', 'toàn'),
    (r'\bh[ \t]+oàn\b', 'hoàn'),
    (r'\bg[ \t]+iới\b', 'giới'),
    (r'\bt[ \t]+rên\b', 'trên'),
    (r'\bd[ \t]+ưới\b', 'dưới'),
    (r'\bph[ \t]+ương\b', 'phương'),
    (r'\b(h|H)o[ \t]+ặc\b', r'\1oặc'),
    (r'\b(t|T)hi[ \t]+ện\b', r'\1hiện'),
    (r'\b(t|T)i[ \t]+ện\b', r'\1iện'),
    (r'\b(h|H)i[ \t]+ện\b', r'\1iện'),
    (r'\b(n|N)go[ \t]+ại\b', r'\1goại'),
    (r'\b(n|N)guy[ \t]+ện\b', r'\1guyện'),
    (r'\b(l|L)o[ \t]+ại\b', r'\1oại'),
    (r'\b(h|H)i[ \t]+ểu\b', r'\1iểu'),
    (r'\b(x|X)u[ \t]+ất\b', r'\1uất'),
    (r'\b(h|H)o[ \t]+ại\b', r'\1oại'),
    (r'\b(n|N)ghi[ \t]+ệp\b', r'\1ghiệp'),
    (r'\b(k|K)ho[ \t]+ảng\b', r'\1hoảng'),
    (r'\b(h|H)i[ \t]+ệp\b', r'\1iệp'),
    (r'\b(b|B)i[ \t]+ện\b', r'\1iện'),
    (r'\b(b|B)i[ \t]+ển\b', r'\1iển'),
    (r'\b(n|N)hi[ \t]+ễu\b', r'\1hiễu'),
    (r'\b(c|C)huy[ \t]+ển\b', r'\1huyển'),
    (r'\b(t|T)ri[ \t]+ển\b', r'\1riển'),
    (r'\b(t|T)i[ \t]+ểu\b', r'\1iểu'),
    (r'\b(l|L)u[ \t]+ận\b', r'\1uận'),
    (r'\b(t|T)hu[ \t]+ận\b', r'\1huận'),
    (r'\b(l|L)o[ \t]+ạn\b', r'\1oạn'),
    (r'\b(t|T)hi[ \t]+ểu\b', r'\1hiểu'),
    (r'\b(k|K)hu[ \t]+ất\b', r'\1huất'),
    (r'\b(c|C)hu[ \t]+ẩn\b', r'\1huẩn'),
    (r'\b(d|D)uy[ \t]+ệt\b', r'\1uyệt'),
    (r'\b(t|T)huy[ \t]+ết\b', r'\1huyết'),
    (r'\b(q|Q)uy[ \t]+ết\b', r'\1uyết'),
    (r'\b(t|T)uy[ \t]+ệt\b', r'\1uyệt'),
    (r'\b(n|N)ghĩ[ \t]+a\b', r'\1ghĩa'),
    (r'\bthiệ[ \t]+n\b', 'thiện'),
    (r'\bThiệ[ \t]+n\b', 'Thiện'),
]

def clean_vietnamese_text(text):
    text = re.sub(r'-[ \t]+', '-', text)
    # 0. Merge split digraph onsets: c h, t h, n h, k h, p h, n g, t r, g i, g h, n gh
    text = re.sub(r'\b(c|t|n|k|p|g)[ \t]+(h|g|r|i)(?=[ \t]*[' + VOWELS + r'])', r'\1\2', text, flags=re.IGNORECASE)
    text = re.sub(r'\bn[ \t]+gh(?=[ \t]*[' + VOWELS + r'])', 'ngh', text, flags=re.IGNORECASE)

    for pat, repl in split_pairs:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
        
    for _ in range(5):
        # 1. Onset consonant + space + vowel
        text = re.sub(r'\b(' + onsets + r')[ \t]+([' + VOWELS + r'])', r'\1\2', text, flags=re.IGNORECASE)
        # 2. Vowel + space + coda (including g and h after n)
        text = re.sub(r'(?<=[a-zà-ỹA-ZÀ-Ỹ]n)[ \t]+([gh])\b', r'\1', text, flags=re.IGNORECASE)
        text = re.sub(r'(?<=[' + VOWELS + r'])[ \t]+(ch|ng|nh|[cmnpt])(?=[^\w\s]|[ \t]|$)', r'\1', text, flags=re.IGNORECASE)
        # 3. Vowel offglides
        text = re.sub(r'(?<=[' + VOWELS + r'])[ \t]+([iyuov])(?=[^\w\s]|[ \t]|$)', r'\1', text, flags=re.IGNORECASE)
        # 4. Known bound suffixes
        text = re.sub(r'\b([' + LOWER_VN + UPPER_VN + r']+)[ \t]+(' + rhymes + r')\b', r'\1\2', text)
    
    text = re.sub(r'\b(nhi|th|đ|ti|tri|li)[ \t]+(ều|êu|ệu|êm|ết)\b', r'\1\2', text, flags=re.IGNORECASE)
    text = re.sub(r',([^\s\d])', r', \1', text)
    text = re.sub(r'([^\s])v\.v', r'\1 v.v', text)
    
    # Specific OCR artifacts & VNI header conversions
    text = text.replace('Thiệ nHi ện', 'Thiện Hiện')
    text = re.sub(r'\b[ðÐ][ \t]+ại\b', 'Đại', text)
    text = re.sub(r'\b[ðÐ][ \t]+ộc\b', 'độc', text)
    text = text.replace('Ðại', 'Đại')
    text = text.replace('Ð ại', 'Đại')
    text = text.replace('phàp mầu', 'pháp mầu')
    text = text.replace('nguời', 'người')
    text = text.replace('ngu ời', 'người')
    text = text.replace('Cực Lạ cở', 'Cực Lạc ở')
    text = text.replace('Phậ tở', 'Phật ở')
    text = re.sub(r'\b[bB]ồ[ \t]*-[ \t]*tát\b', 'Bồ-tát', text)
    text = text.replace('Bồ -tát', 'Bồ-tát')
    text = text.replace('íc h', 'ích')
    text = text.replace('như Lai', 'Như Lai')
    text = text.replace('Lúc Bấy giờ', 'Lúc bấy giờ')
    text = text.replace('định vương diệu', 'định Vương diệu')
    text = text.replace('đượ cít', 'được ít')
    text = text.replace('Ch ơn T ự T ại', 'Chơn Tự Tại')
    text = text.replace('chữ Đức ( )', 'chữ Đức (卍)')

    # Specific missing/truncated words in typesetting
    text = re.sub(r'\bchẳng thấy[ \t]+q\b', 'chẳng thấy quả', text)
    text = re.sub(r'\bthấy[ \t]+q\b', 'thấy quả', text)
    text = re.sub(r'\bt[ \t]+đó là\b', 'thì đó là', text)
    text = re.sub(r'\bt[ \t]+Thiện Hiện\b', 'Phật bảo Thiện Hiện', text)
    text = re.sub(r'\ban nhẫn,[ \t]+t(?=[ \t]*[;,.\n]|\b)', 'an nhẫn, tinh tấn', text)
    text = re.sub(r'\ban nhẫn,[ \t]+t[ \t]+mà cầu\b', 'an nhẫn, tinh tấn mà cầu', text)
    text = re.sub(r'\ban nhẫn,[ \t]+t[ \t]+có thể\b', 'an nhẫn, tinh tấn có thể', text)
    text = re.sub(r'\ban nhẫn,[ \t]+t[ \t]+hoặc\b', 'an nhẫn, tinh tấn hoặc', text)
    text = re.sub(r'\bpháp tánh,[ \t]+t[ \t]+tánh bình đẳng\b', 'pháp tánh, tánh bình đẳng', text)
    text = re.sub(r'\bt đa inh tấn, tịnh lự\b', 'tinh tấn, tịnh lự', text)
    text = re.sub(r'\btánh[ \t]+c[ \t]+pháp\b', 'tánh của pháp', text)
    text = re.sub(r'\bđắc[ \t]+c[ \t]+Như Lai\b', 'đắc Như Lai', text)
    text = re.sub(r'\bB[ \t]+Ba-la-mật-đa\b', 'Bát-nhã Ba-la-mật-đa', text)

    # VNI uppercase titles in text stream
    text = text.replace('các h ', 'cách ')
    text = text.replace('lạ cở', 'lạc ở')
    text = text.replace('PHAÀN MAÏN-THUØ-THAÁT-LÔÏI', 'PHẦN MẠN-THÙ-THẤT-LỢI')
    text = text.replace('PHAÀN NA-GIAØ-THAÁT-LÔÏI', 'PHẦN NA-GIÀ-THẤT-LỢI')
    text = text.replace('PHAÀN KIM CÖÔNG NAÊNG ÑOAÏN', 'PHẦN KIM CƯƠNG NĂNG ĐOẠN')
    text = text.replace('PHAÀN LYÙ THUÙ BAÙT-NHAÕ', 'PHẦN LÝ THÚ BÁT-NHÃ')
    text = text.replace('PHAÀN BOÁ THÍ BA-LA-MAÄT-ÑA', 'PHẦN BỐ THÍ BA-LA-MẬT-ĐA')
    text = text.replace('PHAÀN TÒNH GIÔÙI BA-LA-MAÄT-ÑA', 'PHẦN TỊNH GIỚI BA-LA-MẬT-ĐA')
    text = text.replace('PHAÀN TÓNH LÖÏ BA-LA-MAÄT-ÑA', 'PHẦN TĨNH LỰ BA-LA-MẬT-ĐA')
    text = text.replace('LYÙ THUÙ BAÙT-NHAÕ', 'LÝ THÚ BÁT-NHÃ')
    text = text.replace('TRÔØI KHEN NGỢI', 'TRỜI KHEN NGỢI')
    text = text.replace('SAÂU XA', 'SÂU XA')
    text = text.replace('BIEÁT VIỆC MA', 'BIẾT VIỆC MA')
    text = text.replace('THIEÄN HÖÕU', 'THIỆN HỮU')
    text = text.replace('THIEÂN CHUÛ', 'THIÊN CHỦ')
    text = text.replace('VOÂ TAÏP VOÂ DÒ', 'VÔ TẠP VÔ DỊ')
    text = text.replace('TAÁN TOÁC', 'TẤN TỐC')
    text = text.replace('KIEÂN COÁ', 'KIÊN CỐ')
    text = text.replace('THAÀN CHUÙ', 'THẦN CHÚ')
    text = text.replace('KINH ÑIEÅN', 'KINH ĐIỂN')
    text = text.replace('HOÀI HÖÔÙNG', 'HỒI HƯỚNG')
    text = text.replace('BAÁT TÖ NGHÌ', 'BẤT TƯ NGHÌ')
    text = text.replace('NHÖ LAI', 'NHƯ LAI')
    text = text.replace('BAÁT THOÁI', 'BẤT THỐI')
    text = text.replace('THAM HAØNH', 'THAM HÀNH')
    text = text.replace('TYÛ MUOÄI', 'TỶ MUỘI')
    text = text.replace('TU HOÏC', 'TU HỌC')
    text = text.replace('TROÀNG CAÊN LAØNH', 'TRỒNG CĂN LÀNH')
    text = text.replace('PHOÙ CHUÙC', 'PHÓ CHÚC')
    text = text.replace('KIEÁN BAÁT ÑOÄNG PHAÄT', 'KIẾN BẤT ĐỘNG PHẬT')
    text = text.replace('THOÂNG ÑAÏT', 'THÔNG ĐẠT')
    text = text.replace('PHAÙP GIÔÙI', 'PHÁP GIỚI')
    text = text.replace('NIEÄM TRUÏ', 'NIỆM TRỤ')
    text = text.replace('BÌNH ÑAÚNG', 'BÌNH ĐẲNG')
    text = text.replace('HIEÄN TÖÔÙNG', 'HIỆN TƯỚNG')
    text = text.replace('CHÖÙNG KHUYEÁN', 'CHỨNG KHUYẾN')
    text = text.replace('HIEÄN HOÙA', 'HIỆN HÓA')
    text = text.replace('KHYEÂN RAÊN', 'KHUYÊN RĂN')
    text = text.replace('NHÒ HAÏNH', 'NHỊ HẠNH')
    text = text.replace('HOÄI THÖÙ 5', 'HỘI THỨ NĂM')
    text = text.replace('HOÄI THÖÙ 6', 'HỘI THỨ SÁU')
    text = text.replace('HOÄI THÖÙ 7', 'HỘI THỨ BẢY')
    text = text.replace('HOÄI THÖÙ 8', 'HỘI THỨ TÁM')
    text = text.replace('HOÄI THÖÙ 9', 'HỘI THỨ CHÍN')
    text = text.replace('HOÄI THÖÙ 10', 'HỘI THỨ MƯỜI')
    text = text.replace('HOÄI THÖÙ 11', 'HỘI THỨ MƯỜI MỘT')
    text = text.replace('HOÄI THÖÙ 12', 'HỘI THỨ MƯỜI HAI')
    text = text.replace('HOÄI THÖÙ 13', 'HỘI THỨ MƯỜI BA')
    text = text.replace('HOÄI THÖÙ 14', 'HỘI THỨ MƯỜI BỐN')
    text = text.replace('HOÄI THÖÙ 15', 'HỘI THỨ MƯỜI LĂM')
    text = text.replace('HOÄI THÖÙ 16', 'HỘI THỨ MƯỜI SÁU')
    text = text.replace('HỘI THỨ 5', 'HỘI THỨ NĂM')
    text = text.replace('HỘI THỨ 6', 'HỘI THỨ SÁU')
    text = text.replace('HỘI THỨ 7', 'HỘI THỨ BẢY')
    text = text.replace('HỘI THỨ 8', 'HỘI THỨ TÁM')
    text = text.replace('HỘI THỨ 9', 'HỘI THỨ CHÍN')
    text = text.replace('HỘI THỨ 10', 'HỘI THỨ MƯỜI')
    text = text.replace('HỘI THỨ 11', 'HỘI THỨ MƯỜI MỘT')
    text = text.replace('HỘI THỨ 12', 'HỘI THỨ MƯỜI HAI')
    text = text.replace('HỘI THỨ 13', 'HỘI THỨ MƯỜI BA')
    text = text.replace('HỘI THỨ 14', 'HỘI THỨ MƯỜI BỐN')
    text = text.replace('HỘI THỨ 15', 'HỘI THỨ MƯỜI LĂM')
    text = text.replace('HỘI THỨ 16', 'HỘI THỨ MƯỜI SÁU')
    text = text.replace('THAÄM THAÂM TÖÔÙNG', 'THẬM THÂM TƯỚNG')
    text = text.replace('THAÉNG YÙ LAÏC', 'THẮNG Ý LẠC')
    text = text.replace('HIEÅN TÖÔÙNG', 'HIỂN TƯỚNG')
    text = text.replace('PHAÙP TAÙNH', 'PHÁP TÁNH')
    text = text.replace('HIEÅN ÑÖÙC', 'HIỂN ĐỨC')
    text = text.replace('XAÙ-LÔÏI', 'XÁ-LỢI')
    text = text.replace('HOÄI THÖÙ TÖ', 'HỘI THỨ TƯ')
    text = text.replace('HỘI THỨ TƯ', 'HỘI THỨ TƯ')
    text = text.replace('HIEÄN BẢO THÁP', 'HIỆN BẢO THÁP')
    text = text.replace('XÖNG DÖÔNG', 'XƯNG DƯƠNG')
    text = text.replace('XAÙ-LÔÏI PHAÄT', 'XÁ-LỢI PHẬT')
    text = text.replace('PHÖÔÙC TUÏ', 'PHƯỚC TỤ')
    text = text.replace('TAÙN THAÙN THANH TỊNH', 'TÁN THÁN THANH TỊNH')
    text = text.replace('TAÙN THAÙN CÔNG ĐỨC', 'TÁN THÁN CÔNG ĐỨC')
    text = text.replace('TAÙN THAÙN', 'TÁN THÁN')
    text = text.replace('ÑAØ-LA-NI', 'ĐÀ-LA-NI')
    text = text.replace('VIEÄC MA', 'VIỆC MA')
    text = text.replace('HIEÄN THEÁ GIAN', 'HIỆN THẾ GIAN')
    text = text.replace('THEÁ GIAN', 'THẾ GIAN')
    text = text.replace('BAÁT TÖ NGHÌ ÑAÚNG', 'BẤT TƯ NGHÌ ĐẲNG')
    text = text.replace('BAÏN LAØNH', 'BẠN LÀNH')
    text = text.replace('TÖÔÙNG BAÁT THOÁI', 'TƯỚNG BẤT THỐI')
    text = text.replace('TÖÔÙNG KHOÂNG', 'TƯỚNG KHÔNG')
    text = text.replace('XAÛO TIEÄN', 'XẢO TIỆN')
    text = text.replace('KHI HOÏC', 'KHI HỌC')
    text = text.replace('THAÁY BAÁT ÑOÄNG', 'THẤY BẤT ĐỘNG')
    text = text.replace('TUEÄ ÑAÙO BÆ NGAÏN', 'TUỆ ĐÁO BỈ NGẠN')
    text = text.replace('DIEÄU TÖÔÙNG', 'DIỆU TƯỚNG')
    text = text.replace('THÍ BÌNH ÑAÚNG', 'THÍ BÌNH ĐẲNG')
    text = text.replace('PHAÄT QUOÁC', 'PHẬT QUỐC')
    text = text.replace('TUYEÂN HOÙA', 'TUYÊN HÓA')
    text = text.replace('DIEÄU HAÏNH', 'DIỆU HẠNH')
    text = text.replace('CUÙNG DÖÔØNG BẢO THÁP', 'CÚNG DƯỜNG BẢO THÁP')
    text = text.replace('CUÙNG DÖÔØNG', 'CÚNG DƯỜNG')
    text = text.replace('PHÖÔÙC MOÂN', 'PHƯỚC MÔN')
    text = text.replace('KHEN NGÔÏI', 'KHEN NGỢI')
    text = text.replace('TOÅNG TRÌ', 'TỔNG TRÌ')
    text = text.replace('HOÄI THÖÙ 3', 'HỘI THỨ BA')
    text = text.replace('HỘI THỨ 3', 'HỘI THỨ BA')
    text = text.replace('THANH TÒNH', 'THANH TỊNH')
    text = text.replace('KHOÂNG NEÂU CÔØ', 'KHÔNG NÊU CỜ')
    text = text.replace('BAÁT KHAÛ ÑAÉC', 'BẤT KHẢ ĐẮC')
    text = text.replace('PHÖÔNG ÑOÂNG BAÉC', 'PHƯƠNG ĐÔNG BẮC')
    text = text.replace('KHOÂNG HOØA HÔÏP', 'KHÔNG HÒA HỢP')
    text = text.replace('CHÆ TÖÔÙNG', 'CHỈ TƯỚNG')
    text = text.replace('THAØNH BIEÄN', 'THÀNH BIỆN')
    text = text.replace('THUYEÀN ÑAÚNG DUÏ', 'THUYỀN ĐẲNG DỤ')
    text = text.replace('SÔ NGHIEÄP', 'SƠ NGHIỆP')
    text = text.replace('ÑIEÀU PHUÏC THAM ÑAÚNG', 'ĐIỀU PHỤC THAM ĐẲNG')
    text = text.replace('CHUYEÅN BAÁT CHUYEÅN', 'CHUYỂN BẤT CHUYỂN')
    text = text.replace('MOÄNG HAØNH', 'MỘNG HÀNH')
    text = text.replace('CAÊN-GIAØ THIEÂN', 'CĂNG-GIÀ THIÊN')
    text = text.replace('TAÄP CAÄN', 'TẬP CẬN')
    text = text.replace('ÑOÀNG HOÏC', 'ĐỒNG HỌC')
    text = text.replace('ÑOÀNG TAÙNH', 'ĐỒNG TÁNH')
    text = text.replace('KHOÂNG PHAÂN BIEÄT', 'KHÔNG PHÂN BIỆT')
    text = text.replace('KIEÂN COÁ CHAÚNG KIEÂN COÁ', 'KIÊN CỐ CHẲNG KIÊN CỐ')
    text = text.replace('THAÄT NGÖÕ', 'THẬT NGỮ')
    text = text.replace('TÖÔNG NHIEÁP', 'TƯƠNG NHIẾP')
    text = text.replace('THOÏ DUÏ', 'THỌ DỤ')
    text = text.replace('BOÀ-TAÙT HAÏNH', 'BỒ-TÁT HẠNH')
    text = text.replace('THAÂN CAÄN', 'THÂN CẬN')
    text = text.replace('HOÏC TAÁT CAÛ', 'HỌC TẤT CẢ')
    text = text.replace('TUAÀN TÖÏ', 'TUẦN TỰ')
    text = text.replace('VOÂ TÖÔÙNG', 'VÔ TƯỚNG')
    text = text.replace('KHOÂNG TAÏP', 'KHÔNG TẠP')
    text = text.replace('CAÙC ÑÖÙC TÖÔÙNG', 'CÁC ĐỨC TƯỚNG')
    text = text.replace('THIEÄN ÑAÏT', 'THIỆN ĐẠT')
    text = text.replace('THAÄT TEÁ', 'THẬT TẾ')
    text = text.replace('VOÂ KHUYEÁT', 'VÔ KHUYẾT')
    text = text.replace('ÑAÏO SÓ', 'ĐẠO SĨ')
    text = text.replace('CHAÙNH ÑÒNH', 'CHÁNH ĐỊNH')
    text = text.replace('PHAÄT PHAÙP', 'PHẬT PHÁP')
    text = text.replace('VOÂ SÖÏ', 'VÔ SỰ')
    text = text.replace('TAÙNH KHOÂNG', 'TÁNH KHÔNG')
    text = text.replace('XAÙ-LÔÏI TÖÛ', 'XÁ-LỢI TỬ')
    text = text.replace('THAØNH THUÏC HÖÕU TÌNH', 'THÀNH THỤC HỮU TÌNH')
    text = text.replace('NGHIEÂM TÒNH COÕI PHAÄT', 'NGHIÊM TỊNH CÕI PHẬT')
    text = text.replace('TÒNH ÑOÄ PHÖÔNG TIEÄN', 'TỊNH ĐỘ PHƯƠNG TIỆN')
    text = text.replace('VOÂ TAÙNH TÖÏ TAÙNH', 'VÔ TÁNH TỰ TÁNH')
    text = text.replace('THAÉNG NGHÓA DU-GIAØ', 'THẮNG NGHĨA DU-GIÀ')
    text = text.replace('PHAÙP TAÙNH VOÂ ÑOÄNG', 'PHÁP TÁNH VÔ ĐỘNG')
    text = text.replace('BOÀ-TAÙT THÖÔØNG ÑEÀ', 'BỒ-TÁT THƯỜNG ĐỀ')
    text = text.replace('BOÀ-TAÙT PHAÙP DUÕNG', 'BỒ-TÁT PHÁP DŨNG')
    text = text.replace('KEÁT KHUYEÁN', 'KẾT KHUYẾN')
    text = text.replace('HOAN HYÛ', 'HOAN HỶ')
    text = text.replace('QUAÙN CHIEÁU', 'QUÁN CHIẾU')
    text = text.replace('VOÂ ÑAÚNG ÑAÚNG', 'VÔ ĐẲNG ĐẲNG')
    text = text.replace('TÖÔÙNG THIEÄT CAÊN', 'TƯỚNG THIỆT CĂN')
    text = text.replace('THIEÄN HIEÄN', 'THIỆN HIỆN')
    text = text.replace('LY SANH', 'LY SANH')
    text = text.replace('THAÉNG QUAÂN', 'THẮNG QUÂN')
    text = text.replace('HAØNH TÖÔÙNG', 'HÀNH TƯỚNG')
    text = text.replace('HUYEÃN DUÏ', 'HUYỄN DỤ')
    text = text.replace('ÑOAÏN CHÖ KIEÁN', 'ĐOẠN CHƯ KIẾN')
    text = text.replace('LUÏC ÑAÙO BÆ NGAÏN', 'LỤC ĐÁO BỈ NGẠN')
    text = text.replace('NÖÔNG ÑAÏI THÖØA', 'NƯƠNG ĐẠI THỪA')
    text = text.replace('KHOÂNG BUOÄC, KHOÂNG MÔÛ', 'KHÔNG BUỘC, KHÔNG MỞ')
    text = text.replace('TAM-MA-ÑÒA', 'TAM-MA-ĐỊA')
    text = text.replace('NIEÄM TRUÏ ÑAÚNG', 'NIỆM TRỤ ĐẲNG')
    text = text.replace('TU TRÒ ÑÒA', 'TU TRỊ ĐỊA')
    text = text.replace('XUAÁT TRUÏ', 'XUẤT TRỤ')
    text = text.replace('SIEÂU THAÉNG', 'SIÊU THẮNG')
    text = text.replace('VOÂ SÔÛ HÖÕU', 'VÔ SỞ HỮU')
    text = text.replace('VOÂ BIEÂN TEÁ', 'VÔ BIÊN TẾ')
    text = text.replace('VIEÃN LY', 'VIỄN LY')
    text = text.replace('ÑEÁ THÍCH', 'ĐẾ THÍCH')
    text = text.replace('TÍN THOÏ', 'TÍN THỌ')
    text = text.replace('THOÏ KYÙ', 'THỌ KÝ')
    text = text.replace('BAÛO THAÙP', 'BẢO THÁP')
    text = text.replace('PHÖÔÙC SANH', 'PHƯỚC SANH')
    text = text.replace('COÂNG ÑÖÙC', 'CÔNG ĐỨC')
    text = text.replace('NGOAÏI ÑAÏO', 'NGOẠI ĐẠO')
    text = text.replace('TRÔØI ÑEÁN', 'TRỜI ĐẾN')
    text = text.replace('THIEÁT-LÔÏI-LA', 'THIẾT-LỢI-LA')
    text = text.replace('KINH VAÊN', 'KINH VĂN')
    text = text.replace('TUYØ HYÛ HOÀI HÖÔÙNG', 'TÙY HỶ HỒI HƯỚNG')
    text = text.replace('ÑAÏI SÖ', 'ĐẠI SƯ')
    text = text.replace('ÑÒA NGUÏC', 'ĐỊA NGỤC')
    text = text.replace('HOÏC PHÖÔNG TIEÄN THIEÄN XAÛO', 'HỌC PHƯƠNG TIỆN THIỆN XẢO')
    text = text.replace('NGUYEÄN DUÏ', 'NGUYỆN DỤ')
    text = text.replace('KHEN TAÙNH CHAÉC THAÄT', 'KHEN TÁNH CHẮC THẬT')
    text = text.replace('CHUÙC LUÏY', 'CHÚC LỤY')
    text = text.replace('VOÂ TAÄN', 'VÔ TẬN')
    text = text.replace('DAÃN NHIEÁP NHAU', 'DẪN NHIẾP NHAU')
    text = text.replace('ÑA VAÁN BAÁT NHÒ', 'ĐA VẤN BẤT NHỊ')
    text = text.replace('NOÙI THAÄT', 'NÓI THẬT')
    text = text.replace('XAÛO TIEÄN HAØNH', 'XẢO TIỆN HÀNH')
    text = text.replace('HOÏC ÑAÏO KHAÉP', 'HỌC ĐẠO KHẮP')
    text = text.replace('VOÂ TÖÔÙNG VOÂ ÑAÉC', 'VÔ TƯỚNG VÔ ĐẮC')
    text = text.replace('PHAÙP NGHÓA VOÂ TAÏP', 'PHÁP NGHĨA VÔ TẠP')
    text = text.replace('TÖÔÙNG CAÙC COÂNG ÑÖÙC', 'TƯỚNG CÁC CÔNG ĐỨC')
    text = text.replace('CAÙC PHAÙP BÌNH ÑAÚNG', 'CÁC PHÁP BÌNH ĐẲNG')
    text = text.replace('BAÁT KHAÛ ÑOÄNG', 'BẤT KHẢ ĐỘNG')
    text = text.replace('KHEN NGÔÏI THANH TÒNH', 'KHEN NGỢI THANH TỊNH')
    text = text.replace('TRÖÔÙC VAØ CHAÚNG TRÖÔÙC TÖÔÙNG', 'TRƯỚC VÀ CHẲNG TRƯỚC TƯỚNG')
    text = text.replace('TRÖÔÙC VAØ KHOÂNG TRÖÔÙC TÖÔÙNG', 'TRƯỚC VÀ KHÔNG TRƯỚC TƯỚNG')
    text = text.replace('TRÖÔÙC VAØ', 'TRƯỚC VÀ CHẲNG TRƯỚC TƯỚNG')
    text = text.replace('NOÙI TÖÔÙNG BAÙT-NHAÕ', 'NÓI TƯỚNG BÁT-NHÃ')
    text = text.replace('BA-LA-MAÄT-ÑA', 'BA-LA-MẬT-ĐA')
    text = text.replace('KHOÙ NGHE COÂNG ÑÖÙC', 'KHÓ NGHE CÔNG ĐỨC')
    text = text.replace('MA SÖÏ', 'MA SỰ')
    text = text.replace('PHAÄT MAÃU', 'PHẬT MẪU')
    text = text.replace('CHAÚNG NGHÓ BAØN', 'CHẲNG NGHĨ BÀN')
    text = text.replace('BIEÄN SÖÏ', 'BIỆN SỰ')
    text = text.replace('CHUÙNG DUÏ', 'CHÚNG DỤ')
    text = text.replace('CHÔN THIEÄN HÖÕU', 'CHƠN THIỆN HỮU')
    text = text.replace('TRÍ HÖÔÙNG ÑEÁN', 'TRÍ HƯỚNG ĐẾN')
    text = text.replace('CHÔN NHÖ', 'CHƠN NHƯ')
    text = text.replace('BOÀ-TAÙT AN TRUÏ', 'BỒ-TÁT AN TRỤ')
    text = text.replace('BAÁT THOÁI CHUYEÅN', 'BẤT THỐI CHUYỂN')
    text = text.replace('PHÖÔNG TIEÄN THIEÄN XAÛO', 'PHƯƠNG TIỆN THIỆN XẢO')
    text = text.replace('HAÏNH NGUYEÄN', 'HẠNH NGUYỆN')
    text = text.replace('CAÊNG-GIAØ-THIEÂN', 'CĂNG-GIÀ-THIÊN')
    text = text.replace('KHEÙO HOÏC', 'KHÉO HỌC')
    text = text.replace('ÑOAÏN PHAÂN BIEÄT', 'ĐOẠN PHÂN BIỆT')
    text = text.replace('PHAÅM TUØY HYÛ HOÀI HÖÔÙNG', 'PHẨM TÙY HỶ HỒI HƯỚNG')
    text = text.replace('TUØY HYÛ HOÀI HÖÔÙNG', 'TÙY HỶ HỒI HƯỚNG')
    text = text.replace('KHEN BAÙT-NHAÕ', 'KHEN NGỢI BÁT-NHÃ')
    text = text.replace('HUÛY BAÙNG BAÙT-NHAÕ', 'HỦY BÁNG BÁT-NHÃ')
    text = text.replace('KHOÙ TIN HIEÅU', 'KHÓ TIN HIỂU')
    text = text.replace('PHAÅM', 'PHẨM')
    text = text.replace('AÙO GIAÙP ÑAÏI-THÖØA', 'ÁO GIÁP ĐẠI-THỪA')
    text = text.replace('BIEÄN ÑAÏI-THÖØA', 'BIỆN ĐẠI-THỪA')
    text = text.replace('TAÙN ÑAÏI-THÖØA', 'TÁN ĐẠI-THỪA')
    text = text.replace('TUØY THUAÄN', 'TÙY THUẬN')
    text = text.replace('VOÂ SÔÛ ÑAÉC', 'VÔ SỞ ĐẮC')
    text = text.replace('QUAÙN HAÏNH', 'QUÁN HẠNH')
    text = text.replace('VOÂ SANH', 'VÔ SANH')
    text = text.replace('TÒNH ÑAÏO', 'TỊNH ĐẠO')
    text = text.replace('THIEÂN ÑEÁ', 'THIÊN ĐẾ')
    text = text.replace('CHÖ THIEÂN TÖÛ', 'CHƯ THIÊN TỬ')
    text = text.replace('THOÏ GIAÙO', 'THỌ GIÁO')
    text = text.replace('TAÙN HOA', 'TÁN HOA')
    text = text.replace('HOÏC BAÙT-NHAÕ', 'HỌC BÁT-NHÃ')
    text = text.replace('CAÀU BAÙT-NHAÕ', 'CẦU BÁT-NHÃ')
    text = text.replace('CAÀU BAÙT NHAÕ', 'CẦU BÁT-NHÃ')
    text = text.replace('THAÙN CHUÙNG COÂNG ÑÖÙC', 'THÁN CHÚNG CÔNG ĐỨC')
    text = text.replace('NHIEÁP THOÏ', 'NHIẾP THỌ')
    text = text.replace('SO SAÙNH COÂNG ÑÖÙC', 'SO SÁNH CÔNG ĐỨC')
    text = text.replace('MA-HA-TAÙT', 'MA-HA-TÁT')
    text = text.replace('BOÀ-TAÙT', 'BỒ-TÁT')
    text = text.replace('THÍ DUÏ', 'THÍ DỤ')
    text = text.replace('BAÙT NHAÕ HAØNH TÖÔÙNG', 'BÁT NHÃ HÀNH TƯỚNG')
    text = text.replace('VOÂ TRUÏ', 'VÔ TRỤ')
    text = text.replace('KHUYEÂN HOÏC', 'KHUYÊN HỌC')
    text = text.replace('DAÏY BAÛO TRAO TRUYEÀN', 'DẠY BẢO TRAO TRUYỀN')
    text = text.replace('HIEÄN TÖÔÙNG LÖÔÕI', 'HIỆN TƯỚNG LƯỠI')
    text = text.replace('KHEN NGÔÏI THAÉNG ÑÖÙC', 'KHEN NGỢI THẮNG ĐỨC')
    text = text.replace('CHUYEÅN SANH', 'CHUYỂN SANH')
    text = text.replace('TÖÔNG ÖNG', 'TƯƠNG ƯNG')
    text = text.replace('HOÏC QUAÙN', 'HỌC QUÁN')
    text = text.replace('DUYEÂN KHÔÛI', 'DUYÊN KHỞI')
    text = text.replace('ÑAÏI-THÖØA', 'ĐẠI-THỪA')
    text = text.replace('ÑAÏI THÖØA', 'ĐẠI THỪA')
    text = text.replace('Ñaïi-thöøa', 'Đại-thừa')
    text = text.replace('Ðại-thừa', 'Đại-thừa')
    
    # Abbreviations
    text = re.sub(r'([^\s])v\.[ \t]*v', r'\1 v.v', text)
    text = re.sub(r'\bv\.[ \t]+v\b', 'v.v', text)
    text = re.sub(r'\bv\.[ \t]*v\b', 'v.v', text)
    text = text.replace('HOÄI THÖÙ 2', 'HỘI THỨ HAI')
    text = text.replace('HOÄI THÖÙ', 'HỘI THỨ')
    text = text.replace('HỘI THỨ 2', 'HỘI THỨ HAI')
    
    # Honorifics
    text = re.sub(r'\bnhư Lai\b', 'Như Lai', text)
    text = re.sub(r'\bthế Tôn\b', 'Thế Tôn', text)
    
    # Space before punctuation
    text = re.sub(r'([^\s]+)\s+([.,;:!?])', r'\1\2', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

para_starters = [
    'Lúc bấy giờ', 'Khi ấy', 'Cứ như vậy', 'Cứ như thế', 'Lại nữa,', 'Lại nữa, Xá Lợi Tử!',
    'Xá Lợi Tử!', 'Các đại Bồ-tát', 'Nếu đại Bồ-tát', 'Phật bảo', 'Đức Phật',
    'Có khả năng biết như thật', 'Lại nữa, Thiện Hiện!', 'Thiện Hiện!',
    'Cụ thọ Thiện Hiện', 'Thiện Hiện bạch', 'Bạch Thế Tôn!', 'Xá Lợi Tử bạch',
    'Lại có', 'Đức Thế Tôn', 'Phật nhận hoa', 'Bồ-tát đứng đầu', 'Các vị Bồ-tát',
    'Mỗi vị đứng đầu', 'Khi đến chỗ', 'Đức Phật liền lấy'
]

def summarize_page_content(page_lines):
    text = ' '.join(page_lines)
    text = clean_vietnamese_text(text)
    sentences = re.split(r'[.!?:]\s+', text)
    for s in sentences:
        s = s.strip()
        if len(s) > 30 and not any(k in s for k in ['Kinh Đại Bát Nhã', 'Tập 01', 'Quyển', 'HEÁT', 'Hết']):
            s_clean = s.replace('|', '-').strip()
            s_clean = re.sub(r'^[;,:\s]+', '', s_clean)
            if len(s_clean) > 110:
                s_clean = s_clean[:105].rsplit(' ', 1)[0].rstrip(' ,;:') + '...'
            return s_clean
    return 'Kinh văn Bát-nhã-ba-la-mật-đa'

def validate_quality_gates(file_path, quyen_num):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    errors = []

    # Gate 1: Encoding
    for vni in ['öø', 'ñôøi', 'thöøa', 'baùt', 'nhaõ', 'quyeån', 'thöù']:
        if vni in text.lower():
            errors.append(f'Gate 1 Error: Found raw VNI "{vni}"')

    # Gate 2: Syllable integrity
    clean_t = re.sub(r'\bv\.[ \t]*v[\.…]*', '', text)
    clean_t = re.sub(r'\bv\.v[\.…]*', '', clean_t)
    # Strip Roman numerals before punctuation/space (e.g. 'V. PHẨM')
    clean_t = re.sub(r'\b[IVXLCDM]+\b\.?', '', clean_t)
    single_c = re.findall(r'\b[bcdđghklmnpqrstvx]\b', clean_t, re.IGNORECASE)
    if single_c:
        errors.append(f'Gate 2 Error: Found single consonant letters: {set(single_c)}')

    if 'phậ tở' in text.lower() or 'lạ cở' in text.lower():
        errors.append('Gate 2 Error: Found merged prepositions (phậ tở / lạ cở)')

    # Gate 3: Orthography
    if 'nguời' in text or 'ngu ời' in text:
        errors.append('Gate 3 Error: Found un-horned nguời')
    if 'phàp mầu' in text:
        errors.append('Gate 3 Error: Found phàp mầu')

    # Gate 4: Buddhist terminology
    if re.search(r'\bnhư Lai\b', text):
        errors.append('Gate 4 Error: Found uncapitalized "như Lai"')
    if 'bồ -tát' in text.lower():
        errors.append('Gate 4 Error: Found space in hyphen "Bồ -tát"')

    # Gate 5: Typography
    space_before_punct = re.findall(r'\w\s+[.,;:!?]', text)
    if space_before_punct:
        errors.append(f'Gate 5 Error: Found spaces before punctuation: {space_before_punct[:5]}')

    body_idx = text.find('### NỘI DUNG KINH VĂN')
    if 'Kinh Đại Bát Nhã Ba La Mật Đa' in text[body_idx + 30:]:
        errors.append('Gate 5 Error: Found running header in text body')

    # Gate 6: Structural
    end_marker = f'**QUYỂN THỨ {quyen_num:02d} (HẾT)**'
    if end_marker not in text:
        errors.append(f'Gate 6 Error: Missing ending marker {end_marker}')

    return errors

def process_quyen(reader, tap_num, quyen_num, pdf_start, pdf_end, p_in_start, p_in_end, hoi_str, phan_str, pham_str, out_dir, tap_range_str=None, page_in_map=None):
    all_lines = []
    page_summaries = [] # (p_in, p_pdf, summary)

    for p in range(pdf_start, pdf_end + 1):
        raw = reader.pages[p-1].extract_text() or ''
        raw_lines = [l.strip() for l in raw.split('\n') if l.strip()]
        
        # Calculate printed page number
        if page_in_map and p in page_in_map:
            p_in = page_in_map[p]
        else:
            p_offset = p - pdf_start
            p_in = p_in_start + p_offset
        
        # Header/footer stripping
        if p == pdf_start:
            # Check if line 0 is section title or subnumber
            content_lines = []
            for l in raw_lines:
                if re.match(r'^\d+$', l) or 'PHAÅM' in l or 'PHẨM' in l or 'HOÄI THÖÙ' in l or 'HỘI THỨ' in l or 'PHAÀN' in l or 'PHẦN' in l:
                    continue
                content_lines.append(l)
        elif p == pdf_end:
            # Last page has header, page num, content, end marker
            first = 1 if ('Kinh Đại Bát Nhã' in raw_lines[0] or f'Quyển {quyen_num:02d}' in raw_lines[0] or 'Tập' in raw_lines[0]) else 0
            sub = raw_lines[first:]
            if sub and re.match(r'^\d+$', sub[0]):
                sub = sub[1:]
            # filter out ending tags and trailing page numbers
            content_lines = [l for l in sub if not (any(k in l.lower() for k in ['quyeån', 'quyển', 'hết', 'heát']) and len(l) < 25) and not re.match(r'^\d+$', l)]
        else:
            first = 1 if ('Kinh Đại Bát Nhã' in raw_lines[0] or f'Quyển {quyen_num:02d}' in raw_lines[0] or 'Tập' in raw_lines[0]) else 0
            last = len(raw_lines) - 1 if re.match(r'^\d+$', raw_lines[-1]) else len(raw_lines)
            content_lines = raw_lines[first:last]
            # also check if first line is a page number
            if content_lines and re.match(r'^\d+$', content_lines[0]):
                content_lines = content_lines[1:]

        # Check for intermediate Phẩm heading inside this page
        for l in raw_lines:
            if 'PHAÅM' in l or 'PHẨM' in l:
                clean_h = clean_vietnamese_text(l)
                if clean_h.startswith('### '):
                    all_lines.append(clean_h)
                elif re.match(r'^[I|V|X]+\.', clean_h):
                    all_lines.append(f'### {clean_h}')

        # Clean lines
        cleaned_page = [clean_vietnamese_text(cl) for cl in content_lines if cl.strip()]
        page_summary = summarize_page_content(cleaned_page)
        page_summaries.append((p_in, p, page_summary))
        all_lines.extend(cleaned_page)

    # Assemble paragraphs
    paragraphs = []
    cur_p = []

    for idx, line in enumerate(all_lines):
        if line.startswith('### '):
            if cur_p:
                joined = ' '.join(cur_p)
                paragraphs.append(clean_vietnamese_text(joined))
                cur_p = []
            paragraphs.append(line)
            continue

        cur_p.append(line)
        is_end = False
        is_sentence_end = any(line.endswith(p) for p in ['.', ':', '!', '?', '.”', '?”', '!”'])
        if idx == len(all_lines) - 1:
            is_end = True
        else:
            next_l = all_lines[idx+1]
            if is_sentence_end and (len(line) < 55 or any(next_l.startswith(ps) for ps in para_starters) or next_l.startswith('### ')):
                is_end = True
                
        if is_end:
            joined = ''
            for piece in cur_p:
                if not joined:
                    joined = piece
                elif joined.endswith('-'):
                    joined = joined + piece
                else:
                    joined = joined + ' ' + piece
            joined = clean_vietnamese_text(joined)
            if joined.strip():
                paragraphs.append(joined)
            cur_p = []

    # Build Markdown document
    doc = []
    doc.append('# KINH ĐẠI BÁT NHÃ BA LA MẬT ĐA')
    if not tap_range_str:
        tap_range_str = f'TỪ QUYỂN {quyen_num:02d} ĐẾN QUYỂN ...'
    doc.append(f'## TẬP {tap_num:02d}: {tap_range_str}')
    doc.append('')
    doc.append('* **Hán dịch:** Tam Tạng Pháp Sư Huyền Trang')
    doc.append('* **Việt dịch:** Hòa Thượng Thích Trí Nghiêm (Chùa Long Sơn, Nha Trang)')
    doc.append('* **Giảo chính:** Hòa Thượng Thích Quảng Độ')
    doc.append('* **Ấn hành:** Ban Bảo Trợ Phiên Dịch Pháp Tạng Phật Giáo Việt Nam Tại Hoa Kỳ (PL. 2547 – DL. 2003)')
    doc.append('')
    doc.append('---')
    doc.append('')
    doc.append(f'### {hoi_str}')
    if phan_str:
        doc.append(f'#### {phan_str}')
    doc.append(f'##### {pham_str}')
    doc.append(f'###### QUYỂN THỨ {quyen_num:02d}')
    doc.append('')
    doc.append(f'*(Phạm vi văn bản: Trang bản in {p_in_start} – {p_in_end} | Trang PDF {pdf_start} – {pdf_end})*')
    doc.append('')
    doc.append('---')
    doc.append('')
    doc.append('### BẢNG ĐỐI CHIẾU TRANG NGUYÊN BẢN (PAGE INDEX)')
    doc.append('')
    doc.append('| Trang bản in | Trang PDF | Nội dung chính |')
    doc.append('| :---: | :---: | :--- |')
    for p_in, p_pdf, s_text in page_summaries:
        doc.append(f'| **{p_in}** | {p_pdf} | {s_text} |')
    doc.append('')
    doc.append('---')
    doc.append('')
    doc.append('### NỘI DUNG KINH VĂN')
    doc.append('')

    for p in paragraphs:
        doc.append(p)
        doc.append('')

    doc.append('---')
    doc.append('')
    doc.append(f'**QUYỂN THỨ {quyen_num:02d} (HẾT)**')
    doc.append('')

    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f'Tap_{tap_num:02d}_Quyen_{quyen_num:02d}.md')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(doc))

    # Validate Quality Gates
    errors = validate_quality_gates(out_file, quyen_num)
    if errors:
        print(f'[FAIL] Quyển {quyen_num:02d}: {len(errors)} defects found!')
        for e in errors:
            print(f'   - {e}')
        return False
    else:
        size = os.path.getsize(out_file)
        print(f'[PASS] Quyển {quyen_num:02d}: 100% Quality Gates Passed! ({size:,} bytes | {len(paragraphs)} paras | {len(page_summaries)} pages)')
        return True
