import customtkinter as ctk
import tkinter as tk
import winreg

class QuickSetDNSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Windows Automatic DNS")
        self.geometry("800x500")
        self.create_navbar()

        # دریافت رنگ تم سیستم از رجیستری ویندوز
        color_key_path = r'SOFTWARE\\Microsoft\Windows\DWM'
        color_value_name = 'AccentColor'
        color_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, color_key_path)
        color_value, _ = winreg.QueryValueEx(color_key, color_value_name)
        winreg.CloseKey(color_key)
        self.color = "#{:02X}{:02X}{:02X}".format((color_value >> 16) & 0xFF, (color_value >> 8) & 0xFF, color_value & 0xFF)

        self.configure(fg_color=self.color)
        ctk.set_appearance_mode("system")

        self.create_home_page()

    def create_navbar(self):
        self.navbar_frame = ctk.CTkFrame(self, width=200, height=500, corner_radius=0, fg_color="#2D2D2D")
        self.navbar_frame.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(
            self.navbar_frame, text="DNS App",
            font=("Arial", 24, "bold"), text_color="#FFFFFF"
        )
        self.logo_label.pack(pady=30, padx=10)

        nav_buttons = [("🏠 Home", self.show_home), ("⚙️ Settings", self.show_settings), ("ℹ️ About", self.show_about)]
        for text, command in nav_buttons:
            button = ctk.CTkButton(
                self.navbar_frame, text=text, command=command,
                font=("Arial", 16), fg_color="transparent",
                hover_color="#404040", anchor="w",
                text_color="#FFFFFF", corner_radius=8
            )
            button.pack(fill="x", pady=5, padx=10)

    def create_home_page(self):
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1E1E1E")
        self.home_frame.pack(side="right", fill="both", expand=True)

        


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

        # 📌 **اسکرول‌بار و فریم اسکرول**
        scroll_frame = ctk.CTkFrame(self.home_frame, corner_radius=50, fg_color=self.color)  # فریم گرد‌شده
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        canvas = tk.Canvas(scroll_frame, bg="#2D2D2D", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(scroll_frame, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#2D2D2D")  # پس‌زمینه تیره‌تر
        scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        selected_item = tk.IntVar(value=-1)
        for i in range(1, 31):
            radio_btn = ctk.CTkRadioButton(scrollable_frame, text=f"آیتم {i}",
                                           variable=selected_item, value=i)
            radio_btn.pack(anchor="w", padx=15, pady=5)

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", update_scroll_region)

        def on_mouse_wheel(event):
            canvas.yview_scroll(-int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

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
    app = QuickSetDNSApp()
    app.mainloop()
