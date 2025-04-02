# Import modules
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Go to current dir
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    from UI import WindowsAutoDNS
    from Tools.Set_DNS import Set_DNS
    from Tools.Network_Usage import NetworkUsageMonitor
    from Tools.Network import NetworkInterfaceInfo
    from Tools.Ping import ContinuousPing
    from Tools.Speed_Test import InternetSpeedTest

except ImportError as err:
    print(f"Failed to import some modules: {err}")
    sys.exit(1)


if __name__ == "__main__":
    # interface_name = "Ethernet"
    # primary_dns = "8.8.8.8"
    # secondary_dns = "8.8.4.4"
    # dns_manager = Set_DNS(interface_name)
    # dns_manager.set_dns(primary_dns, secondary_dns)
    # dns_manager.remove_dns()

    # monitor = NetworkUsageMonitor()
    # monitor.start_monitoring(interval=1)

    # network_info = NetworkInterfaceInfo()
    # network_info.get_network_interfaces_with_details_and_description()
    # network_info.display_interfaces()


    # ip_address = input("IP Target: ")
    # ping_instance = ContinuousPing(ip_address, interval=1)
    # ping_instance.start_ping()

    #speed_test = InternetSpeedTest()
    #speed_test.run_speed_test()

    app = WindowsAutoDNS()
    app.mainloop()

    sys.exit(0)