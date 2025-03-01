import psutil
import time

def get_network_usage():

    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def monitor_network_usage(interval=1):

    try:
        # دریافت حجم اولیه داده‌های ارسالی و دریافتی
        initial_sent, initial_recv = get_network_usage()

        # متغیرهای برای محاسبه کل حجم مصرف شده
        total_sent = 0
        total_recv = 0

        while True:
            # انتظار برای بازه زمانی مشخص
            time.sleep(interval)

            # دریافت حجم فعلی داده‌های ارسالی و دریافتی
            current_sent, current_recv = get_network_usage()

            # محاسبه مصرف حجم در بازه زمانی
            sent = current_sent - initial_sent
            recv = current_recv - initial_recv

            # افزودن به کل حجم مصرف شده
            total_sent += sent
            total_recv += recv

            # نمایش نتایج
            print(f"حجم ارسالی در این بازه: {sent / 1024:.2f} KB")
            print(f"حجم دریافتی در این بازه: {recv / 1024:.2f} KB")
            print(f"کل حجم ارسالی: {total_sent / 1024:.2f} KB")
            print(f"کل حجم دریافتی: {total_recv / 1024:.2f} KB")
            print(f"کل مصرف حجم: {(total_sent + total_recv) / 1024:.2f} KB")
            print("-" * 30)

            # به‌روزرسانی حجم اولیه برای محاسبه بعدی
            initial_sent, initial_recv = current_sent, current_recv

    except KeyboardInterrupt:
        print("مانیتورینگ متوقف شد.")

# اجرای مانیتورینگ مصرف حجم اینترنت
if __name__ == "__main__":
    print("مانیتورینگ مصرف حجم اینترنت شروع شد. برای توقف، Ctrl+C را فشار دهید.")
    monitor_network_usage(interval=1)  # بازه زمانی 1 ثانیه