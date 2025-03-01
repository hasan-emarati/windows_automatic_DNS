from ping3 import ping
import time

def continuous_ping(ip_address, interval=1):
    """
    این تابع به صورت پیوسته از یک آی‌پی پینگ می‌گیرد و نتایج را نمایش می‌دهد.
    """
    try:
        print(f"شروع پینگ به {ip_address}. برای توقف، Ctrl+C را فشار دهید.")
        while True:
            # ارسال درخواست پینگ
            response_time = ping(ip_address, unit='ms')  # زمان پاسخ به میلی‌ثانیه

            if response_time is not None:
                print(f"پینگ به {ip_address} موفق بود. زمان پاسخ: {response_time:.2f} ms")
            else:
                print(f"پینگ به {ip_address} ناموفق بود. ممکن است آی‌پی در دسترس نباشد.")

            # مکث بین پینگ‌ها (مثلاً 1 ثانیه)
            time.sleep(interval)

    except KeyboardInterrupt:
        print("پینگ متوقف شد.")

# مثال استفاده
if __name__ == "__main__":
    ip_address = input("لطفاً آی‌پی مورد نظر را وارد کنید: ")  # دریافت آی‌پی از کاربر
    continuous_ping(ip_address, interval=1)  # بازه زمانی 1 ثانیه