import speedtest

def run_speed_test():
    """
    این تابع سرعت اینترنت (دانلود، آپلود، و پینگ) را تست می‌کند و نتایج را نمایش می‌دهد.
    """
    try:
        # ایجاد یک شیء Speedtest
        st = speedtest.Speedtest()

        # پیدا کردن بهترین سرور برای تست
        print("در حال پیدا کردن بهترین سرور...")
        st.get_best_server()

        # تست سرعت دانلود
        print("در حال تست سرعت دانلود...")
        download_speed = st.download() / 1_000_000  # تبدیل به مگابیت بر ثانیه

        # تست سرعت آپلود
        print("در حال تست سرعت آپلود...")
        upload_speed = st.upload() / 1_000_000  # تبدیل به مگابیت بر ثانیه

        # دریافت پینگ
        ping = st.results.ping  # پینگ به میلی‌ثانیه

        # نمایش نتایج
        print("\nspeedtest.net  :")
        print(f"سرعت دانلود: {download_speed:.2f} Mbps")
        print(f"سرعت آپلود: {upload_speed:.2f} Mbps")
        print(f"پینگ: {ping:.2f} ms")

    except Exception as e:
        print(f"خطا در اجرای تست سرعت: {e}")

# اجرای تست سرعت
if __name__ == "__main__":
    run_speed_test()