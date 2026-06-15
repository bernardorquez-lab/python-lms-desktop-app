import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageFilter
import os
import shutil
import sys
from pathlib import Path

# ── resolve project root so imports work regardless of cwd ───────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


class StudentDashboard:
    def __init__(self, root, engine, user_profile):
        """
        Parameters
        ----------
        root         : tk.Tk / tk.Toplevel
        engine       : student_engine module  (import student_engine as engine)
        user_profile : dict with at least {'full_name': ..., 'username': ...}
                       Build it with  engine.get_user_profile(username)
        """
        self.root = root
        self.engine = engine
        self.user_profile = user_profile

        self.root.title("DANAS - Student Dashboard")
        try:
            self.root.state('zoomed')
        except tk.TclError:
            self.root.attributes('-zoomed', True)
        self.root.resizable(False, False)
        self.main_panel = None

        # ── asset paths (same pattern as FacultyDashboard) ───────────────
        BG_IMAGE   = PROJECT_ROOT / "Assets" / "img 3.png"
        LOGO_IMAGE = PROJECT_ROOT / "Assets" / "img 2.png"

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.raw_bg = None

        self.canvas = tk.Canvas(
            root, width=screen_w, height=screen_h,
            highlightthickness=0, bg="#1a0000"
        )
        self.canvas.pack(fill="both", expand=True)

        try:
            raw = (
                Image.open(BG_IMAGE)
                .resize((screen_w, screen_h), Image.Resampling.LANCZOS)
                .filter(ImageFilter.GaussianBlur(2))
            )
            self.raw_bg = raw.convert("RGBA")
            self.bg_photo = ImageTk.PhotoImage(raw)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception:
            pass

        try:
            logo = Image.open(LOGO_IMAGE).resize((60, 60))
            self.logo_photo = ImageTk.PhotoImage(logo)
            self.canvas.create_image(95, 75, image=self.logo_photo)
        except Exception:
            pass

        self.canvas.create_text(
            260, 75,
            text="Polytechnic University of the\nPhilippines",
            fill="white", font=("Georgia", 13, "bold"), justify="left"
        )

        # ── layout constants ──────────────────────────────────────────────
        self.PANEL_X = 420
        self.PANEL_Y = 200
        self.PANEL_W = screen_w - 420 - 60
        self.PANEL_H = screen_h - 200 - 80

        # ── sidebar ───────────────────────────────────────────────────────
        sidebar = tk.Frame(
            root, width=330, height=int(screen_h * 0.75),
            highlightbackground="white", highlightthickness=1
        )
        sidebar.pack_propagate(False)
        self._apply_frame_bg(sidebar, 60, 150, 330, int(screen_h * 0.75))
        self.canvas.create_window(60, 150, anchor="nw", window=sidebar)

        tk.Label(sidebar, text="👤", bg="#6b0f0f", fg="#dba413",
                 font=("Arial", 42)).pack(pady=(20, 5))
        tk.Label(sidebar, text=self.user_profile.get("full_name", "Student"),
                 bg="#6b0f0f", fg="white",
                 font=("Georgia", 14, "bold")).pack()
        tk.Label(sidebar, text="Student Portal", bg="#6b0f0f", fg="#aaaaaa",
                 font=("Georgia", 11)).pack(pady=(0, 10))
        tk.Frame(sidebar, bg="#dba413", height=1).pack(fill="x", padx=20, pady=10)

        for text, cmd in [
            ("📚    View Enrolled Courses", self.view),
            ("➕         Enroll Course",    self.enroll),
        ]:
            tk.Button(
                sidebar, text=text, command=cmd,
                bg="#dba413", fg="#3d080a", relief="flat",
                font=("Georgia", 12), width=22, height=2
            ).pack(pady=6)

        tk.Button(
            sidebar, text="LOG OUT",
            bg="#dba413", fg="#3d080a", relief="flat",
            font=("Georgia", 12, "bold"), width=22, height=2,
            command=self.logout
        ).pack(side="bottom", pady=15)

        # ── dashboard title ───────────────────────────────────────────────
        content_cx = 420 + (screen_w - 420) // 2
        self.canvas.create_text(
            content_cx, 120,
            text="Student Dashboard",
            fill="white", font=("Georgia", 36, "bold"), anchor="center"
        )
        self.canvas.create_text(
            content_cx, 170,
            text="Digital Academy for Navigating Academic Studies",
            fill="#dba413", font=("Georgia", 14), anchor="center"
        )

        self.view()

    # ── helpers ───────────────────────────────────────────────────────────────

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()

    def _make_tinted_image(self, x, y, w, h):
        if self.raw_bg is None:
            return None
        bw, bh = self.raw_bg.size
        x, y   = max(0, x), max(0, y)
        w, h   = min(w, bw - x), min(h, bh - y)
        if w <= 0 or h <= 0:
            return None
        crop = self.raw_bg.crop((x, y, x + w, y + h))
        tint = Image.new("RGBA", crop.size, (160, 10, 10, 155))
        return Image.alpha_composite(crop, tint)

    def _apply_frame_bg(self, frame, x, y, w, h):
        img = self._make_tinted_image(x, y, w, h)
        if img is None:
            frame.config(bg="#6b0f0f")
            return
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(frame, image=photo, bd=0, highlightthickness=0)
        lbl.image = photo
        lbl.place(x=0, y=0, relwidth=1, relheight=1)
        lbl.lower()

    def clear_panel(self):
        if self.main_panel:
            self.main_panel.destroy()
        self.main_panel = tk.Frame(
            self.root,
            width=self.PANEL_W, height=self.PANEL_H,
            highlightbackground="#cc3333", highlightthickness=1
        )
        self.main_panel.pack_propagate(False)
        self._apply_frame_bg(
            self.main_panel,
            self.PANEL_X, self.PANEL_Y,
            self.PANEL_W, self.PANEL_H
        )
        self.canvas.create_window(
            self.PANEL_X, self.PANEL_Y,
            anchor="nw", window=self.main_panel
        )

    # ── 1. VIEW ENROLLED COURSES ──────────────────────────────────────────────

    def view(self):
        self.clear_panel()
        tk.Label(
            self.main_panel, text="📚 Your Courses",
            bg="#6b0f0f", fg="white", font=("Georgia", 26)
        ).pack(pady=10)

        container = tk.Frame(self.main_panel, bg="#6b0f0f")
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        enrolled_courses = self.engine.get_student_courses(
            self.user_profile["username"]
        )

        if not enrolled_courses:
            tk.Label(
                container,
                text="You have no enrolled courses yet.\nClick ➕ Enroll Course to get started.",
                bg="#6b0f0f", fg="#aaaaaa",
                font=("Georgia", 13), justify="center"
            ).pack(expand=True)
            return

        # scrollable table
        wrap = tk.Frame(container, bg="#6b0f0f")
        wrap.pack(fill="both", expand=True)

        sb = tk.Scrollbar(wrap)
        sb.pack(side="right", fill="y")

        cv = tk.Canvas(wrap, bg="#6b0f0f", highlightthickness=0)
        cv.pack(side="left", fill="both", expand=True)
        sb.config(command=cv.yview)
        cv.configure(yscrollcommand=sb.set)

        table = tk.Frame(cv, bg="#6b0f0f")
        win = cv.create_window((0, 0), window=table, anchor="nw")
        table.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.bind("<Configure>", lambda e: cv.itemconfig(win, width=e.width))
        cv.bind_all("<MouseWheel>",
                    lambda e: cv.yview_scroll(int(-1*(e.delta/120)), "units"))

        # header
        header = tk.Frame(table, bg="#8c1616")
        header.pack(fill="x", pady=(0, 2))
        for col, label in enumerate(["Course Name", "Code", "Action"]):
            tk.Label(
                header, text=label,
                bg="#8c1616", fg="#dba413",
                font=("Georgia", 11, "bold"),
                anchor="w", padx=8
            ).grid(row=0, column=col, sticky="ew", padx=(0, 10))
        header.grid_columnconfigure(0, weight=1)

        for i, course in enumerate(enrolled_courses):
            row_bg = "#3d080a" if i % 2 == 0 else "#4a0c0e"
            row = tk.Frame(table, bg=row_bg, pady=2)
            row.pack(fill="x")
            row.grid_columnconfigure(0, weight=1)

            tk.Button(
                row, text=f"  {course['name']}",
                bg=row_bg, fg="white",
                activebackground="#dba413", activeforeground="#3d080a",
                relief="flat", anchor="w",
                font=("Georgia", 12), cursor="hand2",
                command=lambda c=course: self.open_course_dashboard(c)
            ).grid(row=0, column=0, sticky="ew", padx=(8, 0))

            tk.Label(
                row, text=course["code"],
                bg=row_bg, fg="#cccccc",
                font=("Georgia", 11), width=8
            ).grid(row=0, column=1, padx=10)

            tk.Button(
                row, text="Unenroll",
                bg="#E92C2C", fg="white",
                activebackground="#c0392b",
                relief="flat", font=("Georgia", 10), cursor="hand2",
                command=lambda c=course["code"]: self.unenroll(c)
            ).grid(row=0, column=2, padx=(0, 8))

    # ── 2. UNENROLL ───────────────────────────────────────────────────────────

    def unenroll(self, code):
        if messagebox.askyesno("Unenroll", "Are you sure you want to drop this course?"):
            self.engine.unenroll_student(self.user_profile["username"], code)
            self.view()

    # ── 3. ENROLL ─────────────────────────────────────────────────────────────

    def enroll(self):
        self.clear_panel()
        tk.Label(
            self.main_panel, text="➕ Enroll in Courses",
            bg="#6b0f0f", fg="white", font=("Georgia", 26)
        ).pack(pady=10)

        # scrollable checklist
        wrap = tk.Frame(self.main_panel, bg="#6b0f0f")
        wrap.pack(fill="both", expand=True, padx=30, pady=10)

        sb = tk.Scrollbar(wrap)
        sb.pack(side="right", fill="y")

        cv = tk.Canvas(wrap, bg="#6b0f0f", highlightthickness=0)
        cv.pack(side="left", fill="both", expand=True)
        sb.config(command=cv.yview)
        cv.configure(yscrollcommand=sb.set)

        inner = tk.Frame(cv, bg="#6b0f0f")
        win = cv.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.bind("<Configure>", lambda e: cv.itemconfig(win, width=e.width))
        cv.bind_all("<MouseWheel>",
                    lambda e: cv.yview_scroll(int(-1*(e.delta/120)), "units"))

        all_courses     = self.engine.get_all_courses()
        student_codes   = {
            c["code"]
            for c in self.engine.get_student_courses(self.user_profile["username"])
        }

        self.check_vars = {}
        for course in all_courses:
            code        = course["code"]
            is_enrolled = code in student_codes
            var         = tk.BooleanVar(value=is_enrolled)
            self.check_vars[code] = var

            row = tk.Frame(inner, bg="#7a1212", pady=4)
            row.pack(fill="x", pady=3)

            chk = tk.Checkbutton(
                row, variable=var,
                bg="#7a1212", activebackground="#4a0c0e",
                selectcolor="#3d080a",
                fg="#dba413", activeforeground="#dba413",
                relief="flat", cursor="hand2"
            )
            chk.pack(side="left", padx=(10, 0))

            tk.Label(
                row, text=course["name"],
                bg="#7a1212", fg="white",
                font=("Georgia", 12), anchor="w", width=36
            ).pack(side="left")

            tk.Label(
                row, text=f"[{code}]",
                bg="#7a1212", fg="#aaaaaa",
                font=("Georgia", 11)
            ).pack(side="left", padx=10)

            if is_enrolled:
                chk.config(state="disabled")
                tk.Label(
                    row, text="✔ Enrolled",
                    bg="#7a1212", fg="#dba413",
                    font=("Georgia", 10, "italic")
                ).pack(side="left")

        tk.Button(
            self.main_panel, text="✔  Confirm Enrollment",
            bg="#dba413", fg="#3d080a",
            relief="flat", font=("Georgia", 13, "bold"),
            padx=20, pady=6,
            command=self._confirm_enrollment
        ).pack(pady=(0, 12))

    def _confirm_enrollment(self):
        newly_added = 0
        for code, var in self.check_vars.items():
            if var.get():
                if self.engine.enroll_student(self.user_profile["username"], code):
                    newly_added += 1

        if newly_added:
            messagebox.showinfo(
                "Enrolled",
                f"Successfully enrolled in {newly_added} course(s)!"
            )
            self.view()
        else:
            messagebox.showinfo("No Change", "No new courses were selected.")

    # ── 4. OPEN SPECIFIC COURSE ───────────────────────────────────────────────

    def open_course_dashboard(self, course):
        self.clear_panel()

        top = tk.Frame(self.main_panel, bg="#6b0f0f")
        top.pack(fill="x", padx=15, pady=(10, 0))

        tk.Button(
            top, text="← Back",
            command=self.view,
            bg="#dba413", fg="#3d080a",
            relief="flat", font=("Georgia", 11, "bold"), cursor="hand2"
        ).pack(side="left")

        tk.Label(
            top,
            text=f"{course['name']}  [{course['code']}]",
            bg="#6b0f0f", fg="white",
            font=("Georgia", 16, "bold")
        ).pack(side="left", padx=15)

        tk.Frame(self.main_panel, bg="#dba413", height=1).pack(
            fill="x", padx=15, pady=8
        )

        tab_bar = tk.Frame(self.main_panel, bg="#6b0f0f")
        tab_bar.pack(fill="x", padx=15)

        self._course_content = tk.Frame(self.main_panel, bg="#7a1212")
        self._course_content.pack(fill="both", expand=True, padx=15, pady=10)

        tabs = ["📋 Overview", "📄 Modules"]
        self._tab_buttons = {}
        for tab in tabs:
            btn = tk.Button(
                tab_bar, text=tab,
                bg="#8c1616", fg="#cccccc",
                relief="flat", font=("Georgia", 11),
                padx=14, pady=6,
                command=lambda t=tab: self._show_tab(t, course)
            )
            btn.pack(side="left", padx=2)
            self._tab_buttons[tab] = btn

        self._show_tab(tabs[0], course)

    def _show_tab(self, tab, course):
        for t, btn in self._tab_buttons.items():
            if t == tab:
                btn.config(bg="#dba413", fg="#3d080a", font=("Georgia", 11, "bold"))
            else:
                btn.config(bg="#8c1616", fg="#cccccc", font=("Georgia", 11))

        for w in self._course_content.winfo_children():
            w.destroy()

        # ── Overview tab ──────────────────────────────────────────────────
        if tab == "📋 Overview":
            tk.Label(
                self._course_content,
                text=f"Welcome to {course['name']}",
                bg="#7a1212", fg="#dba413",
                font=("Georgia", 15, "bold")
            ).pack(anchor="w", padx=20, pady=(15, 5))

            details = (
                f"{course.get('description', 'Welcome to this course.')}\n\n"
                f"Course Code : {course.get('code', 'N/A')}\n"
                f"Units       : {course.get('units', '3')}\n"
                f"Schedule    : {course.get('schedule', 'TBA')}\n"
                f"Room        : {course.get('room', 'TBA')}"
            )
            tk.Label(
                self._course_content,
                text=details,
                bg="#7a1212", fg="white",
                font=("Georgia", 12), justify="left"
            ).pack(anchor="w", padx=20)

        # ── Modules tab ───────────────────────────────────────────────────
        elif tab == "📄 Modules":
            wrap = tk.Frame(self._course_content, bg="#7a1212")
            wrap.pack(fill="both", expand=True)

            sb = tk.Scrollbar(wrap)
            sb.pack(side="right", fill="y")

            cv = tk.Canvas(wrap, bg="#7a1212", highlightthickness=0)
            cv.pack(side="left", fill="both", expand=True)
            sb.config(command=cv.yview)
            cv.configure(yscrollcommand=sb.set)

            inner = tk.Frame(cv, bg="#7a1212")
            win = cv.create_window((0, 0), window=inner, anchor="nw")
            inner.bind("<Configure>",
                       lambda e: cv.configure(scrollregion=cv.bbox("all")))
            cv.bind("<Configure>",
                    lambda e: cv.itemconfig(win, width=e.width))
            cv.bind_all("<MouseWheel>",
                        lambda e: cv.yview_scroll(int(-1*(e.delta/120)), "units"))

            # fetch real PDFs from the database
            course_id = course.get("course_id")
            materials = (
                self.engine.get_course_materials(course_id)
                if course_id else []
            )

            if not materials:
                tk.Label(
                    inner,
                    text="No modules uploaded yet.\nCheck back later!",
                    bg="#7a1212", fg="#aaaaaa",
                    font=("Georgia", 13), justify="center"
                ).pack(expand=True, pady=30)
                return

            for mat in materials:
                pdf_name = mat["pdf_name"]
                pdf_path = mat["pdf_path"]

                row = tk.Frame(inner, bg="#8c1616")
                row.pack(fill="x", padx=20, pady=2)

                tk.Label(
                    row, text="📄 " + pdf_name,
                    bg="#8c1616", fg="white",
                    font=("Georgia", 11), anchor="w"
                ).pack(side="left", padx=10, pady=6, fill="x", expand=True)

                btn_frame = tk.Frame(row, bg="#8c1616")
                btn_frame.pack(side="right", padx=10)

                tk.Button(
                    btn_frame, text="Download",
                    bg="#8c1616", fg="white",
                    relief="raised", font=("Georgia", 10), cursor="hand2",
                    command=lambda p=pdf_path, n=pdf_name: self.download_pdf(p, n)
                ).pack(side="right", padx=5)

                tk.Button(
                    btn_frame, text="View",
                    bg="yellow", fg="black",
                    relief="flat", font=("Georgia", 10), cursor="hand2",
                    command=lambda p=pdf_path: self.view_pdf(p)
                ).pack(side="right", padx=5)

    # ── 5. PDF FUNCTIONS ──────────────────────────────────────────────────────

    def view_pdf(self, file_path):
        if os.path.exists(file_path):
            try:
                os.startfile(file_path)          # Windows
            except AttributeError:
                import subprocess
                subprocess.call(["xdg-open", file_path])   # Linux / Mac
        else:
            messagebox.showwarning(
                "File Missing",
                "This PDF could not be found on disk.\n"
                "The faculty may have moved or deleted it."
            )

    def download_pdf(self, file_path, pdf_name):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=pdf_name
        )
        if not save_path:
            return

        if os.path.exists(file_path):
            try:
                shutil.copy(file_path, save_path)
                messagebox.showinfo("Success", f"'{pdf_name}' downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Download Error", str(e))
        else:
            messagebox.showwarning(
                "File Missing",
                "The original PDF could not be found.\n"
                "Please ask your faculty to re-upload it."
            )