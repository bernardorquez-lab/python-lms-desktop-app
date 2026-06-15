import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
from unicodedata import name
from PIL import Image, ImageTk, ImageFilter, ImageDraw
from click import clear
from Database import  database1, student_engine
import importlib, sys

if "Student" in sys.modules:
    del sys.modules["Student"]
    
class DANASLogin:
    def __init__(self, root):
        database1.init_db()
        self.root = root
        self.root.title("DANAS - PUP LMS Portal")
        self.root.state('zoomed')
        self.root.resizable(False, False)

        self.maroon      = "#631214"
        self.maroon_card = "#3d080a"
        self.maroon_btn  = "#800c0e"
        self.yellow      = "#f5ee33"
        self.white       = "#fdfdfd"
        self.black       = "#000000"

        self.font_left_header     = ("Helvetica", 13, "bold")
        self.font_serif           = ("Helvetica", 11)
        self.font_serif_bold      = ("Helvetica", 11, "bold")
        self.font_serif_italic    = ("Helvetica", 10, "italic")
        self.font_small_serif     = ("Helvetica", 9)
        self.font_serif_underline = ("Helvetica", 11, "underline")

        self.bg_image_path   = r"c:\Users\orque\Downloads\1ca96c69-9815-4649-88dc-9c7374d624ac.jpg"
        self.logo_image_path = r"c:\Users\orque\Downloads\5d93139f-1806-4f2b-95bc-5e479d7c9286 (1).jpg"

        self.members = [
            {
                "name": "Bernard Anthony F. Orquez",
                "role": "Project Manager",
                "initials": "BO",
                "position": "Project Manager",
                "gender": "Male",
                "city_address": "52-19 Loreto St., Sampaloc, Manila",
                "provincial_address": "Bulacan, Marilao",
                "cellphone": "09997981098",
                "email": "bernardorquez@gmail.com",
                "dob": "October 2, 2007",
                "height": "176cm",
                "religion": "Roman Catholic",
                "civil_status": "Single",
                "message": "I'm starting to like coding, pero nakakahilo paren!",
                "photo_path": r"c:\Users\orque\OneDrive\Pictures\Screenshots\Screenshot 2026-06-13 202216.png",
            },
            {
                "name": "Krysha Loraine F. Fajura",
                "role": "Backend Developer",
                "initials": "KF",
                "position": "Backend Developer",
                "gender": "Female",
                "city_address": "658 Dona Maria St., Brgy 584, Sampaloc, Manila",
                "provincial_address": "S Osmena St., Brgy Poblacion, Banton, Romblon",
                "cellphone": "09777460232",
                "email": "kryshalorainefajura1234@gmail.com",
                "dob": "October 8, 2006",
                "height": "160 cm",
                "religion": "Roman Catholic",
                "civil_status": "Single",
                "message": "—",
                "photo_path": r"c:\Users\orque\OneDrive\Pictures\Screenshots\Screenshot 2026-06-13 202059.png",
            },
            {
                "name": "Jayvee Rayniel B. Iggo",
                "role": "Backend Developer",
                "initials": "JI",
                "position": "Backend Developer",
                "gender": "Male",
                "city_address": "7 Gregorio St. Novaliches, Quezon City",
                "provincial_address": "Catanduanes, Bicol",
                "cellphone": "09169645668",
                "email": "jayveeiggo0@gmail.com",
                "dob": "December 23, 2003",
                "height": "165cm",
                "religion": "Roman Catholic",
                "civil_status": "Single",
                "message": "—",
                "photo_path": None,
            },
            {
                "name": "Charles Irwin Garado",
                "role": "Backend Developer",
                "initials": "CG",
                "position": "Backend Developer",
                "gender": "Male",
                "city_address": "—",
                "provincial_address": "—",
                "cellphone": "—",
                "email": "—",
                "dob": "—",
                "height": "—",
                "religion": "—",
                "civil_status": "—",
                "message": "—",
                "photo_path": r"c:\Users\orque\OneDrive\Pictures\Screenshots\Screenshot 2026-06-13 204248.png",
            },
            {
                "name": "Nica Ella P. Gajardo",
                "role": "Backend Developer",
                "initials": "EG",
                "position": "Backend Developer",
                "gender": "Female",
                "city_address": "117 Sitio Sampaguita Brgy. Santa Cruz Antipolo City, Rizal",
                "provincial_address": "",
                "cellphone": "09052063150",
                "email": "gajardonicaella86@gmail.com",
                "dob": "November 29, 2007",
                "height": "152.4 cm",
                "religion": "Christian",
                "civil_status": "Single",
                "message": "—",
                "photo_path": r"c:\Users\orque\OneDrive\Pictures\Screenshots\Screenshot 2026-06-13 210810.png",
            },
            {
                "name": "Marcus Alexander S. Rosales",
                "role": "UI/UX Designer",
                "initials": "MR",
                "position": "UI/UX Designer",
                "gender": "Male",
                "city_address": "1, Silver Spring Park St., Malanday, Marikina",
                "provincial_address": "Naujan, Mindoro",
                "cellphone": "09765657336",
                "email": "marcusrosales.pqepwppy@gmail.com ",
                "dob": "January 30, 2006",
                "height": "175cm",
                "religion": "Christian",
                "civil_status": "Single",
                "message": "—",
                "photo_path": r"c:\Users\orque\OneDrive\Pictures\Screenshots\Screenshot 2026-06-13 201941.png",
            },
            {
                "name": "Shan Ashley C. Carillo",
                "role": "UI/UX Designer",
                "initials": "SC",
                "position": "UI/UX Designer",
                "gender": "Female",
                "city_address": "Blk 8 Lot 11 Phase 1 Northgate, City of San Jose Del Monte, Bulacan",
                "provincial_address": "Labangon, Cebu City, Cebu / Naga City, Camarines Sur",
                "cellphone": "09770414383",
                "email": "ashleyycarilloo@gmail.com",
                "dob": "August 13, 2007",
                "height": "162cm",
                "religion": "Roman Catholic",
                "civil_status": "Single",
                "message": "It took a whole lot of sem for me to realize coding is fun when it comes to designing UI. Thank you Sir Godofredo!",
                "photo_path": r"c:\Users\orque\OneDrive\Pictures\Screenshots\Screenshot 2026-06-13 201931.png",
            },
            {
                "name": "Verdhenz Apple M. Domasig",
                "role": "UI/UX Designer",
                "initials": "VD",
                "position": "UI/UX Designer",
                "gender": "Female",
                "city_address": "3349 Atis St. Kalawaan, Pasig City",
                "provincial_address": "Prieto Diaz, Bicol",
                "cellphone": "09383656082",
                "email": "verdhenzapplem.domasig@gmail.com",
                "dob": "December 22, 2006",
                "height": "150 cm",
                "religion": "Roman Catholic",
                "civil_status": "Single",
                "message": "—",
                "photo_path": r"c:\Users\orque\OneDrive\Pictures\Screenshots\Screenshot 2026-06-13 202226.png",
            },
            {
                "name": "Osiris R. Jugo",
                "role": "Quality Assurance/\nDocumentation",
                "initials": "OJ",
                "position": "Quality Assurance/Documentation",
                "gender": "Male",
                "city_address": "—",
                "provincial_address": "—",
                "cellphone": "—",
                "email": " osirisracazajugo@gmail.com",
                "dob": "October 28, 2005",
                "height": "158 cm",
                "religion": "Roman Catholic",
                "civil_status": "Single",
                "message": "Set your heart ablaze.",
                "photo_path": r"c:\Users\orque\OneDrive\Pictures\Screenshots\Screenshot 2026-06-13 201920.png",
            },
            {
                "name": "Erwin Jhay M. Santos",
                "role": "Quality Assurance/\nDocumentation",
                "initials": "MT",
                "position": "Quality Assurance/ Documentation",
                "gender": "Male",
                "city_address": "113 JM Basa St. Calumpang, Marikina City",
                "provincial_address": "—",
                "cellphone": "09694034994",
                "email": "santoserwinjhay105@gmail.com",
                "dob": "February 22, 2007",
                "height": "169cm",
                "religion": "Roman Catholic",
                "civil_status": "Single",
                "message": "—",
                "photo_path": r"c:\Users\orque\OneDrive\Pictures\Screenshots\Screenshot 2026-06-13 202207.png",
            },
        ]

        self.canvas = tk.Canvas(self.root, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._load_images()
        self._build_shared_header()
        self._build_login_page()
        self._build_info_page()
        self._show_login_page()
        self.root.bind("<Configure>", self._on_resize)

    def _make_circle_photo(self, initials, size=110, photo_path=None):
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([0, 0, size - 1, size - 1], fill="#800c0e")

        if photo_path:
            try:
                member_img = Image.open(photo_path).convert("RGBA")
                member_img = member_img.resize((size - 6, size - 6), Image.Resampling.LANCZOS)

                mask = Image.new("L", (size - 6, size - 6), 0)
                ImageDraw.Draw(mask).ellipse([0, 0, size - 7, size - 7], fill=255)

                img.paste(member_img, (3, 3), mask)

                draw = ImageDraw.Draw(img)
                draw.ellipse([0, 0, size - 1, size - 1], fill=None, outline="#ffb516", width=3)

            except (FileNotFoundError, Exception):
                draw.ellipse([0, 0, size - 1, size - 1], fill=None, outline="#ffb516", width=3)
                try:
                    from PIL import ImageFont
                    fnt = ImageFont.truetype("arial.ttf", size // 3)
                except Exception:
                    fnt = None
                bbox = draw.textbbox((0, 0), initials, font=fnt)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                draw.text(((size - tw) / 2, (size - th) / 2 - 2), initials, fill="#ffb516", font=fnt)
        else:
            draw.ellipse([0, 0, size - 1, size - 1], fill=None, outline="#ffb516", width=3)
            try:
                from PIL import ImageFont
                fnt = ImageFont.truetype("arial.ttf", size // 3)
            except Exception:
                fnt = None
            bbox = draw.textbbox((0, 0), initials, font=fnt)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text(((size - tw) / 2, (size - th) / 2 - 2), initials, fill="#ffb516", font=fnt)

        return ImageTk.PhotoImage(img)

    def _load_images(self):
        try:
            raw = Image.open(self.bg_image_path)
            self.blurred_bg = raw.filter(ImageFilter.GaussianBlur(radius=1))
        except FileNotFoundError:
            self.blurred_bg = None
            self.canvas.configure(bg="#1e0304")

        self.bg_img_id = self.canvas.create_image(0, 0, anchor="nw")

        try:
            raw_logo = Image.open(self.logo_image_path)
            self.logo_photo_sm = ImageTk.PhotoImage(
                raw_logo.resize((45, 45), Image.Resampling.LANCZOS))
            self.logo_photo_lg = ImageTk.PhotoImage(
                raw_logo.resize((80, 80), Image.Resampling.LANCZOS))
            self._has_logo = True
        except FileNotFoundError:
            self._has_logo = False

        self.circle_photos = [
            self._make_circle_photo(m["initials"], photo_path=m.get("photo_path"))
            for m in self.members
        ]

    def _build_shared_header(self):
        c = self.canvas

        if self._has_logo:
            self.hdr_logo_id = c.create_image(50, 60, image=self.logo_photo_sm, anchor="w")
        else:
            self.hdr_logo_id = c.create_text(50, 60, text="★",
                font=("Georgia", 24, "bold"), fill=self.yellow, anchor="w")

        self.hdr_univ_id = c.create_text(
            110, 60,
            text="Polytechnic University of the Philippines",
            font=self.font_left_header, fill=self.white, anchor="w")

        self.hdr_sep_id = c.create_line(0, 40, 0, 80, fill=self.white, width=1)

        self.title_font = font.Font(family="Georgia", size=13, weight="bold")
        self.title_segments = [
            ("Mula Sa'Yo, Para sa Bayan   ", self.white),
            ("|",                            self.white),
            ("    DANAS",                    self.white),
        ]
        self.hdr_title_ids = []
        for text, color in self.title_segments:
            self.hdr_title_ids.append(
                c.create_text(0, 0, text=text, font=self.title_font,
                              fill=color, anchor="w"))

        self.desc_font = font.Font(family="Georgia", size=12, weight="bold")
        self.hdr_desc_segments = [
            ("D", self.yellow), ("igital ",   self.white),
            ("A", self.yellow), ("cademy for ", self.white),
            ("N", self.yellow), ("avigating ", self.white),
            ("A", self.yellow), ("cademic ",  self.white),
            ("S", self.yellow), ("tudies",    self.white),
        ]
        self.hdr_desc_ids = []
        for text, color in self.hdr_desc_segments:
            self.hdr_desc_ids.append(
                c.create_text(0, 0, text=text, font=self.desc_font,
                              fill=color, anchor="w"))

        self.credit_id = c.create_text(
            50, 100,
            text="POLYTECHNIC UNIVERSITY OF THE PHILIPPINES\n"
                 "PHOTO: JAMES ONA\nCOMMUNICATION MANAGEMENT OFFICE",
            font=("Georgia", 9), fill="#a0a0a0", anchor="sw", justify="left")

        self.info_btn_oval = c.create_oval(
            0, 0, 0, 0, fill=self.maroon_card, outline=self.yellow, width=2)
        self.info_btn_text = c.create_text(
            0, 0, text="!", font=("Georgia", 14, "bold"),
            fill=self.yellow, anchor="center")

        for tag in (self.info_btn_oval, self.info_btn_text):
            c.tag_bind(tag, "<Button-1>", lambda e: self._show_info_page())
            c.tag_bind(tag, "<Enter>",
                lambda e: (c.itemconfig(self.info_btn_oval, fill="#5a0f11"),
                           c.config(cursor="hand2")))
            c.tag_bind(tag, "<Leave>",
                lambda e: (c.itemconfig(self.info_btn_oval, fill=self.maroon_card),
                           c.config(cursor="")))

    def _build_login_page(self):
        c = self.canvas

        self.lp_card = c.create_rectangle(
            0, 0, 0, 0, fill=self.maroon, outline="", stipple="gray75")

        self.lp_header = c.create_text(
            0, 0, text="Log in",
            font=("Georgia", 24, "bold"), fill=self.white, anchor="nw")

        self.lp_user_frame = tk.Frame(
            self.root, bg="#ffffff", bd=1, relief="flat", width=340, height=55)
        self.lp_user_frame.pack_propagate(False)
        tk.Label(self.lp_user_frame, text="ID Student/Faculty",
                 font=self.font_small_serif, fg="#000000", bg="#ffffff"
                 ).pack(anchor="w", padx=10, pady=(4, 0))
        self.user_entry = tk.Entry(
            self.lp_user_frame, font=self.font_serif,
            fg="#000000", bg="#ffffff", bd=0, highlightthickness=0)
        self.user_entry.pack(fill="x", padx=14, pady=(2, 2))
        self.lp_user_win = c.create_window(0, 0, window=self.lp_user_frame, anchor="nw")

        self.lp_pass_frame = tk.Frame(
            self.root, bg="#ffffff", bd=1, relief="flat", width=340, height=55)
        self.lp_pass_frame.pack_propagate(False)
        tk.Label(self.lp_pass_frame, text="Password",
                 font=self.font_small_serif, fg="#000000", bg="#ffffff"
                 ).pack(anchor="w", padx=10, pady=(4, 0))
        self.pass_entry = tk.Entry(
            self.lp_pass_frame, font=self.font_serif,
            fg="#000000", bg="#ffffff", bd=0, highlightthickness=0, show="•")
        self.pass_entry.pack(fill="x", padx=14, pady=(2, 2))
        self.lp_pass_win = c.create_window(0, 0, window=self.lp_pass_frame, anchor="nw")

        self.lp_login_btn = tk.Button(
            self.root, text="Log In",
            bg=self.maroon_btn, fg=self.white, font=self.font_serif_bold,
            bd=0, padx=25, pady=6,
            activebackground="#4a0507", activeforeground=self.white,
            cursor="hand2", command=self.handle_main_login)
        self.lp_login_win = c.create_window(0, 0, window=self.lp_login_btn, anchor="nw")

        self.lp_forgot = c.create_text(
            0, 0, text="Forgot Password?",
            font=self.font_serif_italic, fill=self.white, anchor="ne")
        c.tag_bind(self.lp_forgot, "<Button-1>",
                   lambda e: self.open_forgot_password_window())
        c.tag_bind(self.lp_forgot, "<Enter>",
                   lambda e: c.config(cursor="hand2"))
        c.tag_bind(self.lp_forgot, "<Leave>",
                   lambda e: c.config(cursor=""))

        self.lp_ca_frame = tk.Frame(
            self.root, bg="#ffffff", bd=0, width=155, height=38)
        self.lp_ca_frame.pack_propagate(False)
        tk.Button(
            self.lp_ca_frame, text="Create an Account",
            font=self.font_serif_underline,
            fg=self.maroon_card, bg="#ffffff", bd=0,
            activebackground="#eeeeee", activeforeground=self.maroon_card,
            cursor="hand2", command=self.open_create_account_window
        ).pack(fill="both", expand=True)
        self.lp_ca_win = c.create_window(0, 0, window=self.lp_ca_frame, anchor="nw")

        self._login_canvas_items = [
            self.lp_card, self.lp_header,
            self.lp_user_win, self.lp_pass_win,
            self.lp_login_win, self.lp_forgot, self.lp_ca_win,
        ]

    def _build_info_page(self):
        c = self.canvas

        self.ip_back_rect = c.create_rectangle(
            0, 0, 0, 0,
            fill=self.maroon_btn, outline=self.yellow, width=1, state="hidden")
        self.ip_back_text = c.create_text(
            0, 0, text="← Back",
            font=("Georgia", 10, "bold"), fill=self.white,
            anchor="center", state="hidden")

        for tag in (self.ip_back_rect, self.ip_back_text):
            c.tag_bind(tag, "<Button-1>", lambda e: self._show_login_page())
            c.tag_bind(tag, "<Enter>",
                lambda e: (c.itemconfig(self.ip_back_rect, fill="#4a0507"),
                           c.config(cursor="hand2")))
            c.tag_bind(tag, "<Leave>",
                lambda e: (c.itemconfig(self.ip_back_rect, fill=self.maroon_btn),
                           c.config(cursor="")))

        self.ip_logo = c.create_image(
            0, 0, anchor="center",
            image=self.logo_photo_lg if self._has_logo else None,
            state="hidden")

        self.ip_title = c.create_text(
            0, 0, text="DANAS",
            font=("Georgia", 26, "bold"), fill=self.yellow,
            anchor="center", state="hidden")

        self.ip_desc_font = font.Font(family="Georgia", size=13, weight="bold")
        self.ip_desc_segments = [
            ("D", self.yellow), ("igital ",    self.white),
            ("A", self.yellow), ("cademy for ", self.white),
            ("N", self.yellow), ("avigating ", self.white),
            ("A", self.yellow), ("cademic ",   self.white),
            ("S", self.yellow), ("tudies",     self.white),
        ]
        self.ip_desc_ids = []
        for text, color in self.ip_desc_segments:
            self.ip_desc_ids.append(
                c.create_text(0, 0, text=text, font=self.ip_desc_font,
                              fill=color, anchor="w", state="hidden"))

        self.ip_divider = c.create_line(
            0, 0, 0, 0, fill=self.yellow, width=1, state="hidden")

        self.ip_about = c.create_text(
            0, 0, text="",
            font=("Georgia", 11),
            fill=self.white,
            anchor="n",
            justify="center",
            state="hidden")

        self.profile_circle_ids = []
        self.profile_name_ids = []
        self.profile_role_ids = []

        for i, member in enumerate(self.members):
            img_id = c.create_image(0, 0, image=self.circle_photos[i],
                                    anchor="center", state="hidden")

            name_id = c.create_text(
                0, 0,
                text=member["name"],
                font=("Georgia", 9, "bold"),
                fill=self.white,
                anchor="center",
                state="hidden",
                width=120,
                justify="center")

            role_id = c.create_text(0, 0, text=member["role"],
                                    font=("Georgia", 8, "italic"), fill=self.yellow,
                                    anchor="center", state="hidden")

            idx = i
            for tag in (img_id, name_id, role_id):
                c.tag_bind(tag, "<Button-1>", lambda e, n=idx: self._open_profile_panel(n))
                c.tag_bind(tag, "<Enter>", lambda e: c.config(cursor="hand2"))
                c.tag_bind(tag, "<Leave>", lambda e: c.config(cursor=""))

            self.profile_circle_ids.append(img_id)
            self.profile_name_ids.append(name_id)
            self.profile_role_ids.append(role_id)

        self._info_canvas_items = (
            [self.ip_back_rect, self.ip_back_text,
             self.ip_logo, self.ip_title, self.ip_divider, self.ip_about]
            + self.ip_desc_ids
            + self.profile_circle_ids
            + self.profile_name_ids
            + self.profile_role_ids
        )

        c.tag_raise(self.ip_logo)
        c.tag_raise(self.ip_title)
        for sid in self.ip_desc_ids:
            c.tag_raise(sid)
        for pid in self.profile_circle_ids + self.profile_name_ids + self.profile_role_ids:
            c.tag_raise(pid)
        c.tag_raise(self.ip_back_rect)
        c.tag_raise(self.ip_back_text)

    def _open_profile_panel(self, index):
        member = self.members[index]

        panel = tk.Toplevel(self.root)
        panel.title(member["name"])
        panel.configure(bg=self.maroon_card)
        panel.resizable(False, False)
        panel.transient(self.root)
        panel.grab_set()

        pw, ph = 440, 600
        px = self.root.winfo_x() + self.root.winfo_width() - pw - 20
        py = self.root.winfo_y() + (self.root.winfo_height() - ph) // 2
        panel.geometry(f"{pw}x{ph}+{px}+{py}")

        header = tk.Frame(panel, bg=self.maroon_btn, height=6)
        header.pack(fill="x")

        outer = tk.Frame(panel, bg=self.maroon_card)
        outer.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(outer, orient="vertical", bg=self.maroon_card,
                                 troughcolor=self.maroon, activebackground=self.yellow)
        scrollbar.pack(side="right", fill="y")

        inner_canvas = tk.Canvas(outer, bg=self.maroon_card, bd=0,
                                 highlightthickness=0,
                                 yscrollcommand=scrollbar.set)
        inner_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=inner_canvas.yview)

        content = tk.Frame(inner_canvas, bg=self.maroon_card)
        content_window = inner_canvas.create_window((0, 0), window=content, anchor="nw")

        def on_configure(event):
            inner_canvas.configure(scrollregion=inner_canvas.bbox("all"))
            inner_canvas.itemconfig(content_window, width=inner_canvas.winfo_width())

        content.bind("<Configure>", on_configure)
        inner_canvas.bind("<Configure>",
            lambda e: inner_canvas.itemconfig(content_window, width=e.width))

        def _on_mousewheel(event):
            inner_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        inner_canvas.bind("<MouseWheel>", _on_mousewheel)
        content.bind("<MouseWheel>", _on_mousewheel)

        circle_lbl = tk.Label(content, image=self.circle_photos[index],
                              bg=self.maroon_card)
        circle_lbl.pack(pady=(20, 6))
        circle_lbl.bind("<MouseWheel>", _on_mousewheel)

        tk.Label(content, text=member["name"],
                 font=("Georgia", 13, "bold"), fg=self.yellow,
                 bg=self.maroon_card).pack()

        tk.Label(content, text=member["position"],
                 font=("Georgia", 10, "italic"), fg=self.white,
                 bg=self.maroon_card).pack(pady=(2, 10))

        sep = tk.Frame(content, bg=self.yellow, height=1)
        sep.pack(fill="x", padx=30, pady=(0, 12))

        fields = [
            ("Position",            member["position"]),
            ("Gender",              member["gender"]),
            ("City Address",        member["city_address"]),
            ("Provincial Address",  member["provincial_address"]),
            ("Cellphone No.",       member["cellphone"]),
            ("Email",               member["email"]),
            ("Date of Birth",       member["dob"]),
            ("Height",              member["height"]),
            ("Religion",            member["religion"]),
            ("Civil Status",        member["civil_status"]),
            ("Message",             member["message"]),
        ]

        info_frame = tk.Frame(content, bg=self.maroon_card)
        info_frame.pack(fill="x", padx=30)
        info_frame.bind("<MouseWheel>", _on_mousewheel)

        for label, value in fields:
            row = tk.Frame(info_frame, bg=self.maroon_card)
            row.pack(fill="x", pady=2)
            row.bind("<MouseWheel>", _on_mousewheel)
            tk.Label(row, text=label + ":", font=("Georgia", 9, "bold"),
                     fg=self.yellow, bg=self.maroon_card, width=18, anchor="w"
                     ).pack(side="left")
            tk.Label(row, text=value, font=("Georgia", 9),
                     fg=self.white, bg=self.maroon_card, anchor="w",
                     wraplength=220, justify="left"
                     ).pack(side="left", fill="x", expand=True)

        tk.Button(content, text="Close", font=self.font_serif_bold,
                  bg=self.maroon_btn, fg=self.white, bd=0,
                  padx=20, pady=5, cursor="hand2",
                  activebackground="#4a0507", activeforeground=self.white,
                  command=panel.destroy).pack(pady=18)

    @property
    def _navbar_items(self):
        return (
            [self.hdr_logo_id, self.hdr_univ_id, self.hdr_sep_id]
            + self.hdr_title_ids
            + self.hdr_desc_ids
        )

    def _show_login_page(self):
        for item in self._info_canvas_items:
            self.canvas.itemconfig(item, state="hidden")

        for item in self._navbar_items:
            self.canvas.itemconfig(item, state="normal")

        self.canvas.itemconfig(self.info_btn_oval, state="normal")
        self.canvas.itemconfig(self.info_btn_text, state="normal")

        for item in self._login_canvas_items:
            self.canvas.itemconfig(item, state="normal")

        self._layout_login()
        self._layout_header()

    def _show_info_page(self):
        for item in self._login_canvas_items:
            self.canvas.itemconfig(item, state="hidden")

        for item in self._navbar_items:
            self.canvas.itemconfig(item, state="hidden")

        self.canvas.itemconfig(self.info_btn_oval, state="hidden")
        self.canvas.itemconfig(self.info_btn_text, state="hidden")

        for item in self._info_canvas_items:
            self.canvas.itemconfig(item, state="normal")

        self._layout_info()

    def _layout_header(self):
        c = self.canvas
        w = self.root.winfo_width()

        c.coords(self.hdr_logo_id, 50, 60)
        c.coords(self.hdr_univ_id, 110, 60)

        bbox = c.bbox(self.hdr_univ_id)
        sep_x = (bbox[2] if bbox else 360) + 30
        c.coords(self.hdr_sep_id, sep_x, 40, sep_x, 80)

        cx = w // 2

        total_w = sum(self.title_font.measure(t) for t, _ in self.title_segments)
        x = cx - total_w // 2
        for i, sid in enumerate(self.hdr_title_ids):
            t, _ = self.title_segments[i]
            c.coords(sid, x, 52)
            x += self.title_font.measure(t)

        total_w = sum(self.desc_font.measure(t) for t, _ in self.hdr_desc_segments)
        x = cx - total_w // 2
        for i, sid in enumerate(self.hdr_desc_ids):
            t, _ = self.hdr_desc_segments[i]
            c.coords(sid, x, 74)
            x += self.desc_font.measure(t)

        r, bx, by = 18, w - 35, 35
        c.coords(self.info_btn_oval, bx - r, by - r, bx + r, by + r)
        c.coords(self.info_btn_text, bx, by)
        c.tag_raise(self.info_btn_oval)
        c.tag_raise(self.info_btn_text)

    def _layout_login(self):
        c = self.canvas
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        cw, ch = 430, 530
        cx1 = (w - cw) // 2
        cy1 = (h - ch) // 2 + 50
        cx2 = cx1 + cw

        px = 45
        c.coords(self.lp_card,      cx1,       cy1,       cx2,       cy1 + ch)
        c.coords(self.lp_header,    cx1 + px,  cy1 + 50)
        c.coords(self.lp_user_win,  cx1 + px,  cy1 + 140)
        c.coords(self.lp_pass_win,  cx1 + px,  cy1 + 225)

        row_y = cy1 + 320
        c.coords(self.lp_login_win, cx1 + px,  row_y)
        c.coords(self.lp_forgot,    cx2 - px,  row_y + 15)
        c.coords(self.lp_ca_win,    cx1 + px,  cy1 + 420)
        c.coords(self.credit_id,    50,         h - 50)

    def _layout_info(self):
        c = self.canvas
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        cx = w // 2

        bw, bh = 120, 34
        bx1, by1 = 30, 15
        c.coords(self.ip_back_rect, bx1, by1, bx1 + bw, by1 + bh)
        c.coords(self.ip_back_text, bx1 + bw // 2, by1 + bh // 2)

        logo_y = h // 2 - 360
        c.coords(self.ip_logo, cx, logo_y)

        title_y = logo_y + 60
        c.coords(self.ip_title, cx, title_y)

        desc_y = title_y + 42
        total_w = sum(self.ip_desc_font.measure(t) for t, _ in self.ip_desc_segments)
        x = cx - total_w // 2
        for i, sid in enumerate(self.ip_desc_ids):
            t, _ = self.ip_desc_segments[i]
            c.coords(sid, x, desc_y)
            x += self.ip_desc_font.measure(t)

        profile_top = desc_y + 150
        circle_r = 70
        total_members = len(self.members)
        per_row = 6
        col_spacing = min(170, (w - 80) // per_row)

        for i in range(total_members):
            row = i // per_row
            col = i % per_row
            total_in_row = min(per_row, total_members - row * per_row)
            row_width = total_in_row * col_spacing
            row_start_x = cx - row_width // 2 + col_spacing // 2
            px_pos = row_start_x + col * col_spacing
            py_pos = profile_top + row * 180

            c.coords(self.profile_circle_ids[i], px_pos, py_pos)
            c.coords(self.profile_name_ids[i],   px_pos, py_pos + circle_r + 18)
            c.coords(self.profile_role_ids[i],   px_pos, py_pos + circle_r + 42)

        c.coords(self.credit_id, 50, h - 50)

        c.tag_raise(self.ip_logo)
        c.tag_raise(self.ip_title)
        for sid in self.ip_desc_ids:
            c.tag_raise(sid)
        for pid in self.profile_circle_ids + self.profile_name_ids + self.profile_role_ids:
            c.tag_raise(pid)
        c.tag_raise(self.ip_back_rect)
        c.tag_raise(self.ip_back_text)

    def _on_resize(self, event):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if w < 100 or h < 100:
            return

        if self.blurred_bg:
            resized = self.blurred_bg.resize((w, h), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized)
            self.canvas.itemconfig(self.bg_img_id, image=self.bg_photo)

        login_visible = (
            self.canvas.itemcget(self.lp_card, "state") == "normal")
        if login_visible:
            self._layout_header()
            self._layout_login()
        else:
            self._layout_info()

    def handle_main_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not username or not password:
            err = tk.Toplevel(self.root)
            err.title("Error")
            err.geometry("320x150")
            err.configure(bg=self.maroon_card)
            err.resizable(False, False)
            err.transient(self.root)
            err.grab_set()
            mx = self.root.winfo_x() + self.root.winfo_width() // 2 - 160
            my = self.root.winfo_y() + self.root.winfo_height() // 2 - 75
            err.geometry(f"+{mx}+{my}")
            tk.Label(err, text="Error, Try again!",
                 font=self.font_serif_bold, fg=self.white,
                 bg=self.maroon_card).pack(pady=(30, 15))
            tk.Button(err, text="Okay", font=self.font_serif,
                  bg=self.maroon_btn, fg=self.white, bd=0,
                  padx=20, pady=4, command=err.destroy).pack()
        else:
            user = database1.login_user(username, password)
            if user is None:
                messagebox.showerror("Login Failed", "Incorrect username or password.")
            else:
                self.open_role_selection_window(user)

    def open_role_selection_window(self, user):
        win = tk.Toplevel(self.root)
        win.title("Select Role")
        win.geometry("400x220")
        win.configure(bg=self.maroon_card)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()
        rx = self.root.winfo_x() + self.root.winfo_width() // 2 - 200
        ry = self.root.winfo_y() + self.root.winfo_height() // 2 - 110
        win.geometry(f"+{rx}+{ry}")

        tk.Label(win, text="Student or Faculty",
                 font=("Georgia", 16, "bold"), fg=self.white,
                 bg=self.maroon_card).pack(pady=(25, 5))
        tk.Label(win, text="Please select your portal navigation role:",
                 font=self.font_serif_italic, fg=self.white,
                 bg=self.maroon_card).pack(pady=(0, 20))

        def grant(role):
            if role.lower() != (user.get("role") or "").lower():
                access_denied()
                return
            win.destroy()
            self.root.withdraw()
 
            if role.lower() == "faculty":
                from Faculty import FacultyDashboard          # your existing import
                dashboard_root = tk.Toplevel(self.root)
                dashboard_root.protocol("WM_DELETE_WINDOW", self.root.destroy)
                FacultyDashboard(dashboard_root, user_id=user["id"])
 
            else:  # student
                from Database import student_engine
                from Student import StudentDashboard

                profile = student_engine.get_user_profile(user["username"])

                dashboard_root = tk.Toplevel(self.root)
                dashboard_root.protocol("WM_DELETE_WINDOW", self.root.destroy)
                StudentDashboard(dashboard_root, student_engine, profile)

        def access_denied():
            ad = tk.Toplevel(win)
            ad.title("Access Denied")
            ad.geometry("340x150")
            ad.configure(bg=self.maroon)
            ad.resizable(False, False)
            ad.transient(win)
            ad.grab_set()
            ax = win.winfo_x() + win.winfo_width() // 2 - 170
            ay = win.winfo_y() + win.winfo_height() // 2 - 75
            ad.geometry(f"+{ax}+{ay}")
            tk.Label(ad, text="You don't have access",
                     font=self.font_serif_bold, fg=self.white,
                     bg=self.maroon).pack(pady=(35, 15))
            tk.Button(ad, text="Okay", font=self.font_serif,
                      bg=self.maroon_card, fg=self.white, bd=0,
                      padx=25, pady=4, command=ad.destroy).pack()

        bf = tk.Frame(win, bg=self.maroon_card)
        bf.pack()
        tk.Button(bf, text="Student", font=self.font_serif_bold,
                  bg=self.yellow, fg=self.black, bd=0, padx=20, pady=8,
                  width=10, command=lambda: grant("student")
                  ).grid(row=0, column=0, padx=10)
        tk.Button(bf, text="Faculty", font=self.font_serif_bold,
                  bg=self.maroon_btn, fg=self.white, bd=0, padx=20, pady=8,
                  width=10, command=lambda: grant("faculty")
                  ).grid(row=0, column=1, padx=10)

    def open_create_account_window(self):
        win = tk.Toplevel(self.root)
        win.title("Create an Account")
        win.geometry("450x450")
        win.configure(bg=self.maroon_card)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()
        cx = self.root.winfo_x() + self.root.winfo_width() // 2 - 225
        cy = self.root.winfo_y() + self.root.winfo_height() // 2 - 195
        win.geometry(f"+{cx}+{cy}")

        tk.Label(win, text="Create a New Account",
                 font=("Georgia", 18, "bold"), fg=self.white,
                 bg=self.maroon_card).pack(pady=(25, 20))

        entries = {}
        for field in ["Full Name", "PUP ID", "Email", "Password"]:
            tk.Label(win, text=field, font=self.font_small_serif,
                     fg=self.yellow, bg=self.maroon_card
                     ).pack(anchor="w", padx=55, pady=(8, 2))
            e = tk.Entry(win, font=self.font_serif, bd=0, width=32)
            e.pack(ipady=6, padx=55)
            if field == "Password":
                e.config(show="•")
            entries[field] = e

        def submit():
            name     = entries["Full Name"].get().strip()
            username = entries["PUP ID"].get().strip()
            email    = entries["Email"].get().strip()
            password = entries["Password"].get().strip()

            print(f"name={name}, username={username}, email={email}, password={password}")  # ← debug

            if not name or not username or not email or not password:
                messagebox.showerror("Validation Error", "All fields are required.", parent=win)
                return

            try:
                success = database1.create_user(name, username, password, email)
                print(f"Result: {success}")
                if success:
                    messagebox.showinfo("Account Created", "Your registration was successful!", parent=win)
                    win.destroy()
                else:
                    messagebox.showerror("Error", "That username is already taken.", parent=win)
            except Exception as ex:
                print(f"Error: {ex}") 
                messagebox.showerror("Error", str(ex), parent=win)

        tk.Button(win, text="Submit Registration",
                  font=self.font_serif_bold, bg=self.yellow, fg=self.black,
                  bd=0, width=28, pady=6, command=submit
                  ).pack(pady=(30, 10))

    def open_forgot_password_window(self):
        self._otp_code = None

        win = tk.Toplevel(self.root)
        win.title("Reset Password Portal")
        win.geometry("450x280")
        win.configure(bg=self.maroon_card)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()
        fx = self.root.winfo_x() + self.root.winfo_width() // 2 - 225
        fy = self.root.winfo_y() + self.root.winfo_height() // 2 - 140
        win.geometry(f"+{fx}+{fy}")

        def clear():
            for w in win.winfo_children():
                w.destroy()

        def step1():
            clear(); win.geometry("450x280")
            tk.Label(win, text="Reset Password", font=("Georgia", 16, "bold"),
                    fg=self.white, bg=self.maroon_card).pack(pady=(30, 20))
            tk.Label(win, text="Enter your registered Email",
                    font=self.font_small_serif, fg=self.yellow,
                    bg=self.maroon_card).pack(anchor="w", padx=55, pady=(0, 4))
            e = tk.Entry(win, font=self.font_serif, bd=0, width=32)
            e.pack(ipady=6, padx=55)
            status = tk.Label(win, text="", font=self.font_serif_italic,
                            fg=self.yellow, bg=self.maroon_card)
            status.pack(pady=(8, 0))

            def go():
                email = e.get().strip()
                if not email:
                    messagebox.showerror("Error", "Please enter your email.", parent=win)
                    return
                user = database1.get_user_by_email(email)  # ← changed
                if user is None:
                    messagebox.showerror("Error", "No account found with that email.", parent=win)
                    return
                otp = database1.generate_otp()
                self._otp_code = otp
                self._reset_username = user["username"]
                status.config(text="Sending OTP...")
                win.update()
                sent = database1.send_otp_email(email, otp)
                if sent:
                    step2()
                else:
                    messagebox.showerror("Error", "Failed to send email.", parent=win)

            tk.Button(win, text="Submit", font=self.font_serif_bold,
                    bg=self.yellow, fg=self.black, bd=0, width=28,
                    pady=6, command=go).pack(pady=(15, 10))

        def step2():
            clear(); win.geometry("450x300")
            tk.Label(win, text="Check Your Email", font=("Georgia", 16, "bold"),
                    fg=self.white, bg=self.maroon_card).pack(pady=(30, 8))
            tk.Label(win, text="We sent a 6-digit OTP to your email.",
                    font=self.font_serif_italic, fg=self.white,
                    bg=self.maroon_card).pack(pady=(0, 16))
            tk.Label(win, text="Enter OTP Code", font=self.font_small_serif,
                    fg=self.yellow, bg=self.maroon_card
                    ).pack(anchor="w", padx=55, pady=(0, 4))
            e = tk.Entry(win, font=self.font_serif, bd=0, width=32)
            e.pack(ipady=6, padx=55)

            def verify():
                if e.get().strip() == self._otp_code:
                    step3()
                else:
                    messagebox.showerror("Invalid OTP", "The code you entered is incorrect.", parent=win)

            tk.Button(win, text="Submit", font=self.font_serif_bold,
                    bg=self.yellow, fg=self.black, bd=0, width=28,
                    pady=6, command=verify).pack(pady=(25, 10))

        def step3():
            clear(); win.geometry("450x310")
            tk.Label(win, text="Create a New Password",
                    font=("Georgia", 16, "bold"), fg=self.white,
                    bg=self.maroon_card).pack(pady=(30, 20))
            tk.Label(win, text="New Password", font=self.font_small_serif,
                    fg=self.yellow, bg=self.maroon_card
                    ).pack(anchor="w", padx=55, pady=(0, 4))
            e = tk.Entry(win, font=self.font_serif, bd=0, width=32, show="•")
            e.pack(ipady=6, padx=55)
            msg = tk.Label(win, text="", font=self.font_serif_italic,
                        fg=self.yellow, bg=self.maroon_card)
            msg.pack(pady=(10, 0))

            def save():
                new_pass = e.get().strip()
                if not new_pass:
                    messagebox.showerror("Error", "Please enter a new password.", parent=win)
                    return
                database1.update_password(self._reset_username, new_pass)
                e.config(state="disabled")
                btn.config(state="disabled")
                msg.config(text="✓ Password updated successfully!")

            btn = tk.Button(win, text="Submit", font=self.font_serif_bold,
                            bg=self.yellow, fg=self.black, bd=0, width=28,
                            pady=6, command=save)
            btn.pack(pady=(16, 10))

        step1()


if __name__ == "__main__":
    root = tk.Tk()
    app = DANASLogin(root)
    root.mainloop()
