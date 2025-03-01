import subprocess

class Set_DNS:
    def __init__(self, interface_name):
        self.interface_name = interface_name

    def set_dns(self, primary_dns, secondary_dns=None):
        command_primary = f'netsh interface ip set dns name="{self.interface_name}" static {primary_dns}'
        result_primary = subprocess.run(command_primary, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result_primary.returncode == 0:
            print(f"Primary DNS ({primary_dns}) successfully set on interface {self.interface_name}.")
        else:
            print(f"Failed to set primary DNS. Error: {result_primary.stderr.decode()}")
            return

        if secondary_dns:
            command_secondary = f'netsh interface ip add dns name="{self.interface_name}" addr={secondary_dns} index=2'
            result_secondary = subprocess.run(command_secondary, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result_secondary.returncode == 0:
                print(f"Secondary DNS ({secondary_dns}) successfully set on interface {self.interface_name}.")
            else:
                print(f"Failed to set secondary DNS. Error: {result_secondary.stderr.decode()}")

    def remove_dns(self):
        command = f'netsh interface ip set dns name="{self.interface_name}" source=dhcp'
        
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print(f"DNS settings successfully removed on interface {self.interface_name}. DHCP is now active.")
        else:
            print(f"Failed to remove DNS settings. Error: {result.stderr.decode()}")

#if __name__ == "__main__":
#    interface_name = "Ethernet" 
#    primary_dns = "8.8.8.8"  
#    secondary_dns = "8.8.4.4" 

#    dns_manager = Set_DNS(interface_name)

#    dns_manager.set_dns(primary_dns, secondary_dns)

#    dns_manager.remove_dns()