# BLUEPRINT & CHECKLIST RÀ SOÁT CHẤT LƯỢNG SỐ HÓA
# BỘ KINH ĐẠI BÁT NHÃ BA LA MẬT ĐA (600 QUYỂN)

> **Tài liệu tham chiếu chuẩn (SSOT - Single Source of Truth)**
> * **Nguyên bản:** 11 tập PDF (10.454 trang) – Ban Bảo Trợ Phiên Dịch Pháp Tạng Phật Giáo Việt Nam Tại Hoa Kỳ (PL. 2547 – DL. 2003).
> * **Dịch giả:** Hán dịch: Tam Tạng Pháp Sư Huyền Trang | Việt dịch: Trưởng Lão Hòa Thượng Thích Trí Nghiêm | Giảo chính: Hòa Thượng Thích Quảng Độ.

---

## PHẦN I: BLUEPRINT (KIẾN TRÚC & QUY CHUẨN KỸ THUẬT)

### 1. Kiến trúc xử lý 5 tầng (5-Layer Processing Pipeline)

```
[ PDF Gốc (11 Tập / 10.454 trang) ]
               │
               ▼
┌────────────────────────────────────────────────────────┐
│ Tầng 1: PDF Parsing & Stream Extraction                │
│  - Trích xuất text stream, font resource (/BaseFont),  │
│    và ma trận tọa độ glyph (x, y) qua pypdf visitor.   │
└────────────────────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────┐
│ Tầng 2: De-spacing & Font Boundary Reconstruction      │
│  - Khử khoảng trắng nhân tạo do lỗi kerning/overlay.   │
│  - Nối phụ âm đầu + nguyên âm (th ời → thời).          │
│  - Nối nguyên âm + âm cuối (gồ m → gồm, mộ t → một).   │
│  - Khử phân rã vần đôi/ba (chi ếu → chiếu, khu ỷu).    │
└────────────────────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────┐
│ Tầng 3: Header/Footer Stripping & Page Seam Stitching  │
│  - Loại bỏ 100% running header & số trang lẻ footer.   │
│  - Nối câu xuyên trang mượt mà (không ngắt vụn đoạn).  │
│  - Bảo toàn gạch nối danh xưng phiên âm (Bồ-tát).      │
└────────────────────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────┐
│ Tầng 4: Typographical Normalization & Honorifics       │
│  - Viết hoa tôn kính: "Như Lai", "Thế Tôn", chư Bồ-tát.│
│  - Khử khoảng trắng trước dấu câu (spacing anomalies). │
│  - Khôi phục ký tự đồ họa đặc thù: chữ Đức (卍).       │
│  - Bảo lưu tuyệt đối từ ngữ cổ/đặc thù của bản dịch.   │
└────────────────────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────┐
│ Tầng 5: Structured Document Assembly & Page Indexing   │
│  - Phân đoạn chuẩn theo câu mở kinh & logic đối thoại. │
│  - Tạo Frontmatter metadata đầy đủ dịch giả/nguồn gốc. │
│  - Xây dựng Bảng đối chiếu trang (Page Index) chuẩn xác│
│    về cõi nước, tôn hiệu Phật, Bồ-tát đại diện.        │
└────────────────────────────────────────────────────────┘
               │
               ▼
[ File Markdown / JSON Hoàn Chỉnh Đạt Tiêu Chuẩn Xuất Bản ]
```

---

### 2. Quy chuẩn cấu trúc thư mục & đặt tên file

Toàn bộ 600 quyển được phân cấp theo 11 tập tương ứng 11 file PDF:

```text
Kinh Phật/
├── BLUEPRINT_AND_CHECKLIST.md       # Tài liệu này
├── Kinh Bát Nhã/                    # 11 file PDF nguyên bản (read-only)
│   ├── Kinh Đại Bát Nhã - Tập 01.PDF
│   └── ...
├── Tap_01/                          # Tập 01 (Quyển 01 – 50)
│   ├── Tap_01_Quyen_01.md
│   ├── Tap_01_Quyen_02.md
│   └── ... (đến Tap_01_Quyen_50.md)
├── Tap_02/                          # Tập 02 (Quyển 51 – 100)
│   └── ...
└── ...
└── Tap_11/                          # Tập 11 (Quyển 551 – 600)
    └── ...
```

