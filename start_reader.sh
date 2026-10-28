#!/usr/bin/env bash
# Khởi chạy Ứng dụng đọc kinh Đại Bát Nhã (Prajñā Reader)

PORT=8080
URL="http://localhost:${PORT}/reader/"

echo "==========================================================="
echo "   ☸ KINH ĐẠI BÁT NHÃ BA LA MẬT ĐA — PRAJÑĀ READER ☸"
echo "   Toàn bộ 600 Quyển · 16 Hội · 11 Tập"
echo "==========================================================="
echo ""
echo "Đang khởi chạy máy chủ đọc kinh tại: ${URL}"
echo "Nhấn Ctrl+C để dừng máy chủ khi hoàn tất đọc tụng."
echo ""

# Tự động mở trình duyệt mặc định trên macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
  sleep 1 && open "${URL}" &
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  sleep 1 && xdg-open "${URL}" &
fi

python3 -m http.server ${PORT}
