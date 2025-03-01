import customtkinter as ctk

# تنظیمات اولیه
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

root = ctk.CTk()
root.geometry("300x200")

# ساختن ComboBox با شبیه‌سازی لبه‌های گرد
combo = ctk.CTkComboBox(root, 
                        values=["گزینه ۱", "گزینه ۲", "گزینه ۳"],
                        fg_color="#1F6AA5",   # رنگ پس‌زمینه
                        border_color="#1F6AA5",  # رنگ مرز
                        border_width=3,  # ضخامت مرز برای گرد شدن
                        corner_radius=20,  # مقدار گرد شدن لبه‌ها
                        dropdown_fg_color="#1F6AA5",  # رنگ پس‌زمینه لیست بازشو
                        dropdown_text_color="white",  # رنگ متن در لیست بازشو
                        text_color="white"  # رنگ متن
                        )
combo.pack(pady=50)




root.mainloop()
