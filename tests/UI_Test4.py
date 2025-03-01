import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("450x500")  # بزرگ‌تر شدن اندازه پنجره

# فریم اصلی برای لیست و اسکرول‌بار
main_frame = ctk.CTkFrame(root)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# ایجاد Canvas برای نمایش لیست
canvas = tk.Canvas(main_frame, bg="#1F1F1F", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))  # کمی فاصله از اسکرول‌بار

# اسکرول‌بار عمودی
scrollbar = ctk.CTkScrollbar(main_frame, command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# فریم داخلی برای لیست
scrollable_frame = ctk.CTkFrame(canvas)
scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# متغیر برای دکمه‌های رادیویی
selected_item = tk.IntVar(value=-1)

# افزودن دکمه‌های رادیویی به لیست
for i in range(1, 31):  # افزایش تعداد آیتم‌ها
    radio_btn = ctk.CTkRadioButton(scrollable_frame, text=f"آیتم {i}", 
                                   variable=selected_item, value=i)
    radio_btn.pack(anchor="w", padx=15, pady=5)  # بزرگ‌تر کردن فاصله آیتم‌ها

# تابع برای بروزرسانی اسکرول‌بار
def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", update_scroll_region)

# تابع اسکرول با موس
def on_mouse_wheel(event):
    canvas.yview_scroll(-int(event.delta / 120), "units")

# فعال کردن اسکرول با موس
canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # ویندوز
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # لینوکس
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # لینوکس

root.mainloop()
