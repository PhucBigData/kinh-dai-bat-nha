import glob
import re
import os
import sys

concrete_pairs = [
    # ho + ặc -> hoặc
    (r'\b(h|H)o[ \t]+ặc\b', r'\1oặc'),
    # thi + ện -> thiện
    (r'\b(t|T)hi[ \t]+ện\b', r'\1hiện'),
    # ti + ện -> tiện
    (r'\b(t|T)i[ \t]+ện\b', r'\1iện'),
    # hi + ện -> hiện
    (r'\b(h|H)i[ \t]+ện\b', r'\1iện'),
    # ngo + ại -> ngoại
    (r'\b(n|N)go[ \t]+ại\b', r'\1goại'),
    # nguy + ện -> nguyện
    (r'\b(n|N)guy[ \t]+ện\b', r'\1guyện'),
    # lo + ại -> loại
    (r'\b(l|L)o[ \t]+ại\b', r'\1oại'),
    # hi + ểu -> hiểu
    (r'\b(h|H)i[ \t]+ểu\b', r'\1iểu'),
    # xu + ất -> xuất
    (r'\b(x|X)u[ \t]+ất\b', r'\1uất'),
    # ho + ại -> hoại
    (r'\b(h|H)o[ \t]+ại\b', r'\1oại'),
    # nghi + ệp -> nghiệp
    (r'\b(n|N)ghi[ \t]+ệp\b', r'\1ghiệp'),
    # kho + ảng -> khoảng
    (r'\b(k|K)ho[ \t]+ảng\b', r'\1hoảng'),
    # hi + ệp -> hiệp
    (r'\b(h|H)i[ \t]+ệp\b', r'\1iệp'),
    # bi + ện -> biện
    (r'\b(b|B)i[ \t]+ện\b', r'\1iện'),
    # bi + ển -> biển
    (r'\b(b|B)i[ \t]+ển\b', r'\1iển'),
    # nhi + ễu -> nhiễu
    (r'\b(n|N)hi[ \t]+ễu\b', r'\1hiễu'),
    # chuy + ển -> chuyển
    (r'\b(c|C)huy[ \t]+ển\b', r'\1huyển'),
    # tri + ển -> triển
    (r'\b(t|T)ri[ \t]+ển\b', r'\1riển'),
    # ti + ểu -> tiểu
    (r'\b(t|T)i[ \t]+ểu\b', r'\1iểu'),
    # lu + ận -> luận
    (r'\b(l|L)u[ \t]+ận\b', r'\1uận'),
    # thu + ận -> thuận
    (r'\b(t|T)hu[ \t]+ận\b', r'\1huận'),
    # lo + ạn -> loạn
    (r'\b(l|L)o[ \t]+ạn\b', r'\1oạn'),
    # thi + ểu -> thiểu
    (r'\b(t|T)hi[ \t]+ểu\b', r'\1hiểu'),
    # khu + ất -> khuất
    (r'\b(k|K)hu[ \t]+ất\b', r'\1huất'),
    # chu + ẩn -> chuẩn
    (r'\b(c|C)hu[ \t]+ẩn\b', r'\1huẩn'),
    # duy + ệt -> duyệt
    (r'\b(d|D)uy[ \t]+ệt\b', r'\1uyệt'),
    # thuy + ết -> thuyết
    (r'\b(t|T)huy[ \t]+ết\b', r'\1huyết'),
    # quy + ết -> quyết
    (r'\b(q|Q)uy[ \t]+ết\b', r'\1uyết'),
    # tuy + ệt -> tuyệt
    (r'\b(t|T)uy[ \t]+ệt\b', r'\1uyệt'),
    # nghĩ + a -> nghĩa
    (r'\b(n|N)ghĩ[ \t]+a\b', r'\1ghĩa'),
    (r'\bthiệ[ \t]+n\b', 'thiện'),
    (r'\bThiệ[ \t]+n\b', 'Thiện'),
]

compiled_pairs = [(re.compile(pat), repl) for pat, repl in concrete_pairs]

files = sorted(glob.glob('Tap_0[1-5]/*.md'))
print(f"Total files to process: {len(files)}")

total_modifications = 0
files_modified = 0

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()
    
    modified = original
    
    # Text replacements for OCR artifacts
    modified = modified.replace('Thiệ nHi ện', 'Thiện Hiện')
    modified = re.sub(r'\b[ðÐ][ \t]+ại\b', 'Đại', modified)
    modified = re.sub(r'\b[ðÐ][ \t]+ộc\b', 'độc', modified)
    modified = modified.replace('Ðại', 'Đại')
    modified = modified.replace('Ð ại', 'Đại')
    
    for regex, repl in compiled_pairs:
        modified = regex.sub(repl, modified)
    
    if modified != original:
        diff_count = len(original) - len(modified)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(modified)
        files_modified += 1
        total_modifications += 1

print(f"Done! Modified {files_modified}/{len(files)} files.")
