import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import threading
import pyttsx3

# --- அட்மின் மற்றும் மெம்பர் பாஸ்வேர்டு ---
ADMIN_PASS = "admintest@123"
MEMBER_PASS = "membertest@123"

class GangBoysApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GANG BOYS 🥷")
        self.root.geometry("500x750")
        self.root.configure(bg="#000000")
        self.engine = pyttsx3.init()
        
        # தற்காலிக டேட்டா சேமிப்பு
        self.income_list = []
        self.expense_list = []
        self.complaints = []
        self.announcement = "இன்னும் அறிவிப்புகள் இல்லை."
        
        self.login_page()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- 1. லாகின் பக்கம் ---
    def login_page(self):
        self.clear_screen()
        tk.Label(self.root, text="GANG BOYS 🥷", font=("Helvetica", 30, "bold"), fg="#FFD700", bg="#000000").pack(pady=40)
        
        fields = [("பெயர்", False), ("தொலைபேசி", False), ("பிறந்தநாள் (DD-MM)", False), ("பாஸ்வேர்டு", True)]
        self.entries = {}

        for label, is_pass in fields:
            tk.Label(self.root, text=label, fg="white", bg="#000000", font=("Arial", 12)).pack()
            ent = tk.Entry(self.root, width=30, show="*" if is_pass else "", font=("Arial", 12))
            ent.pack(pady=5)
            self.entries[label] = ent

        tk.Button(self.root, text="நுழைவு (LOGIN)", font=("Arial", 12, "bold"), bg="#FFD700", fg="black", 
                  width=20, command=self.process_login).pack(pady=30)

    def process_login(self):
        name = self.entries["பெயர்"].get()
        pwd = self.entries["பாஸ்வேர்டு"].get()
        dob = self.entries["பிறந்தநாள் (DD-MM)"].get()
        today = datetime.datetime.now().strftime("%d-%m")

        if pwd == ADMIN_PASS or pwd == MEMBER_PASS:
            is_admin = (pwd == ADMIN_PASS)
            if dob == today:
                self.birthday_animation(name, is_admin)
            else:
                self.home_page(name, is_admin)
        else:
            messagebox.showerror("Error", "தவறான பாஸ்வேர்டு!")

    # --- 2. பிறந்தநாள் அனிமேஷன் & வாழ்த்து ---
    def birthday_animation(self, name, is_admin):
        self.clear_screen()
        tk.Label(self.root, text="🎈🎈🎈", font=("Arial", 50), bg="#000000").pack(pady=20)
        tk.Label(self.root, text=f"இனிய பிறந்தநாள் வாழ்த்துக்கள்\n{name}!", 
                 font=("Helvetica", 22, "bold"), fg="#FFD700", bg="#000000", justify="center").pack(pady=50)
        
        def speak():
            self.engine.say(f"Iniya pirantha naal vaalthukkal {name}")
            self.engine.runAndWait()
        
        threading.Thread(target=speak).start()
        self.root.after(6000, lambda: self.home_page(name, is_admin))

    # --- 3. முகப்புப் பக்கம் ---
    def home_page(self, name, is_admin):
        self.clear_screen()
        # ரைட் கார்னர் லோகோ டெக்ஸ்ட்
        tk.Label(self.root, text="🥷 GB", fg="#FFD700", bg="#000000", font=("bold", 14)).place(x=440, y=10)
        
        welcome_frame = tk.Frame(self.root, bg="#FFD700", pady=10)
        welcome_frame.pack(fill="x")
        tk.Label(welcome_frame, text=f"அன்புடன் GANG BOYS குழுவிற்கு வரவேற்கிறோம், {name}! 🙏", 
                 bg="#FFD700", fg="black", font=("Arial", 11, "bold")).pack()

        # அறிவிப்பு பலகை (மேலே தோன்றும்)
        tk.Label(self.root, text=f"📢 அறிவிப்பு: {self.announcement}", fg="white", bg="#333", font=("Arial", 10, "italic")).pack(fill="x", pady=5)

        menu_frame = tk.Frame(self.root, bg="#000000")
        menu_frame.pack(pady=20)

        buttons = [
            ("👗 ஆடை அளவுகள்", lambda: self.dress_sizes(name, is_admin)),
            ("💰 வரவு செலவு", lambda: self.finance_page(name, is_admin)),
            ("📦 புகார் பெட்டி", lambda: self.complaint_page(name, is_admin)),
            ("🆔 அடையாள அட்டை", lambda: self.id_card_page(name)),
        ]

        for text, cmd in buttons:
            tk.Button(menu_frame, text=text, width=30, pady=10, bg="#222", fg="white", font=("Arial", 11), command=cmd).pack(pady=5)

        if is_admin:
            tk.Button(menu_frame, text="🛡️ தலைவர் அறை (ADMIN)", width=30, pady=10, bg="#8B0000", fg="white", 
                      font=("Arial", 11, "bold"), command=lambda: self.admin_room(name)).pack(pady=20)

    # --- 4. ஆடை அளவுகள் பக்கம் ---
    def dress_sizes(self, name, is_admin):
        self.clear_screen()
        tk.Label(self.root, text="ஆடை அளவுகள்
