import subprocess
import sys

def install_libraries():
    libraries = ["pandas", "numpy", "openpyxl"]

    print("=========================================================")
    print(" BẮT ĐẦU KIỂM TRA VÀ CÀI ĐẶT THƯ VIỆN CHO DỰ ÁN SUPERSTORE")
    print("=========================================================\n")

    for lib in libraries:
        print(f"[*] Đang kiểm tra thư viện: {lib}...")
        try:
            # Kiểm tra xem thư viện đã có sẵn trên máy chưa
            __import__(lib)
            print(f"[✓] Thư viện '{lib}' đã được cài đặt sẵn trước đó.\n")
        except ImportError:
            # Nếu chưa có, tiến hành gọi lệnh pip install tự động
            print(f"[!] Không tìm thấy '{lib}'. Tiến hành cài đặt tự động...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", lib]
                )
                print(f"[✓] Đã cài đặt thành công thư viện: {lib}\n")
            except Exception as e:
                print(
                    f"[X] Gặp lỗi khi cài đặt thư viện {lib}. Chi tiết lỗi: {e}\n"
                )

    print("=========================================================")
    print("   HOÀN TẤT! Môi trường đã sẵn sàng để chạy Pipeline.    ")
    print("=========================================================")


if __name__ == "__main__":
    install_libraries()