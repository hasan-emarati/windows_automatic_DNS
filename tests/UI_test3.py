import ctypes
import struct

def get_accent_color():
    dwmapi = ctypes.windll.dwmapi
    color = ctypes.c_uint32()

    # Call DwmGetColorizationColor to get the accent color
    dwmapi.DwmGetColorizationColor(ctypes.byref(color), ctypes.c_bool())

    # Extract the RGB values
    color_value = color.value
    blue = (color_value & 0xFF)
    green = (color_value >> 8) & 0xFF
    red = (color_value >> 16) & 0xFF

    return f"#{red:02X}{green:02X}{blue:02X}"

accent_color = get_accent_color()
print(f"User's Windows theme color is: {accent_color}")