* **Quy ước tên file:** `Tap_{TT}_Quyen_{QQ}.md` (ví dụ: `Tap_01_Quyen_01.md`).
* **Định dạng file:** Markdown tiêu chuẩn (UTF-8 không BOM), dùng LF (`\n`).

---

### 3. Quy chuẩn cấu trúc nội dung trong từng file Markdown

Mỗi file Markdown bắt buộc gồm 4 khối chuẩn:

1. **Khối 1: Tiêu đề & Frontmatter:**
   - Tên kinh: `# KINH ĐẠI BÁT NHÃ BA LA MẬT ĐA`
   - Số tập & khoảng quyển: `## TẬP XX: TỪ QUYỂN YY ĐẾN QUYỂN ZZ`
   - Thông tin Hán dịch, Việt dịch, Giảo chính, Năm ấn hành.
2. **Khối 2: Phân cấp Hội / Phần / Phẩm / Quyển:**
   - `### HỘI THỨ ...`
   - `#### PHẦN ...`
   - `##### I. PHẨM ...`
   - `###### QUYỂN THỨ ...`
   - Ghi chú phạm vi trang đối soát: `*(Phạm vi văn bản: Trang bản in A – B | Trang PDF C – D)*`
3. **Khối 3: Bảng đối chiếu trang nguyên bản (Page Index):**
   - Bảng Markdown gồm 3 cột: `| Trang bản in | Trang PDF | Nội dung chính |`.
   - Nội dung tóm tắt phải chuẩn xác 100% về: Tên cõi Phật, Tôn hiệu Đức Phật chủ cõi, Tên Bồ-tát phụng mạng, Hướng cúng dường.
4. **Khối 4: Thân kinh văn & Lời kết:**
   - Tiêu đề `### NỘI DUNG KINH VĂN`
   - Các đoạn văn tách nhau bằng đúng một dòng trống.
   - Kết thúc bằng đường phân cách `---` và dòng xác nhận: `**QUYỂN THỨ XX (HẾT)**`.

---

## PHẦN II: CHECKLIST RÀ SOÁT CHẤT LƯỢNG (6 QUALITY GATES)

Mỗi file sau khi xuất bản bắt buộc phải vượt qua 6 cổng kiểm định (đạt 100% tiêu chí mới được coi là hoàn tất):

### Gate 1: Bảng mã & Khử rác Font (Encoding Gate)
* [ ] **1.1. Chuẩn UTF-8:** Toàn bộ file lưu UTF-8 thuần, không có ký tự lỗi font chữ (mojibake).
* [ ] **1.2. Khử sạch mã VNI cũ:** Không sót bất kỳ chuỗi VNI nào (`ö, ø, ñ, ï, ê, ô, ä, ë, ü` trong `öø`, `ñôøi`, `thöøa`, `baùt nhaõ`).
* [ ] **1.3. Khôi phục đồ họa chữ Đức:** Thay thế khoảng trống `chữ Đức ( )` bằng biểu tượng chuẩn `chữ Đức (卍)`.

### Gate 2: Toàn vẹn âm tiết tiếng Việt (Syllable Integrity Gate)
* [ ] **2.1. Không còn chữ cái đơn lẻ:** Quét tự động regex xác nhận không còn phụ âm đơn đứng một mình (`b, c, d, đ, g, h, k, l, m, n, p, r, s, t, v, x`).
* [ ] **2.2. Không dính từ với giới từ:** Tuyệt đối không để dính phụ âm cuối vào giới từ `ở` (phải là `Phật ở`, `Cực Lạc ở`, `người ở`, không để `Phậ tở`, `Lạ cở`).
* [ ] **2.3. Không phân rã vần đôi/vần ba:** Các từ có nguyên âm đôi/ba phải liền mạch (`chiếu`, `khuỷu`, `biếng`, `diễn`, `niệm`, `phiền`, `nhiễm`, không để `chi ếu`, `khu ỷu`, `bi ếng`).
* [ ] **2.4. Không dính từ ghép song hành:** Các từ riêng lẻ đứng cạnh nhau không bị gộp sai (`Bửu Ấn` không thành `BửuẤn`, `tương ưng` không thành `tươngưng`, `trăm nghìn ức` không thành `nghìnức`, `mát êm ả` không thành `mátêmả`).

