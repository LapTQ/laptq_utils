#!/bin/bash

if [ -z "$1" ]; then
    echo "Sử dụng: $0 <PID>"
    exit 1
fi

PID=$1

if [ ! -d "/proc/$PID" ]; then
    echo "⚠️ Không tìm thấy tiến trình có PID $PID (có thể nó đã chạy xong và kết thúc)."
    exit 1
fi

echo "========================================="
echo " THÔNG TIN CƠ BẢN CỦA TIẾN TRÌNH         "
echo "========================================="
ps -f -p "$PID"
echo ""

echo "========================================="
echo " TRUY VẾT DOCKER CONTAINER               "
echo "========================================="
CGROUP_FILE="/proc/$PID/cgroup"
CONTAINER_ID=""

if [ -f "$CGROUP_FILE" ]; then
    # Trích xuất ID 64 ký tự của container từ cgroup
    CONTAINER_ID=$(cat "$CGROUP_FILE" | grep -o -E 'docker-[a-f0-9]{64}\.scope|docker/[a-f0-9]{64}' | grep -o -E '[a-f0-9]{64}' | head -n 1)
fi

if [ -n "$CONTAINER_ID" ]; then
    echo "[+] Tiến trình này đang chạy trong Docker container có ID: ${CONTAINER_ID:0:12}"
    docker inspect --format ' - Tên container: {{.Name}}
 - Image: {{.Config.Image}}
 - Ngày tạo: {{.Created}}' "$CONTAINER_ID"
else
    echo "[-] Tiến trình này KHÔNG chạy trong Docker container (hoặc không có quyền truy cập cgroup)."
fi
echo ""

echo "========================================="
echo " TRUY VẾT NGƯỜI DÙNG (CÂY TIẾN TRÌNH)    "
echo "========================================="
echo "Lần ngược lên các tiến trình cha để tìm xem ai (hoặc ssh/tmux nào) đã khởi chạy:"
CUR_PID=$PID
while [ -n "$CUR_PID" ] && [ "$CUR_PID" -gt 1 ]; do
    CMD=$(ps -o cmd= -p "$CUR_PID" 2>/dev/null)
    USER=$(ps -o user= -p "$CUR_PID" 2>/dev/null)
    
    if [ -z "$CMD" ]; then
        break
    fi
    
    printf " -> PID: %-8s | USER: %-10s | CMD: %s\n" "$CUR_PID" "$USER" "$CMD"
    
    # Lấy PID của tiến trình cha
    CUR_PID=$(ps -o ppid= -p "$CUR_PID" 2>/dev/null | tr -d ' ')
done
echo "========================================="
