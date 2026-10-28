import os
import glob
import json
import re

out_dir = 'reader/data'
os.makedirs(out_dir, exist_ok=True)

hoi_definitions = [
    (1, 'Hội thứ nhất: Hội đầu', 1, 400, 'Hội đầu gồm 79 Phẩm (Quyển 001 đến Quyển 400), thuyết tại núi Thứu Phong thành Vương Xá và vườn Cấp Cô Độc thành Thất-la-phiệt.'),
    (2, 'Hội thứ hai', 401, 478, 'Hội thứ hai gồm 85 Phẩm (Quyển 401 đến Quyển 478), thuyết tại núi Thứu Phong thành Vương Xá.'),
    (3, 'Hội thứ ba', 479, 537, 'Hội thứ ba gồm 31 Phẩm (Quyển 479 đến Quyển 537), thuyết tại núi Thứu Phong thành Vương Xá.'),
    (4, 'Hội thứ tư', 538, 555, 'Hội thứ tư gồm 29 Phẩm (Quyển 538 đến Quyển 555), thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc.'),
    (5, 'Hội thứ năm', 556, 565, 'Hội thứ năm gồm 24 Phẩm (Quyển 556 đến Quyển 565), thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc.'),
    (6, 'Hội thứ sáu', 566, 573, 'Hội thứ sáu gồm 17 Phẩm (Quyển 566 đến Quyển 573), thuyết tại bờ hồ Định sanh thành Vương Xá.'),
    (7, 'Hội thứ bảy: Phần Mạn-Thù-Thất-Lợi', 574, 575, 'Hội thứ bảy thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc.'),
    (8, 'Hội thứ tám: Phần Na-Già-Thất-Lợi', 576, 576, 'Hội thứ tám thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc.'),
    (9, 'Hội thứ chín: Phần Kim Cương Năng Đoạn', 577, 577, 'Hội thứ chín thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc (Kinh Kim Cương Bát Nhã).'),
    (10, 'Hội thứ mười: Phần Lý Thú Bát-Nhã', 578, 578, 'Hội thứ mười thuyết tại cung trời Tha Hóa Tự Tại.'),
    (11, 'Hội thứ mười một: Phần Bố Thí Ba-La-Mật-Đa', 579, 583, 'Hội thứ mười một thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc.'),
    (12, 'Hội thứ mười hai: Phần Tịnh Giới Ba-La-Mật-Đa', 584, 588, 'Hội thứ mười hai thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc.'),
    (13, 'Hội thứ mười ba: Phần An Nhẫn Ba-La-Mật-Đa', 589, 589, 'Hội thứ mười ba thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc.'),
    (14, 'Hội thứ mười bốn: Phần Tinh Tấn Ba-La-Mật-Đa', 590, 590, 'Hội thứ mười bốn thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc.'),
    (15, 'Hội thứ mười lăm: Phần Tĩnh Lự Ba-La-Mật-Đa', 591, 592, 'Hội thứ mười lăm thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc.'),
    (16, 'Hội thứ mười sáu: Phần Bát-Nhã Ba-La-Mật-Đa', 593, 600, 'Hội thứ mười sáu thuyết tại rừng cây Thệ-đa vườn Cấp Cô Độc (Viên mãn Đại Tạng Bát Nhã).')
]

hoi_meta_list = []
for h_id, name, q_s, q_e, desc in hoi_definitions:
    hoi_meta_list.append({
        'id': h_id,
        'name': name,
        'quyen_start': q_s,
        'quyen_end': q_e,
        'count': q_e - q_s + 1,
        'description': desc
    })

quyen_list = []

for tap in range(1, 12):
    pattern = f'Tap_{tap:02d}/Tap_{tap:02d}_Quyen_*.md'
    files = sorted(glob.glob(pattern))
    for fpath in files:
        fname = os.path.basename(fpath)
        q_num = int(fname.split('_Quyen_')[1].split('.md')[0])

        with open(fpath, 'r', encoding='utf-8') as f:
            text = f.read()

        m_hoi = re.search(r'### (HỘI [^\n]+)', text)
        m_phan = re.search(r'#### (PHẦN [^\n]+)', text)
        m_pham = re.search(r'##### ([^\n]+)', text)
        m_range = re.search(r'Trang bản in (\d+)\s*–\s*(\d+)\s*\|\s*Trang PDF (\d+)\s*–\s*(\d+)', text)

        hoi_str = m_hoi.group(1).strip() if m_hoi else 'HỘI THỨ NHẤT'
        phan_str = m_phan.group(1).strip() if m_phan else ''
        pham_str = m_pham.group(1).strip() if m_pham else ''

        if m_range:
            p_in = f'{m_range.group(1)} – {m_range.group(2)}'
            p_pdf = f'{m_range.group(3)} – {m_range.group(4)}'
        else:
            p_in = ''
            p_pdf = ''

        # Map to which Hoi ID (1 to 16)
        hoi_id = 1
        for h_meta in hoi_meta_list:
            if h_meta['quyen_start'] <= q_num <= h_meta['quyen_end']:
                hoi_id = h_meta['id']
                break

        quyen_list.append({
            'quyen': q_num,
            'tap': tap,
            'hoi_id': hoi_id,
            'hoi': hoi_str,
            'phan': phan_str,
            'pham': pham_str,
            'p_in': p_in,
            'p_pdf': p_pdf,
            'file': f'../Tap_{tap:02d}/{fname}'
        })

quyen_list.sort(key=lambda x: x['quyen'])

toc_data = {
    'title': 'Kinh Đại Bát Nhã Ba La Mật Đa',
    'total_quyen': len(quyen_list),
    'total_tap': 11,
    'total_hoi': 16,
    'translator_han': 'Tam Tạng Pháp Sư Huyền Trang',
    'translator_viet': 'Trưởng Lão Hòa Thượng Thích Trí Nghiêm',
    'proofreader': 'Hòa Thượng Thích Quảng Độ',
    'publisher': 'Ban Bảo Trợ Phiên Dịch Pháp Tạng Phật Giáo Việt Nam Tại Hoa Kỳ (PL. 2547 – DL. 2003)',
    'hoi_list': hoi_meta_list,
    'quyen_list': quyen_list
}

out_file = os.path.join(out_dir, 'toc.json')
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(toc_data, f, ensure_ascii=False, indent=2)

print(f'Successfully built {out_file}: {len(quyen_list)} Quyển indexed across {len(hoi_meta_list)} Hội!')
