import subprocess

def get_network_interfaces_with_details():
    interfaces = []
    try:
        result = subprocess.run(
            ["netsh", "interface", "show", "interface"], # netsh Info Commands  
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()

        for line in lines:
            if "Connected" in line or "Disconnected" in line:
                parts = line.split()
                admin_state = parts[0]  # (Enable / Desable)
                state = parts[1]  # (Connect / Disconnect)
                interface_type = parts[2]  
                interface_name = " ".join(parts[3:])  # Network name

                # Discreption Network
                try:
                    desc_result = subprocess.run(
                        ["wmic", "nic", "where", f"NetConnectionID='{interface_name}'", "get", "Description"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    description_lines = desc_result.stdout.splitlines()
                    description = "None"
                    for desc_line in description_lines:
                        if desc_line.strip() and "Description" not in desc_line:
                            description = desc_line.strip()
                            break
                except subprocess.CalledProcessError as e:
                    license(f"Read Error{interface_name}: {e}")
                    description = "None"

                # Get IP
                try:
                    ip_result = subprocess.run(
                        ["netsh", "interface", "ip", "show", "addresses", f"name={interface_name}"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    ip_addresses = []
                    ip_lines = ip_result.stdout.splitlines()
                    for ip_line in ip_lines:
                        if "IP Address" in ip_line:
                            ip_address = ip_line.split(":")[1].strip()
                            ip_addresses.append(ip_address)
                except subprocess.CalledProcessError as e:
                    print(f"Get IP Error {interface_name}: {e}")
                    ip_addresses = []

                # Save Network Info
                interface_info = {
                    "name": interface_name,
                    "admin_state": admin_state,
                    "state": state,
                    "type": interface_type,
                    "description": description,
                    "ip_addresses": ip_addresses
                }
                interfaces.append(interface_info)

        for interface in interfaces:
            print(f"name   : {interface['name']}")
            print(f"Status :  {interface['admin_state']}")
            print(f"connection : {interface['state']}")
            print(f"Type  : {interface['type']}")
            print(f"Description :  {interface['description']}")
            print(f"IP: {', '.join(interface['ip_addresses']) if interface['ip_addresses'] else 'NO IP'}")
            print("-" * 30)
        return interfaces
    except subprocess.CalledProcessError as e:
        print(f"netsh Error: {e}")

# مثال استفاده
if __name__ == "__main__":
    get_network_interfaces_with_details()