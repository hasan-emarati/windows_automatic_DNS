import customtkinter as ctk
import tkinter as tk
import winreg

class WindowsAutoDNS(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Windows Automatic DNS")
        self.geometry("800x500")
        color_key_path = r'SOFTWARE\\Microsoft\Windows\DWM'  # Windows RGB
        color_value_name = 'AccentColor'
        color_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, color_key_path)
        color_value, _ = winreg.QueryValueEx(color_key, color_value_name)
        winreg.CloseKey(color_key)
        blue = (color_value >> 16) & 0xFF  # RGB to BRG
        green = (color_value >> 8) & 0xFF  # RGB to BRG
        red = color_value & 0xFF  # RGB to BRG
        self.color = "#{:02X}{:02X}{:02X}".format(red, green, blue)  # Local Color
        self.configure(fg_color=self.color)  # Foreground Color
        ctk.set_appearance_mode("system")

        self.item_counter = 1
        self.radio_buttons_dict = {}
        self.selected_item = tk.IntVar(value=-1)  # No item selected by default
        self.temp_selected_item = -1  # Temporary selected item
        self.confirmed_item = -1  # Confirmed selected item
        self.edit_mode = False  # Track edit mode

        self.current_page = "home"  # Nav Bar Default Page
        self.nav_buttons = {}  # Nav Buttons

        self.create_navbar()
        self.create_home_page()

        # Bind the Enter key to confirm the selection
        self.bind("<Return>", self.confirm_selection)

    def create_navbar(self):
        self.navbar_frame = ctk.CTkFrame(self, width=200, height=500, corner_radius=0, fg_color="#2D2D2D")
        self.navbar_frame.pack(side="left", fill="y")
        self.logo_label = ctk.CTkLabel(
            self.navbar_frame, text="DNS App",
            font=("Arial", 24, "bold"), text_color="#FFFFFF"
        )
        self.logo_label.pack(pady=30, padx=10)
        nav_buttons_info = [
            ("\ue88a Home", "home", self.show_home),
            ("\uf833 Settings", "settings", self.show_settings),
            ("\ue88e Info", "about", self.show_about)
        ]
        for text, page, command in nav_buttons_info:
            button = ctk.CTkButton(
                self.navbar_frame, text=text, command=lambda p=page, c=command: self.change_page(p, c),
                font=("Material Icons", 16), fg_color="transparent",
                hover_color="#404040", anchor="w",
                text_color="#FFFFFF", corner_radius=8,
                border_spacing=10,
                compound="left"
            )
            button.pack(fill="x", pady=5, padx=10)
            self.nav_buttons[page] = button

        self.update_navbar_buttons()

    def change_page(self, page, command):
        self.current_page = page
        command()
        self.update_navbar_buttons()

    def update_navbar_buttons(self):
        for page, button in self.nav_buttons.items():
            if page == self.current_page:
                button.configure(fg_color="#404040", text_color="#EE00B6")
            else:
                button.configure(fg_color="transparent", text_color="#FFFFFF")

    def create_home_page(self):
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1E1E1E")
        self.home_frame.pack(side="right", fill="both", expand=True)

        self.option_menu = ctk.CTkOptionMenu(
            self.home_frame,
            values=["Option 1", "Option 2", "Option 3"],
            fg_color=self.color,
            button_color=self.color,
            text_color="white",
            font=("Arial", 16),
            dropdown_fg_color=self.color,
            dropdown_hover_color="#404040",
            dropdown_text_color="white",
            width=200,
            height=30
        )
        self.option_menu.pack(pady=20, padx=20, fill="x")

        button_container = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        button_container.pack(side="right", padx=5, pady=10)

        add_btn = ctk.CTkButton(
            button_container,
            text="➕",
            command=self.add_item,
            fg_color=self.color,
            hover_color="#404040",
            font=("Arial", 20),
            width=20,
            height=20,
            corner_radius=15
        )
        add_btn.pack(side="top", pady=5)

        edit_btn = ctk.CTkButton(
            button_container,
            text="✏️",
            command=self.toggle_edit_mode,
            fg_color=self.color,
            hover_color="#404040",
            font=("Arial", 20),
            width=20,
            height=20,
            corner_radius=15
        )
        edit_btn.pack(side="top", pady=5)

        delete_btn = ctk.CTkButton(
            button_container,
            text="➖",
            command=self.delete_item,
            fg_color=self.color,
            hover_color="#404040",
            font=("Arial", 20),
            width=20,
            height=20,
            corner_radius=15
        )
        delete_btn.pack(side="top", pady=5)

        scroll_frame = ctk.CTkFrame(self.home_frame, corner_radius=50, fg_color="#3D2F3F")
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        canvas = tk.Canvas(scroll_frame, bg="#2D2D2D", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(scroll_frame, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(canvas, fg_color="#2D2D2D")
        self.scrollable_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        headers_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2D2D2D")
        headers_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(headers_frame, text="DNS Name", font=("Arial", 14, "bold"), width=150).pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="IPv4", font=("Arial", 14, "bold"), width=100).pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="IPv6", font=("Arial", 14, "bold"), width=100).pack(side="left", padx=5)

        self.message_label = ctk.CTkLabel(
            self.home_frame,
            text="",
            font=("Arial", 14),
            text_color="white",
            fg_color="transparent"
        )
        self.message_label.pack(side="bottom", pady=10, fill="x")

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
        item_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#1E1E1E",
            border_color=self.color,
            border_width=2,
            corner_radius=10
        )
        item_frame.pack(fill="x", pady=5, padx=10)
        
        radio_btn = ctk.CTkRadioButton(
            item_frame,
            text="",
            variable=self.selected_item,
            value=new_value,
            fg_color="#3A3939",
            hover_color="#1E1E1E",
            text_color="white",
            border_color="#1E1E1E",
            font=("Arial", 14),
            command=lambda: self.change_item_background(new_value),
            width=20
        )
        radio_btn.pack(side="left", padx=(10, 5), pady=5)
        
        # DNS Name Entry
        dns_entry = ctk.CTkEntry(
            item_frame,
            placeholder_text=f"DNS {new_value}",
            width=150,
            fg_color="#1E1E1E",
            text_color="white",
            border_color="#1E1E1E",
            state="disabled",
            placeholder_text_color="white"
        )
        dns_entry.pack(side="left", padx=5, pady=5)
        
        # IPv4 Entry
        ipv4_entry = ctk.CTkEntry(
            item_frame,
            placeholder_text="0.0.0.0",
            width=100,
            fg_color="#1E1E1E",
            text_color="white",
            border_color="#1E1E1E",
            state="disabled",
            placeholder_text_color="white"
        )
        ipv4_entry.pack(side="left", padx=5, pady=5)
        
        # IPv6 Entry
        ipv6_entry = ctk.CTkEntry(
            item_frame,
            placeholder_text="::1",
            width=100,
            fg_color="#1E1E1E",
            text_color="white",
            border_color="#1E1E1E",
            state="disabled",
            placeholder_text_color="white"
        )
        ipv6_entry.pack(side="left", padx=5, pady=5)
        
        self.radio_buttons_dict[new_value] = {
            "frame": item_frame,
            "radio": radio_btn,
            "dns_entry": dns_entry,
            "ipv4_entry": ipv4_entry,
            "ipv6_entry": ipv6_entry
        }
        self.item_counter += 1

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        new_state = "normal" if self.edit_mode else "disabled"
        new_bg = "#2D2D2D" if self.edit_mode else "#1E1E1E"
        new_border = self.color if self.edit_mode else "#1E1E1E"
        
        for item_data in self.radio_buttons_dict.values():
            item_data["dns_entry"].configure(state=new_state, fg_color=new_bg ,border_color=new_border)
            item_data["ipv4_entry"].configure(state=new_state, fg_color=new_bg,border_color=new_border)
            item_data["ipv6_entry"].configure(state=new_state, fg_color=new_bg,border_color=new_border)
        
        self.message_label.configure(
            text="Edit Mode: ON" if self.edit_mode else "Edit Mode: OFF",
            text_color="#00FF00" if self.edit_mode else "#FF0000"
        )
    # Radio change Selected item
    def change_item_background(self, selected_value):
        for value, item_data in self.radio_buttons_dict.items():
            item_data["frame"].configure(fg_color="#1E1E1E")
        if selected_value in self.radio_buttons_dict:
            self.radio_buttons_dict[selected_value]["ipv6_entry"].configure(fg_color=self.color ,border_color=self.color)
            self.radio_buttons_dict[selected_value]["ipv4_entry"].configure(fg_color=self.color,border_color=self.color)
            self.radio_buttons_dict[selected_value]["dns_entry"].configure(fg_color=self.color,border_color=self.color)
            self.radio_buttons_dict[selected_value]["frame"].configure(fg_color=self.color,border_color=self.color)
        self.temp_selected_item = selected_value

    def confirm_selection(self, event=None):
        if self.temp_selected_item != -1:
            if self.confirmed_item != -1 and self.confirmed_item in self.radio_buttons_dict:
                self.radio_buttons_dict[self.confirmed_item]["radio"].configure(fg_color="#1E1E1E")

            if self.temp_selected_item in self.radio_buttons_dict:
                self.radio_buttons_dict[self.temp_selected_item]["radio"].configure(fg_color="#00FF00")
            self.confirmed_item = self.temp_selected_item
            self.selected_item.set(self.temp_selected_item)
            
            item_data = self.radio_buttons_dict[self.temp_selected_item]
            dns = item_data["dns_entry"].get() or item_data["dns_entry"].cget("placeholder_text")
            ipv4 = item_data["ipv4_entry"].get() or item_data["ipv4_entry"].cget("placeholder_text")
            ipv6 = item_data["ipv6_entry"].get() or item_data["ipv6_entry"].cget("placeholder_text")
            self.message_label.configure(
                text=f"Selected: DNS={dns}, IPv4={ipv4}, IPv6={ipv6}",
                text_color="white"
            )
        else:
            self.message_label.configure(text="No item selected!", text_color="white")

    def delete_item(self):
        selected_value = self.selected_item.get()
        if selected_value != -1 and selected_value in self.radio_buttons_dict:
            self.radio_buttons_dict[selected_value]["frame"].destroy()
            del self.radio_buttons_dict[selected_value]
            self.selected_item.set(-1)
            self.message_label.configure(text="Item deleted", text_color="white")

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