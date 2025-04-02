import psutil
import time

class NetworkUsageMonitor:
    def __init__(self):
        self.initial_sent = 0
        self.initial_recv = 0
        self.total_sent = 0
        self.total_recv = 0

    def get_network_usage(self):
        net_io = psutil.net_io_counters() # Data 
        return net_io.bytes_sent, net_io.bytes_recv

    def start_monitoring(self, interval=1):
        try:
            # Transmiter Data
            self.initial_sent, self.initial_recv = self.get_network_usage()

            while True:
                time.sleep(interval)
                current_sent, current_recv = self.get_network_usage()
                sent = current_sent - self.initial_sent # Data Rate
                recv = current_recv - self.initial_recv
                self.total_sent += sent # Total Send volume consumed 
                self.total_recv += recv # Total Recive volume consumed 
                self.display_usage(sent, recv) # Final
                # Refresh
                self.initial_sent, self.initial_recv = current_sent, current_recv

        except KeyboardInterrupt:
            print("Connection Error")

    def display_usage(self, sent, recv):
        Send = f"{sent / 1024:.2f} KB"
        TotalSend = f"{self.total_sent / 1024:.2f} KB"
        Recive = f"{recv / 1024:.2f} KB"
        TotalRecive = f"{self.total_recv / 1024:.2f} KB"
        TotalUsage = f"{(self.total_sent + self.total_recv) / 1024:.2f} KB"

#if __name__ == "__main__":
#    monitor = NetworkUsageMonitor()
#    monitor.start_monitoring(interval=1)  