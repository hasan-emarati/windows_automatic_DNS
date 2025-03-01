import subprocess

def get_network_interfaces_with_details_and_description():
    """
    این تابع تمام کارت‌های شبکه را به همراه توضیحات (وضعیت، نوع، توضیحات، و IP آدرس‌ها) برمی‌گرداند.
    خروجی به صورت لیستی از دیکشنری‌ها است.
    """
    try:
        # اجرای دستور netsh برای دریافت اطلاعات کارت‌های شبکه
        result = subprocess.run(
            ["netsh", "interface", "show", "interface"],
            capture_output=True,
            text=True,
            check=True
        )

        # پردازش خروجی
        interfaces = []
        lines = result.stdout.splitlines()

        # خطوط مربوط به کارت‌های شبکه را استخراج می‌کنیم
        for line in lines:
            if "Connected" in line or "Disconnected" in line:
                parts = line.split()
                # استخراج اطلاعات
                admin_state = parts[0]  # وضعیت اداری (Enabled/Disabled)
                state = parts[1]  # وضعیت اتصال (Connected/Disconnected)
                interface_type = parts[2]  # نوع کارت شبکه (Dedicated/...)
                interface_name = " ".join(parts[3:])  # نام کارت شبکه

                # دریافت توضیحات (Description)
                description = get_description_for_interface(interface_name)

                # دریافت IP آدرس‌ها
                ip_addresses = get_ip_addresses_for_interface(interface_name)

                # ذخیره اطلاعات در یک دیکشنری
                interface_info = {
                    "name": interface_name,
                    "admin_state": admin_state,
                    "state": state,
                    "type": interface_type,
                    "description": description,
                    "ip_addresses": ip_addresses
                }
                interfaces.append(interface_info)

        return interfaces

    except subprocess.CalledProcessError as e:
        print(f"خطا در اجرای دستور netsh: {e}")
        return []

def get_description_for_interface(interface_name):
    """
    این تابع توضیحات (Description) مربوط به یک کارت شبکه خاص را برمی‌گرداند.
    """
    try:
        # اجرای دستور wmic برای دریافت توضیحات
        result = subprocess.run(
            ["wmic", "nic", "where", f"NetConnectionID='{interface_name}'", "get", "Description"],
            capture_output=True,
            text=True,
            check=True
        )

        # پردازش خروجی
        lines = result.stdout.splitlines()
        for line in lines:
            if line.strip() and "Description" not in line:
                return line.strip()

        return "بدون توضیحات"

    except subprocess.CalledProcessError as e:
        print(f"خطا در دریافت توضیحات برای کارت شبکه {interface_name}: {e}")
        return "بدون توضیحات"

def get_ip_addresses_for_interface(interface_name):
    """
    این تابع IP آدرس‌های مربوط به یک کارت شبکه خاص را برمی‌گرداند.
    """
    try:
        # اجرای دستور netsh برای دریافت IP آدرس‌ها
        result = subprocess.run(
            ["netsh", "interface", "ip", "show", "addresses", f"name={interface_name}"],
            capture_output=True,
            text=True,
            check=True
        )

        # پردازش خروجی
        ip_addresses = []
        lines = result.stdout.splitlines()

        for line in lines:
            if "IP Address" in line:
                ip_address = line.split(":")[1].strip()
                ip_addresses.append(ip_address)

        return ip_addresses

    except subprocess.CalledProcessError as e:
        print(f"خطا در دریافت IP آدرس‌ها برای کارت شبکه {interface_name}: {e}")
        return []

# مثال استفاده
if __name__ == "__main__":
    interfaces = get_network_interfaces_with_details_and_description()
    print("کارت‌های شبکه با جزئیات، توضیحات و IP آدرس‌ها:")
    for interface in interfaces:
        print(f"name : {interface['name']}")
        print(f"admin_state : {interface['admin_state']}")
        print(f"conection state : {interface['state']}")
        print(f"type: {interface['type']}")
        print(f"description: {interface['description']}")
        print(f"IP : {', '.join(interface['ip_addresses']) if interface['ip_addresses'] else 'بدون IP'}")
        print("-" * 30)