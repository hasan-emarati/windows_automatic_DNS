from ping3 import ping
import time

class ContinuousPing:
    def __init__(self, ip_address, interval=1):
        self.ip_address = ip_address
        self.interval = interval

    def start_ping(self):
        try:
            print(f"{self.ip_address}")
            while True:
                # Ping request
                response_time = ping(self.ip_address, unit='ms')  

                if response_time is not None:
                    print(f"{self.ip_address}:{response_time:.2f} ms")
                else:
                    print(f"{self.ip_address}")

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("Stop")

if __name__ == "__main__":
    ip_address = input("IP : ")  
    ping_instance = ContinuousPing(ip_address, interval=1)  
    ping_instance.start_ping()  