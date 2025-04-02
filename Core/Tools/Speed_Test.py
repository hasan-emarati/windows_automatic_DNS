import speedtest
import time

class InternetSpeedTest:
    def __init__(self):
        self.st = None
        self.download_speed = None
        self.upload_speed = None
        self.ping = None

    def find_best_server(self):
        print("Connecting to Server...")
        try:
            self.st.get_best_server()
        except speedtest.SpeedtestBestServerFailure as e:
            print(f"Request Error : {e}")
            return False
        return True

    def test_download_speed(self):
        print("Download Speed...")
        try:
            self.download_speed = self.st.download() / 1_000_000  
        except speedtest.SpeedtestDownloadError as e:
            print(f"Download Speed Error : {e}")
            return False
        return True

    def test_upload_speed(self):
        print("Upload Speed...")
        try:
            self.upload_speed = self.st.upload() / 1_000_000  # تبدیل به مگابیت بر ثانیه
        except speedtest.SpeedtestUploadError as e:
            print(f"Upload Speed Error : {e}")
            return False
        return True

    def get_ping(self):
        try:
            self.ping = self.st.results.ping  # پینگ به میلی‌ثانیه
        except AttributeError:
            print("Ping Error")
            return False
        return True

    def run_speed_test(self):
        try:
            self.st = speedtest.Speedtest()
            if not self.find_best_server():
                return
            if not self.test_download_speed():
                return
            if not self.test_upload_speed():
                return
            if not self.get_ping():
                return
            self.display_results()

        except speedtest.ConfigRetrievalError as e:
            print(f"Result Error : {e}")
        except Exception as e:
            print(f"Speed test Erorr : {e}")

    def display_results(self):
        print(f"Download Speed : {self.download_speed:.2f} Mbps")
        print(f"Upload Speed : {self.upload_speed:.2f} Mbps")
        print(f"ping {self.ping:.2f} ms")

# اجرای تست سرعت
if __name__ == "__main__":
    speed_test = InternetSpeedTest()
    speed_test.run_speed_test()