### Gate 3: Chính tả, Dấu thanh & Dấu phụ (Orthography Gate)
* [ ] **3.1. Đầy đủ dấu móc chữ ư:** 100% các từ `người`, `người điên`, `người nghe` có đủ dấu móc (không sót dạng `nguời`, `ngu ời`).
* [ ] **3.2. Chuẩn hóa dấu thanh:** Sửa các lỗi dấu thanh in sai của bản gốc (ví dụ: `pháp mầu`, không để `phàp mầu`).
* [ ] **3.3. Viết hoa đầu câu:** Viết hoa chữ cái đầu tiên sau dấu chấm (`. Lại có`, `. Khi ấy`, `. Lúc bấy giờ`).
* [ ] **3.4. Viết hoa sau dấu hai chấm mở kinh:** `Tôi nghe như vầy: Một thời nọ...` (viết hoa chữ `Một`).

### Gate 4: Quy chuẩn Danh xưng & Thuật ngữ Phật học (Buddhist Terminology Gate)
* [ ] **4.1. Tôn xưng Như Lai:** 100% viết hoa cả hai chữ `Như Lai` (không để `như Lai`).
* [ ] **4.2. Tôn xưng Thế Tôn:** 100% viết hoa trang nghiêm `Thế Tôn`.
* [ ] **4.3. Đồng bộ danh hiệu Bồ-tát:** Viết hoa đầy đủ các thành tố danh xưng (`Vô Chướng Tuệ`, `Thường Gia Hạnh`, `Từ Thị`, `Quán Tự Tại`, `Đắc Đại Thế`, `Diệu Cát Tường`...).
* [ ] **4.4. Chuẩn hóa gạch nối từ phiên âm:** Viết liền gạch nối không có khoảng trắng thừa: `Bồ-tát`, `Bí-sô`, `A-la-hán`, `Đà-la-ni`, `Tam-ma-địa`, `Bạt-già-phạm` (không để `Bồ -tát`).
* [ ] **4.5. Bảo lưu văn phong dịch giả:** Giữ nguyên các từ ngữ đặc thù do cố Hòa thượng Thích Trí Nghiêm dịch: `thân tâm thư thới`, `châu Đông thắng thần`, `chạm rất chạm, cùng chạm rất mạnh`, `xin giả từ`.

### Gate 5: Định dạng Dấu câu & Typography (Typography Gate)
* [ ] **5.1. Không có khoảng trắng trước dấu câu:** 0 khoảng trắng trước `,`, `.`, `;`, `:`, `!`, `?` (loại bỏ `họ ;`, `nách ,`, `sự .`, `Sư ,`).
* [ ] **5.2. Đủ khoảng trắng sau dấu câu:** Sau dấu phẩy, dấu chấm phải có một khoảng trắng cách từ tiếp theo (không để `dẳng,tháo`).
* [ ] **5.3. Chuẩn hóa dấu ba chấm:** Dùng `...` liền sau chữ hoặc có khoảng cách chuẩn (`Từ Thị... Vô lượng`).
* [ ] **5.4. Lọc sạch rác đầu và chân trang:** 100% running headers (`Kinh Đại Bát Nhã...`, `Tập 01, Quyển...`) và số trang lẻ footer bị loại bỏ.
* [ ] **5.5. Nối câu xuyên trang mượt mà:** Đoạn văn kéo dài qua nhiều trang PDF phải được ghép liền mạch, không bị đứt gãy câu hay chèn blockquote rác vào giữa câu.

### Gate 6: Kiểm chứng Chỉ mục & Toàn vẹn Cấu trúc (Structural Gate)
* [ ] **6.1. Bảng đối chiếu trang (Page Index) chính xác tuyệt đối:**
  - Tên cõi nước khớp 100% với kinh văn (ví dụ: cõi `Đa Bảo`, cõi `Ly Nhất Thiết Ưu`, cõi `Cận Tịch Tịnh`).
  - Tôn hiệu Đức Phật chủ cõi chính xác (Phật `Bảo Tánh`, Phật `Vô Ưu Đức`, Phật `Bảo Diệm`).
  - Hướng không gian chính xác (phương Đông, Nam, Tây, Bắc...).
* [ ] **6.2. Kiểm tra câu kết quyển:** Có đầy đủ dòng kết `**QUYỂN THỨ XX (HẾT)**`.
* [ ] **6.3. Kiểm thử tự động (Automated Test Pass):** Chạy script assertion xác nhận 0 lỗi trước khi xuất xưởng.
