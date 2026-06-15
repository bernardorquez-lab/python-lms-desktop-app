import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil
import sys
from pathlib import Path
from PIL import Image, ImageTk, ImageFilter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from Backend.course_manager import add_course as db_add_course
from Backend.course_manager import delete_course as db_delete_course
from Backend.course_manager import get_course_count, get_courses
from Backend.course_manager import update_course as db_update_course
from Backend.material_manager import add_material as db_add_material
from Backend.material_manager import delete_material as db_delete_material
from Backend.material_manager import get_materials, get_materials_by_course
from Database.database import initialize_database


class FacultyDashboard:
    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id
        self.root.title("DANAS - Faculty Dashboard")
        self.root.state("zoomed")
        self.root.resizable(False, False)
        
        self.main_panel = None
        self.pdf_files = []
        
        self.pdf_checked = {}
        self.pdf_paths = {}
        
        self.default_modules = [
            "Module 1 – Introduction & Course Overview",
            "Module 2 – Fundamental Concepts",
            "Module 3 – Core Techniques",
            "Module 4 – Practical Applications",
            "Module 5 – Midterm Review",
            "Module 6 – Advanced Topics"
        ]

        self.default_courses = [
            {"name": "Object-Oriented Programming", "code": "0113", "units": "3", "schedule": "MWF 08:00 - 09:30", "room": "GLE-301"},
            {"name": "Data Structures", "code": "0214", "units": "3", "schedule": "TTH 10:30 - 12:00", "room": "GLE-302"},
            {"name": "Database Systems", "code": "0315", "units": "3", "schedule": "MWF 13:00 - 14:30", "room": "LAB-101"},
            {"name": "Software Engineering", "code": "0416", "units": "3", "schedule": "TTH 14:00 - 15:30", "room": "GLE-405"},
            {"name": "Computer Networks", "code": "0517", "units": "3", "schedule": "Sat 08:00 - 11:00", "room": "LAB-203"},
        ]
        initialize_database()
        self._seed_courses_if_empty()
        self.courses = []
        self.load_courses()
        self.load_uploaded_pdfs()

        BG_IMAGE = PROJECT_ROOT / "Assets" / "img 3.png"
        LOGO_IMAGE = PROJECT_ROOT / "Assets" / "img 2.png"

        self.raw_bg = None

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        try:
            bg = Image.open(BG_IMAGE)
            bg = bg.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            bg = bg.filter(ImageFilter.GaussianBlur(2))
            self.raw_bg = bg
            self.bg_photo = ImageTk.PhotoImage(bg)

            self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        except Exception:
            self.canvas = tk.Canvas(
                root,
                width=screen_width,
                height=screen_height,
                bg="#120202",
                highlightthickness=0
            )
            self.canvas.pack(fill="both", expand=True)

        try:
            logo = Image.open(LOGO_IMAGE)
            logo = logo.resize((60, 60))
            self.logo_photo = ImageTk.PhotoImage(logo)
            self.canvas.create_image(95, 75, image=self.logo_photo)
        except Exception:
            pass

        self.canvas.create_text(
            260, 75,
            text="Polytechnic University of the\nPhilippines",
            fill="white",
            font=("Georgia", 13, "bold"),
            justify="left"
        )

        self.sidebar = tk.Frame(
            root,
            width=330,
            height=int(screen_height * 0.7),
            highlightbackground="white",
            highlightthickness=1
        )
        self.sidebar.pack_propagate(False)
        
        self._apply_frame_bg(self.sidebar, 60, 150, 330, int(screen_height * 0.7))

        self.canvas.create_window(
            60, 150,
            anchor="nw",
            window=self.sidebar
        )

        self.build_sidebar()

        content_centered = 60 + 330 + int((screen_width - (60 + 330)) / 2)

        self.canvas.create_text(
            content_centered, 120,
            text="Faculty Dashboard",
            fill="white",
            font=("Georgia", 42, "bold"),
            anchor="center"
        )

        self.canvas.create_text(
            content_centered, 180,
            text="Digital Academy for Navigating Academic Studies",
            fill="#dba413",
            font=("Georgia", 16),
            anchor="center"
        )

        self.panel_x = 60 + 330 + 50
        self.panel_y = 240
        self.panel_w = screen_width - self.panel_x - 60
        self.panel_h = screen_height - self.panel_y - 100

        self.show_course_list()

    def _seed_courses_if_empty(self):
        if get_course_count() > 0:
            return

        for course in self.default_courses:
            db_add_course(
                course["name"],
                course["code"],
                course["units"],
                course["schedule"],
                course["room"],
                "This course provides a comprehensive introduction to the subject.\n"
                "Attend all lectures, complete assignments on time, and review modules regularly."
            )

    def _course_from_row(self, row):
        return {
            "id": row[0],
            "checked": False,
            "name": row[1],
            "code": row[2],
            "units": row[3] or "",
            "schedule": row[4] or "",
            "room": row[5] or "",
            "description": row[6] or ""
        }

    def load_courses(self):
        checked_ids = {
            course.get("id")
            for course in getattr(self, "courses", [])
            if course.get("checked")
        }
        self.courses = [self._course_from_row(row) for row in get_courses()]
        for course in self.courses:
            course["checked"] = course.get("id") in checked_ids

    def load_uploaded_pdfs(self):
        self.pdf_files = []
        self.pdf_paths = {}
        for material in get_materials():
            filename = material[3]
            path = material[4]
            if filename not in self.pdf_files:
                self.pdf_files.append(filename)
                self.pdf_paths[filename] = path

        upload_dir = PROJECT_ROOT / "Uploads" / "PDFs"
        upload_dir.mkdir(parents=True, exist_ok=True)
        for pdf_path in upload_dir.glob("*.pdf"):
            if pdf_path.name not in self.pdf_files:
                self.pdf_files.append(pdf_path.name)
                self.pdf_paths[pdf_path.name] = str(pdf_path)

    def get_selected_courses(self):
        return [course for course in self.courses if course["checked"]]

    def assign_pdfs_to_courses(self, pdf_names, courses):
        assigned_count = 0

        for course in courses:
            existing_pdfs = {
                material[3]
                for material in get_materials_by_course(course["id"])
            }

            for pdf_name in pdf_names:
                if pdf_name in existing_pdfs:
                    continue

                db_add_material(
                    course["id"],
                    pdf_name,
                    pdf_name,
                    self.pdf_paths.get(pdf_name, "")
                )
                assigned_count += 1

        return assigned_count

    def open_pdf(self, path):
        if path and os.path.exists(path):
            os.startfile(path)
        else:
            messagebox.showwarning("File Missing", "The selected PDF file cannot be found.")

    def save_uploaded_pdf(self, filepath):
        filename = os.path.basename(filepath)
        upload_dir = PROJECT_ROOT / "Uploads" / "PDFs"
        upload_dir.mkdir(parents=True, exist_ok=True)
        destination = upload_dir / filename

        if Path(filepath).resolve() != destination.resolve():
            shutil.copy2(filepath, destination)

        if filename not in self.pdf_files:
            self.pdf_files.append(filename)
        self.pdf_paths[filename] = str(destination)
        return filename
    
    def _make_tinted_image(self, x, y, w, h):
        if self.raw_bg is None:
            return None
        bg_w, bg_h = self.raw_bg.size
        crop_x = min(max(0, x), bg_w)
        crop_y = min(max(0, y), bg_h)
        crop_w = min(w, bg_w - crop_x)
        crop_h = min(h, bg_h - crop_y)
        
        if crop_w <= 0 or crop_h <= 0:
            return None
            
        crop = self.raw_bg.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
        tint = Image.new("RGBA", crop.size, (160, 10, 10, 155))
        result = Image.alpha_composite(crop.convert("RGBA"), tint)
        return result

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

    def build_sidebar(self):
        profile_frame = tk.Frame(self.sidebar, bg="#630d10")
        profile_frame.pack(fill="x", pady=(20, 15))

        tk.Label(
            profile_frame,
            text="👤",
            bg="#630d10",
            fg="#dba413",
            font=("Arial", 42)
        ).pack()

        tk.Label(
            profile_frame,
            text="Faculty Portal",
            bg="#630d10",
            fg="white",
            font=("Georgia", 18)
        ).pack(pady=(5, 10))

        tk.Frame(self.sidebar, bg="#dba413", height=1).pack(
            fill="x", padx=20, pady=10
        )

        buttons = [
            ("📚         Course List", self.show_course_list),
            ("➕         Add Course", self.show_add_course),
            ("✏️         Edit Course", self.show_edit_course),
            ("🗂️   Upload PDFs", self.show_upload_pdf),
            ("🗑️   Delete Course", self.delete_checked_confirm),
        ]

        for text, cmd in buttons:
            tk.Button(
                self.sidebar,
                text=text,
                command=cmd,
                bg="#dba413",
                fg="#3d080a",
                relief="flat",
                font=("Georgia", 12),
                width=22,
                height=2
            ).pack(pady=6)

        tk.Button(
            self.sidebar,
            text="LOG OUT",
            bg="#dba413",
            fg="#3d080a",
            relief="flat",
            font=("Georgia", 12, "bold"),
            width=22,
            height=2,
            command=self.logout
        ).pack(side="bottom", pady=15)

    def clear_panel(self):
        if self.main_panel:
            self.main_panel.destroy()

        self.main_panel = tk.Frame(
            self.root,
            width=self.panel_w,
            height=self.panel_h,
            highlightbackground="#cc3333",
            highlightthickness=1
        )
        self.main_panel.pack_propagate(False)
        self._apply_frame_bg(self.main_panel, self.panel_x, self.panel_y, self.panel_w, self.panel_h)

        self.canvas.create_window(
            self.panel_x, self.panel_y,
            anchor="nw",
            window=self.main_panel
        )

    def show_course_list(self):
        self.load_courses()
        self.clear_panel()

        tk.Label(
            self.main_panel,
            text="📚 Course List",
            bg="#6b0f0f",
            fg="white",
            font=("Georgia", 26)
        ).pack(pady=10)

        tk.Frame(
            self.main_panel,
            bg="#ecbc43",
            height=2
        ).pack(fill="x", padx=40, pady=(0, 25))
        
        table_container = tk.Frame(self.main_panel, bg="#dba413")
        table_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        table_container.pack_propagate(False)
        
        scrollbar = tk.Scrollbar(table_container)
        scrollbar.pack(side="right", fill="y")
        
        canvas = tk.Canvas(
             table_container,
             bg="#dba413",
             highlightthickness=0
        )
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar.config(command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        table = tk.Frame(canvas, bg="#dba413")
        canvas_window = canvas.create_window(
             (0, 0),
             window=table,
             anchor="nw"
        )
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        table.bind("<Configure>", on_frame_configure)

        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)

        def _on_mousewheel(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        table.grid_columnconfigure(1, weight=1)

        tk.Label(
            table,
            text="Course Name",
            bg="#dba413",
            fg="#3d080a",
            font=("Georgia", 11, "bold")
        ).grid(row=0, column=1, sticky="w", padx=(10, 20), pady=(10, 8))

        tk.Label(
            table,
            text="Course Code",
            bg="#dba413",
            fg="#3d080a",
            font=("Georgia", 11, "bold")
        ).grid(row=0, column=2, padx=(20, 30), pady=(10, 8), sticky="e")

        tk.Frame(
            table,
            bg="#6b0f0f",
            height=1
        ).grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(0, 8)
        )

        for row, course in enumerate(self.courses, start=2):
            chk = "☑" if course["checked"] else "☐"

            tk.Button(
                table,
                text=chk,
                relief="flat",
                font=("Arial", 11),
                bg="#dba413",
                command=lambda idx=row-2: self.toggle_checkbox(idx)
            ).grid(row=row, column=0, padx=10, pady=8)

            tk.Button(
                table,
                text=course["name"],
                bg="#dba413",
                relief="flat",
                font=("Georgia", 11),
                anchor="w",
                cursor="hand2",
                command=lambda idx=row-2: self.show_course_tabs(idx)
            ).grid(row=row, column=1, sticky="ew", padx=(0, 20))

            tk.Label(
                table,
                text=course["code"],
                font=("Georgia", 11),
                bg="#dba413"
            ).grid(row=row, column=2, padx=(20, 30), sticky="e")

    def toggle_checkbox(self, index):
        self.courses[index]["checked"] = not self.courses[index]["checked"]
        self.show_course_list()

    def show_course_tabs(self, index):
        self.clear_panel()
        
        tab_bar = tk.Frame(self.main_panel, bg="#4a0709", height=45)
        tab_bar.pack(fill="x", side="top")
        tab_bar.pack_propagate(False)

        self.tab_content_view = tk.Frame(self.main_panel, bg="#6b0f0f")
        self.tab_content_view.pack(fill="both", expand=True)

        self.btn_overview_tab = tk.Button(
            tab_bar,
            text="📋 Overview",
            font=("Georgia", 11, "bold"),
            bg="#dba413",
            fg="#3d080a",
            bd=0,
            padx=25,
            relief="flat",
            cursor="hand2",
            command=lambda: self.switch_course_view("overview", index)
        )
        self.btn_overview_tab.pack(side="left", fill="y")

        self.btn_modules_tab = tk.Button(
            tab_bar,
            text="📄 Modules",
            font=("Georgia", 11, "bold"),
            bg="#6b0f0f",
            fg="white",
            bd=0,
            padx=25,
            relief="flat",
            cursor="hand2",
            command=lambda: self.switch_course_view("modules", index)
        )
        self.btn_modules_tab.pack(side="left", fill="y")
        
        self.switch_course_view("overview", index)

    def switch_course_view(self, target_tab, index):
        for widget in self.tab_content_view.winfo_children():
            widget.destroy()

        course = self.courses[index]
        course_name = course["name"]

        if target_tab == "overview":
            self.btn_overview_tab.config(bg="#dba413", fg="#3d080a")
            self.btn_modules_tab.config(bg="#6b0f0f", fg="white")

            tk.Label(
                self.tab_content_view,
                text=f"Welcome to {course_name}",
                bg="#6b0f0f",
                fg="#dba413",
                font=("Georgia", 22, "bold"),
                anchor="w"
            ).pack(anchor="w", padx=40, pady=(25, 10))

            desc_text = course.get(
                "description",
                "This course provides a comprehensive introduction to the subject.\n"
                "Attend all lectures, complete assignments on time, and review modules regularly."
            )
            tk.Label(
                self.tab_content_view,
                text=desc_text,
                bg="#6b0f0f",
                fg="white",
                font=("Georgia", 12),
                justify="left",
                anchor="w",
                wraplength=700
            ).pack(anchor="w", padx=40, pady=(0, 25))

            meta_frame = tk.Frame(self.tab_content_view, bg="#6b0f0f")
            meta_frame.pack(fill="x", padx=40, pady=5)

            meta_data = [
                ("Course Code", f": {course.get('code', 'N/A')}"),
                ("Units",       f": {course.get('units', '3')}"),
                ("Schedule",    f": {course.get('schedule', 'N/A')}"),
                ("Room",        f": {course.get('room', 'N/A')}"),
            ]

            for i, (label, val) in enumerate(meta_data):
                tk.Label(
                    meta_frame, text=label, bg="#6b0f0f", fg="white",
                    font=("Georgia", 13, "bold"), width=12, anchor="w"
                ).grid(row=i, column=0, pady=6, sticky="w")

                tk.Label(
                    meta_frame, text=val, bg="#6b0f0f", fg="white",
                    font=("Georgia", 13), anchor="w"
                ).grid(row=i, column=1, pady=6, sticky="w")

        elif target_tab == "modules":
            self.btn_overview_tab.config(bg="#6b0f0f", fg="white")
            self.btn_modules_tab.config(bg="#dba413", fg="#3d080a")

            tk.Label(
                self.tab_content_view,
                text="Course Modules",
                bg="#6b0f0f",
                fg="#dba413",
                font=("Georgia", 20, "bold")
            ).pack(anchor="w", padx=40, pady=(20, 10))

            pdf_container = tk.Frame(self.tab_content_view, bg="#6b0f0f")
            pdf_container.pack(fill="both", expand=True, padx=40, pady=(0, 10))

            scrollbar = tk.Scrollbar(pdf_container)
            scrollbar.pack(side="right", fill="y")

            pdf_canvas = tk.Canvas(pdf_container, bg="#6b0f0f", highlightthickness=0)
            pdf_canvas.pack(side="left", fill="both", expand=True)

            scrollbar.config(command=pdf_canvas.yview)
            pdf_canvas.configure(yscrollcommand=scrollbar.set)

            files_frame = tk.Frame(pdf_canvas, bg="#6b0f0f")
            pdf_window = pdf_canvas.create_window((0, 0), window=files_frame, anchor="nw")

            files_frame.bind("<Configure>", lambda e: pdf_canvas.configure(scrollregion=pdf_canvas.bbox("all")))
            pdf_canvas.bind("<Configure>", lambda e: pdf_canvas.itemconfig(pdf_window, width=e.width))

            course_materials = get_materials_by_course(course["id"])
            module_items = course_materials

            if not module_items:
                tk.Label(
                    files_frame,
                    text="No uploaded modules yet.",
                    bg="#6b0f0f",
                    fg="white",
                    font=("Georgia", 12),
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=12)

            for item in module_items:
                if isinstance(item, tuple):
                    module_path = item[4]
                    view_command = lambda p=module_path: self.open_pdf(p)
                    item = item[3]
                else:
                    view_command = lambda: None
                rowf = tk.Frame(files_frame, bg="#520a0c", bd=1, relief="solid")
                rowf.pack(fill="x", pady=4, ipady=4)

                tk.Label(
                    rowf,
                    text=f"📄  {item}",
                    bg="#520a0c",
                    fg="white",
                    font=("Georgia", 12),
                    anchor="w"
                ).pack(side="left", fill="x", expand=True, padx=15, pady=8)

                tk.Button(
                    rowf,
                    text="View",
                    bg="#dba413",
                    fg="#3d080a",
                    font=("Georgia", 10, "bold"),
                    relief="flat",
                    width=8,
                    cursor="hand2",
                    command=view_command
                ).pack(side="right", padx=15, pady=8)

        footer_layout = tk.Frame(self.tab_content_view, bg="#6b0f0f")
        footer_layout.pack(side="bottom", fill="x", pady=15, padx=40)

        tk.Button(
            footer_layout, text="← Back to Course List", bg="#dba413",
            font=("Georgia", 11, "bold"), fg="#3d080a",
            command=self.show_course_list
        ).pack(side="left")

    def show_add_course(self):
        self.clear_panel()

        tk.Label(
            self.main_panel,
            text="➕ Add Course",
            bg="#6b0f0f",
            fg="white",
            font=("Georgia", 26)
        ).pack(pady=20)
        
        tk.Frame(
            self.main_panel,
            bg="#dba413",
            height=2
        ).pack(fill="x", padx=40, pady=(0, 25))

        form = tk.Frame(self.main_panel, bg="#6b0f0f")
        form.pack(pady=20)

        tk.Label(form, text="Course Name", bg="#6b0f0f", fg="#dba413", font=("Georgia", 14)).pack()
        self.add_name = tk.Entry(form, width=50, font=("Arial", 12))
        self.add_name.pack(pady=(5, 15))

        tk.Label(form, text="Course Code", bg="#6b0f0f", fg="#dba413", font=("Georgia", 14)).pack()
        self.add_code = tk.Entry(form, width=50, font=("Arial", 12))
        self.add_code.pack(pady=(5, 15))

        tk.Button(
            self.main_panel,
            text="Add Course",
            bg="#dba413",
            fg="#3d080a",
            font=("Georgia", 12, "bold"),
            padx=10,
            command=self.add_course
        ).pack(pady=10)

    def add_course(self):
        name = self.add_name.get().strip()
        code = self.add_code.get().strip()

        if not name or not code:
            messagebox.showwarning("Missing Data", "Please complete all fields.")
            return

        try:
            db_add_course(
                name,
                code,
                "3",
                "TTH 01:00 - 02:30",
                "GLE-202",
                "This course provides a comprehensive introduction to the subject.\n"
                "Attend all lectures, complete assignments on time, and review modules regularly."
            )
        except Exception as error:
            messagebox.showerror("Unable to Add Course", str(error))
            return

        messagebox.showinfo("Success", "Course added successfully.")
        self.show_course_list()

    def get_selected_course_index(self):
        selected = [i for i, c in enumerate(self.courses) if c["checked"]]
        if len(selected) == 0:
            messagebox.showwarning("No Selection", "Please select one course to edit.")
            return None
        if len(selected) > 1:
            messagebox.showwarning("Multiple Selection", "Please select only one course to edit.")
            return None
        return selected[0]

    def show_edit_course(self):
        index = self.get_selected_course_index()
        if index is None:
            return

        course = self.courses[index]
        self.clear_panel()

        top_bar = tk.Frame(self.main_panel, bg="#6b0f0f")
        top_bar.pack(fill="x", padx=30, pady=(15, 0))

        tk.Label(
            top_bar,
            text="✏️ Edit Course",
            bg="#6b0f0f",
            fg="white",
            font=("Georgia", 26)
        ).pack(side="left")

        tk.Button(
            top_bar,
            text="Finish ✔",
            bg="#dba413",
            fg="#3d080a",
            font=("Georgia", 12, "bold"),
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=lambda: self.save_course_changes(index)
        ).pack(side="right", padx=5)

        tk.Frame(self.main_panel, bg="#dba413", height=2).pack(fill="x", padx=30, pady=(8, 12))

        fields_frame = tk.Frame(self.main_panel, bg="#6b0f0f")
        fields_frame.pack(fill="x", padx=30, pady=(0, 12))

        tk.Label(
            fields_frame, text="Course Name:", bg="#6b0f0f",
            fg="#dba413", font=("Georgia", 14)
        ).grid(row=0, column=0, sticky="e", padx=(0, 10), pady=6)

        self.edit_name = tk.Entry(fields_frame, width=40, font=("Arial", 12))
        self.edit_name.grid(row=0, column=1, sticky="w", pady=6)
        self.edit_name.insert(0, course["name"])

        tk.Label(
            fields_frame, text="Course Code:", bg="#6b0f0f",
            fg="#dba413", font=("Georgia", 14)
        ).grid(row=1, column=0, sticky="e", padx=(0, 10), pady=6)

        self.edit_code = tk.Entry(fields_frame, width=40, font=("Arial", 12))
        self.edit_code.grid(row=1, column=1, sticky="w", pady=6)
        self.edit_code.insert(0, course["code"])

        tab_bar = tk.Frame(self.main_panel, bg="#4a0709", height=42)
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)

        self.edit_tab_content = tk.Frame(self.main_panel, bg="#520a0c")
        self.edit_tab_content.pack(fill="both", expand=True)

        self.edit_btn_overview = tk.Button(
            tab_bar, text="📋 Overview",
            font=("Georgia", 11, "bold"), bg="#dba413", fg="#3d080a",
            bd=0, padx=25, relief="flat", cursor="hand2",
            command=lambda: self._edit_switch_tab("overview", index)
        )
        self.edit_btn_overview.pack(side="left", fill="y")

        self.edit_btn_modules = tk.Button(
            tab_bar, text="📄 Modules",
            font=("Georgia", 11, "bold"), bg="#6b0f0f", fg="white",
            bd=0, padx=25, relief="flat", cursor="hand2",
            command=lambda: self._edit_switch_tab("modules", index)
        )
        self.edit_btn_modules.pack(side="left", fill="y")

        self._edit_switch_tab("overview", index)

    def _edit_switch_tab(self, tab, index):
        for w in self.edit_tab_content.winfo_children():
            w.destroy()

        course = self.courses[index]

        if tab == "overview":
            self.edit_btn_overview.config(bg="#dba413", fg="#3d080a")
            self.edit_btn_modules.config(bg="#6b0f0f", fg="white")

            scroll_wrap = tk.Frame(self.edit_tab_content, bg="#520a0c")
            scroll_wrap.pack(fill="both", expand=True)

            sb = tk.Scrollbar(scroll_wrap)
            sb.pack(side="right", fill="y")

            cv = tk.Canvas(scroll_wrap, bg="#520a0c", highlightthickness=0)
            cv.pack(side="left", fill="both", expand=True)
            sb.config(command=cv.yview)
            cv.configure(yscrollcommand=sb.set)

            inner = tk.Frame(cv, bg="#520a0c")
            win = cv.create_window((0, 0), window=inner, anchor="nw")
            inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
            cv.bind("<Configure>", lambda e: cv.itemconfig(win, width=e.width))

            tk.Label(
                inner,
                text=f"Welcome to {course['name']}",
                bg="#520a0c", fg="#dba413",
                font=("Georgia", 16, "bold"), anchor="w"
            ).pack(anchor="w", padx=30, pady=(20, 6))

            tk.Label(
                inner, text="Description:",
                bg="#520a0c", fg="#dba413",
                font=("Georgia", 11, "bold"), anchor="w"
            ).pack(anchor="w", padx=30, pady=(0, 2))

            self.edit_desc = tk.Text(
                inner,
                width=70, height=3,
                font=("Georgia", 11),
                wrap="word",
                bd=0, padx=8, pady=6,
                relief="flat"
            )
            self.edit_desc.pack(anchor="w", padx=30, pady=(0, 18))
            current_desc = course.get(
                "description",
                "This course provides a comprehensive introduction to the subject.\n"
                "Attend all lectures, complete assignments on time, and review modules regularly."
            )
            self.edit_desc.insert("1.0", current_desc)

            meta_frame = tk.Frame(inner, bg="#520a0c")
            meta_frame.pack(anchor="w", padx=30, pady=(0, 10))

            meta_fields = [
                ("Units",       "units"),
                ("Schedule",    "schedule"),
                ("Room",        "room"),
            ]

            self.edit_meta_entries = {}

            for i, (label, key) in enumerate(meta_fields):
                tk.Label(
                    meta_frame, text=label,
                    bg="#520a0c", fg="white",
                    font=("Georgia", 12, "bold"), width=12, anchor="w"
                ).grid(row=i, column=0, pady=6, sticky="w")

                tk.Label(
                    meta_frame, text=":",
                    bg="#520a0c", fg="white",
                    font=("Georgia", 12)
                ).grid(row=i, column=1, pady=6, sticky="w", padx=(0, 8))

                entry = tk.Entry(
                    meta_frame,
                    font=("Georgia", 12),
                    width=28, bd=0,
                    relief="flat"
                )
                entry.grid(row=i, column=2, pady=6, sticky="w")
                entry.insert(0, course.get(key, ""))
                self.edit_meta_entries[key] = entry

            hint_bar = tk.Frame(inner, bg="#520a0c")
            hint_bar.pack(fill="x", pady=(10, 10), padx=20)
            tk.Label(
                hint_bar, text="Editing Mode - Remember to click 'Finish' to save changes",
                bg="#520a0c", fg="#dba413",
                font=("Georgia", 13, "bold")
            ).pack(side="right")

        else: 
            self.edit_btn_overview.config(bg="#6b0f0f", fg="white")
            self.edit_btn_modules.config(bg="#dba413", fg="#3d080a")

            tk.Label(
                self.edit_tab_content,
                text="Course Modules",
                bg="#520a0c", fg="#dba413",
                font=("Georgia", 16, "bold")
            ).pack(anchor="w", padx=30, pady=(16, 8))

            scroll_wrap = tk.Frame(self.edit_tab_content, bg="#520a0c")
            scroll_wrap.pack(fill="both", expand=True, padx=30, pady=(0, 10))

            sb = tk.Scrollbar(scroll_wrap)
            sb.pack(side="right", fill="y")

            cv = tk.Canvas(scroll_wrap, bg="#520a0c", highlightthickness=0)
            cv.pack(side="left", fill="both", expand=True)
            sb.config(command=cv.yview)
            cv.configure(yscrollcommand=sb.set)

            inner = tk.Frame(cv, bg="#520a0c")
            win = cv.create_window((0, 0), window=inner, anchor="nw")
            inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
            cv.bind("<Configure>", lambda e: cv.itemconfig(win, width=e.width))

            course_materials = get_materials_by_course(course["id"])
            module_items = course_materials

            if not module_items:
                tk.Label(
                    inner,
                    text="No uploaded modules yet.",
                    bg="#520a0c",
                    fg="white",
                    font=("Georgia", 12),
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=12)

            for item in module_items:
                if isinstance(item, tuple):
                    delete_command = lambda material_id=item[0], idx=index: self.delete_course_material(material_id, idx)
                    item = item[3]
                else:
                    delete_command = lambda: None
                rowf = tk.Frame(inner, bg="#3d080a", bd=1, relief="solid")
                rowf.pack(fill="x", pady=4, ipady=4)

                tk.Label(
                    rowf, text=f"📄  {item}",
                    bg="#3d080a", fg="white",
                    font=("Georgia", 12), anchor="w"
                ).pack(side="left", fill="x", expand=True, padx=15, pady=8)

                tk.Button(
                    rowf, text="Delete",
                    bg="#db1313", fg="#3d080a",
                    font=("Georgia", 10, "bold"),
                    relief="flat", width=8, cursor="hand2",
                    command=delete_command
                ).pack(side="right", padx=15, pady=8)

    def save_course_changes(self, index):
        name = self.edit_name.get().strip()
        code = self.edit_code.get().strip()

        if not name or not code:
            messagebox.showwarning("Missing Data", "Please complete all fields.")
            return

        course = self.courses[index]
        units = course.get("units", "")
        schedule = course.get("schedule", "")
        room = course.get("room", "")
        description = course.get("description", "")

        if hasattr(self, "edit_meta_entries"):
            units = self.edit_meta_entries["units"].get().strip()
            schedule = self.edit_meta_entries["schedule"].get().strip()
            room = self.edit_meta_entries["room"].get().strip()

        if hasattr(self, "edit_desc"):
            description = self.edit_desc.get("1.0", "end-1c").strip()

        try:
            db_update_course(course["id"], name, code, units, schedule, room, description)
        except Exception as error:
            messagebox.showerror("Unable to Update Course", str(error))
            return

        messagebox.showinfo("Success", "Course updated successfully.")
        self.show_course_list()

    def delete_checked_confirm(self):
        selected = self.get_selected_courses()
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one course.")
            return

        answer = messagebox.askyesno("Delete Course", "Are you sure you want to delete the selected courses?")
        if answer:
            for course in selected:
                db_delete_course(course["id"])
            messagebox.showinfo("Deleted", "Selected courses have been removed.")
            self.show_course_list()

    def show_upload_pdf(self):
        self.clear_panel()

        tk.Label(
            self.main_panel,
            text="Files Portal",
            bg="#6b0f0f",
            fg="#dba413",
            font=("Georgia", 26)
        ).pack(pady=10)

        tk.Frame(
            self.main_panel,
            bg="#dba413",
            height=2
        ).pack(fill="x", padx=40, pady=(0, 25))

        container = tk.Frame(self.main_panel, bg="#dba413", height=180)
        container.pack(fill="x", padx=40, pady=10)
        container.pack_propagate(False)

        scrollbar = tk.Scrollbar(container)
        scrollbar.pack(side="right", fill="y")

        canvas = tk.Canvas(container, bg="#dba413", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        files_frame = tk.Frame(canvas, bg="#dba413")
        win = canvas.create_window((0, 0), window=files_frame, anchor="nw")

        files_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))

        if not self.pdf_files:
            tk.Label(
                files_frame,
                text="No uploaded files yet.",
                bg="#dba413",
                fg="#3d080a",
                font=("Georgia", 11)
            ).pack(anchor="w", padx=10, pady=10)
        else:
            for pdf in self.pdf_files:
                rowf = tk.Frame(files_frame, bg="#dba413")
                rowf.pack(fill="x", padx=10, pady=3)

                tk.Button(
                    rowf,
                    text=f"📄 {pdf}",
                    relief="flat",
                    font=("Georgia", 11),
                    anchor="w",
                    bg="#dba413",
                    fg="#3d080a",
                    command=lambda p=pdf: self.open_pdf(self.pdf_paths.get(p, ""))
                ).pack(side="left", fill="x", expand=True)

                tk.Button(
                    rowf,
                    text="🗑",
                    bg="#dba413",
                    fg="red",
                    font=("Arial", 12),
                    relief="flat",
                    command=lambda p=pdf: self.delete_pdf_file(p)
                ).pack(side="right", padx=5)

        bottom_controls = tk.Frame(self.main_panel, bg="#6b0f0f")
        bottom_controls.pack(fill="x", padx=40, pady=(15, 0))

        lbl_instruct = tk.Label(bottom_controls,
            text="Instructors can manage courses details such as descriptions, and associated PDF configurations structures.",
            bg="#6b0f0f", fg="white", font=("Georgia", 10), wraplength=250, justify="left")
        lbl_instruct.pack(side="left", anchor="nw")

        center_buttons = tk.Frame(bottom_controls, bg="#6b0f0f")
        center_buttons.pack(side="left", fill="x", expand=True, padx=10)

        tk.Button(
            center_buttons,
            text="Upload PDF File",
            bg="#dba413",
            fg="#3d080a",
            font=("Georgia", 11, "bold"),
            width=18,
            command=self.upload_pdf_file
        ).pack(pady=5)

        tk.Button(
            center_buttons,
            text="Multiple Uploads →",
            bg="#dba413",
            fg="#3d080a",
            font=("Georgia", 11, "bold"),
            width=18,
            command=self.assign_selected_pdfs_to_course
        ).pack(pady=5)

        lbl_note = tk.Label(bottom_controls,
            text="NOTE** Choose target courses first before applying multiple material uploads simultaneously.",
            bg="#6b0f0f", fg="yellow", font=("Georgia", 10, "italic"), wraplength=230, justify="left")
        lbl_note.pack(side="right", anchor="ne")

    def upload_pdf_file(self):
        selected_courses = self.get_selected_courses()

        if not selected_courses:
            messagebox.showwarning(
                "No Course Selected",
                "Please select a course from the Course List first."
            )
            return

        filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filepath:
            filename = self.save_uploaded_pdf(filepath)

            selected_courses = self.get_selected_courses()
            if selected_courses:
                self.assign_pdfs_to_courses([filename], selected_courses)
                messagebox.showinfo("Upload Success", f"{filename} uploaded and assigned successfully.")
            else:
                messagebox.showinfo("Upload Success", f"{filename} uploaded successfully.")

            self.show_upload_pdf()

    def toggle_pdf_checkbox(self, filename):
        self.pdf_checked[filename] = not self.pdf_checked.get(filename, False)
        self.show_upload_pdf()

    def assign_selected_pdfs_to_course(self):
        selected_courses = self.get_selected_courses()

        if not selected_courses:
            messagebox.showwarning(
                "No Course Selected",
                "Please select a course from the Course List first."
            )
            return

        filepaths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if not filepaths:
            return

        selected_courses = self.get_selected_courses()
        uploaded_pdfs = [self.save_uploaded_pdf(filepath) for filepath in filepaths]

        if not selected_courses:
            messagebox.showinfo("Upload Success", "PDF files uploaded successfully.")
            self.show_upload_pdf()
            return

        assigned_count = self.assign_pdfs_to_courses(uploaded_pdfs, selected_courses)

        if assigned_count:
            messagebox.showinfo("Success", "PDF files uploaded and assigned to the selected course/s.")
        else:
            messagebox.showinfo("Already Assigned", "The uploaded PDF files are already assigned to the selected course/s.")

        self.show_upload_pdf()

    def delete_pdf_file(self, filename):
        for material in get_materials():
            if material[3] == filename:
                db_delete_material(material[0])

        filepath = self.pdf_paths.get(filename)

        if filepath and os.path.exists(filepath):
            os.remove(filepath)

        if filename in self.pdf_files:
            self.pdf_files.remove(filename)
        self.pdf_checked.pop(filename, None)
        self.pdf_paths.pop(filename, None)
        self.show_upload_pdf()

    def delete_course_material(self, material_id, course_index):
        answer = messagebox.askyesno("Delete Material", "Are you sure you want to delete this material?")
        if answer:
            db_delete_material(material_id)
            self._edit_switch_tab("modules", course_index)

    def logout(self):
        answer = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if answer:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FacultyDashboard(root)
    root.mainloop()