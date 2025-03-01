# created from SHe
# Import modules
import os
import sys
import argparse

# Go to current dir
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    from Tools.Set_DNS import Set_DNS
    

except ImportError as err:
    Set_DNS("Failed import some modules", err)
    sys.exit(1)


if __name__ == "__main__":
    interface_name = "Ethernet" 
    #primary_dns = "8.8.8.8"  
    #secondary_dns = "8.8.4.4" 
    dns_manager = Set_DNS(interface_name)
    #dns_manager.set_dns(primary_dns, secondary_dns)
    dns_manager.remove_dns()
    
    
    sys.exit(1)

