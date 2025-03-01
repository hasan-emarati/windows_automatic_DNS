import customtkinter as ctk
import tkinter as tk
import winreg

class WindowsAutoDNS(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Windows Automatic DNS")
        self.geometry("800x500")
        self.create_navbar()

        # دریافت رنگ اکسانت ویندوز
        color_key_path = r'SOFTWARE\\Microsoft\Windows\DWM'
        color_value_name = 'AccentColor'
        color_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, color_key_path)
        color_value, _ = winreg.QueryValueEx(color_key, color_value_name)
        winreg.CloseKey(color_key)
        self.color = "#{:02X}{:02X}{:02X}".format((color_value >> 16) & 0xFF, (color_value >> 8) & 0xFF, color_value & 0xFF)

        self.configure(fg_color=self.color)
        ctk.set_appearance_mode("system")

        # متغیرهای مدیریت آیتم‌ها
        self.item_counter = 1
        self.radio_buttons_dict = {}
        self.selected_item = tk.IntVar(value=-1)

        # وضعیت اتصال
        self.is_connected = False

        self.create_home_page()

    def create_navbar(self):
        self.navbar_frame = ctk.CTkFrame(self, width=200, height=500, corner_radius=0, fg_color="#2D2D2D")
        self.navbar_frame.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(
            self.navbar_frame, text="DNS App",
            font=("Arial", 24, "bold"), text_color="#FFFFFF"
        )
        self.logo_label.pack(pady=30, padx=10)

        # دکمه‌های نوار ناوبری با آیکون‌های گوگل
        nav_buttons = [
            ("\ue88a Home", self.show_home),  # آیکون خانه
            ("\ue8b8 Settings", self.show_settings),  # آیکون تنظیمات
            ("\ue88e Info", self.show_about)  # آیکون اطلاعات
        ]
        for text, command in nav_buttons:
            button = ctk.CTkButton(
                self.navbar_frame, text=text, command=command,
                font=("Material Icons", 16), fg_color="transparent",
                hover_color="#404040", anchor="w",
                text_color="#FFFFFF", corner_radius=8
            )
            button.pack(fill="x", pady=5, padx=10)

    def create_home_page(self):
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1E1E1E")
        self.home_frame.pack(side="right", fill="both", expand=True)

        # Combobox
        self.combo_box = ctk.CTkComboBox(
            self.home_frame, 
            values=["Option 1", "Option 2", "Option 3"],
            fg_color=self.color, 
            border_color=self.color, 
            button_color=self.color,
            border_width=8,
            corner_radius=20, 
            dropdown_fg_color=self.color,
            dropdown_hover_color="#404040",
            dropdown_text_color="white", 
            text_color="white",
            font=("Arial", 20),
            dropdown_font=("Arial", 14),
            width=0,   
        )
        self.combo_box.pack(pady=20, padx=20, fill="x")

        # فریم برای دکمه‌ها
        button_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        button_frame.pack(pady=10, padx=20, fill="x")

        # دکمه افزودن
        add_btn = ctk.CTkButton(
            button_frame,
            text="\ue145 Add Item",  # آیکون افزودن
            command=self.add_item,
            fg_color=self.color,
            hover_color="#404040",
            font=("Material Icons", 14)
        )
        add_btn.pack(side="left", padx=5)

        # دکمه حذف
        delete_btn = ctk.CTkButton(
            button_frame,
            text="\ue15d Delete Item",  # آیکون حذف
            command=self.delete_item,
            fg_color=self.color,
            hover_color="#404040",
            font=("Material Icons", 14)
        )
        delete_btn.pack(side="left", padx=5)

        # دکمه کانکت/دیسکانکت
        self.connect_btn = ctk.CTkButton(
            button_frame,
            text="\ue839 Disconnected",  # آیکون قطع
            command=self.toggle_connection,
            fg_color=self.color,
            hover_color="#404040",
            font=("Material Icons", 14)
        )
        self.connect_btn.pack(side="left", padx=5)

        # اسکرول‌بار و فریم اسکرول
        scroll_frame = ctk.CTkFrame(self.home_frame, corner_radius=50, fg_color=self.color)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        canvas = tk.Canvas(scroll_frame, bg="#2D2D2D", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(scroll_frame, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(canvas, fg_color="#2D2D2D")
        self.scrollable_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # ایجاد 3 آیتم اولیه
        for _ in range(3):
            self.add_item()

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.scrollable_frame.bind("<Configure>", update_scroll_region)

        def on_mouse_wheel(event):
            canvas.yview_scroll(-int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    def add_item(self):
        new_value = self.item_counter

        # فریم برای هر آیتم با مرزبندی
        item_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#1E1E1E",  # رنگ پس‌زمینه
            border_color=self.color,  # رنگ مرز
            border_width=2,  # ضخامت مرز
            corner_radius=10  # گوشه‌های گرد
        )
        item_frame.pack(fill="x", pady=5, padx=10)

        # رادیو باتن داخل فریم
        radio_btn = ctk.CTkRadioButton(
            item_frame,
            text=f"Item {new_value}",
            variable=self.selected_item,
            value=new_value,
            fg_color=self.color,
            text_color="white",
            font=("Arial", 14)
        )
        radio_btn.pack(side="left", padx=10, pady=5)

        # ذخیره فریم و رادیو باتن در دیکشنری
        self.radio_buttons_dict[new_value] = (item_frame, radio_btn)
        self.item_counter += 1

    def delete_item(self):
        selected_value = self.selected_item.get()
        if selected_value != -1 and selected_value in self.radio_buttons_dict:
            item_frame, radio_btn = self.radio_buttons_dict[selected_value]
            item_frame.destroy()  # حذف فریم آیتم
            del self.radio_buttons_dict[selected_value]
            self.selected_item.set(-1)

    def toggle_connection(self):
        self.is_connected = not self.is_connected
        if self.is_connected:
            self.connect_btn.configure(text="\ue838 Connected")  # آیکون متصل
        else:
            self.connect_btn.configure(text="\ue839 Disconnected")  # آیکون قطع

    def show_home(self):
        self.home_frame.pack(side="right", fill="both", expand=True)
        self.settings_frame.pack_forget() if hasattr(self, "settings_frame") else None
        self.about_frame.pack_forget() if hasattr(self, "about_frame") else None

    def show_settings(self):
        if not hasattr(self, "settings_frame"):
            self.create_settings_page()
        self.settings_frame.pack(side="right", fill="both", expand=True)
        self.home_frame.pack_forget()
        self.about_frame.pack_forget() if hasattr(self, "about_frame") else None

    def show_about(self):
        if not hasattr(self, "about_frame"):
            self.create_about_page()
        self.about_frame.pack(side="right", fill="both", expand=True)
        self.home_frame.pack_forget()
        self.settings_frame.pack_forget() if hasattr(self, "settings_frame") else None

    def create_settings_page(self):
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1E1E1E")
        settings_label = ctk.CTkLabel(
            self.settings_frame, text="Settings Page",
            font=("Arial", 24, "bold"), text_color="#FFFFFF"
        )
        settings_label.pack(pady=50)

    def create_about_page(self):
        self.about_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1E1E1E")
        about_label = ctk.CTkLabel(
            self.about_frame, text="About Page",
            font=("Arial", 24, "bold"), text_color="#FFFFFF"
        )
        about_label.pack(pady=50)

if __name__ == "__main__":
    app = WindowsAutoDNS()
    app.mainloop()