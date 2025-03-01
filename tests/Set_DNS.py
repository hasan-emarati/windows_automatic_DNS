import subprocess

def set_dns(interface_name, primary_dns, secondary_dns=None):
    command_primary = f'netsh interface ip set dns name="{interface_name}" static {primary_dns}'
    result_primary = subprocess.run(command_primary, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result_primary.returncode == 0:
        print(f"Primary DNS ({primary_dns}) successfully set on interface {interface_name}.")
    else:
        print(f"Failed to set primary DNS. Error: {result_primary.stderr.decode()}")
        return

    if secondary_dns:
        command_secondary = f'netsh interface ip add dns name="{interface_name}" addr={secondary_dns} index=2'
        result_secondary = subprocess.run(command_secondary, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result_secondary.returncode == 0:
            print(f"Secondary DNS ({secondary_dns}) successfully set on interface {interface_name}.")
        else:
            print(f"Failed to set secondary DNS. Error: {result_secondary.stderr.decode()}")

interface_name = "Ethernet"  
primary_dns = ""      
secondary_dns = ""    

#set_dns(interface_name, primary_dns, secondary_dns)


def remove_dns(interface_name):

    command = f'netsh interface ip set dns name="{interface_name}" source=dhcp'
    
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode == 0:
        print(f"DNS settings successfully removed on interface {interface_name}. DHCP is now active.")
    else:
        print(f"Failed to remove DNS settings. Error: {result.stderr.decode()}")

interface_name = "Ethernet" 

remove_dns(interface_name)