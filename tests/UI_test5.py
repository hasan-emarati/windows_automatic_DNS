import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CTkComboBox as Button")
        self.geometry("400x200")
        
        # ایجاد فریم
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # مقادیر ComboBox
        options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        
        # ایجاد ComboBox با ظاهر دکمه
        self.combobox = ctk.CTkComboBox(
            master=self.frame,
            values=options,
            width=0,
            corner_radius=20,
            border_width=0,
            button_color="#2CC985",
            dropdown_fg_color="#2CC985",
            state="readonly"  # غیرفعال کردن ویرایش مستقیم متن
        )
        self.combobox.pack(fill="x", padx=20, pady=20)
        self.combobox.set("Click Me!")  # متن پیش‌فرض
        
        # اتصال رویداد کلیک به تابع
        self.combobox.bind("<Button-1>", self.combobox_clicked)

    def combobox_clicked(self, event):
        print("Combobox clicked as a button!")
        # اینجا می‌توانید هر عملکرد دلخواهی اضافه کنید
        return "break"  # جلوگیری از بازشدن dropdown

if __name__ == "__main__":
    app = App()
    app.mainloop()