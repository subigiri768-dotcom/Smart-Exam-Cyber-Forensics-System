
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import os
import glob

import config
import database

from login import LoginWindow
from monitor import ExamMonitor
from process_watcher import ProcessWatcher
from screen_recorder import ScreenRecorder
from report_generator import ReportGenerator
from integrity import IntegrityManager


class SmartExamSystem:

    def __init__(self):

        database.init_db()

        self.root = tk.Tk()
        self.root.title(config.APP_NAME)
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.monitor = None
        self.recorder = None
        self.process_watcher = None

        self.current_user = None
        self.latest_report = None

        self.report_generator = ReportGenerator()
        self.integrity = IntegrityManager()

        self.show_welcome_page()

    # --------------------------------------------------

    def show_welcome_page(self):

        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.pack(fill="both", expand=True)

        if os.path.exists("welcome.png"):

            image = Image.open("welcome.png")
            image = image.resize((900, 600))

            self.bg_image = ImageTk.PhotoImage(image)

            tk.Label(
                self.welcome_frame,
                image=self.bg_image
            ).place(relwidth=1, relheight=1)

        tk.Label(

            self.welcome_frame,

            text=config.APP_NAME,

            font=("Arial",22,"bold"),

            bg="black",

            fg="white"

        ).place(relx=0.5,rely=0.2,anchor="center")

        tk.Label(

            self.welcome_frame,

            text="AI Powered Exam Monitoring & Cyber Forensics",

            font=("Arial",14),

            bg="black",

            fg="white"

        ).place(relx=0.5,rely=0.3,anchor="center")

        tk.Button(

            self.welcome_frame,

            text="START",

            font=("Arial",14,"bold"),

            bg="#1e90ff",

            fg="white",

            width=15,

            command=self.open_login

        ).place(relx=0.5,rely=0.75,anchor="center")

    # --------------------------------------------------

    def open_login(self):

        self.welcome_frame.destroy()

        self.root.geometry("500x350")

        LoginWindow(

            self.root,

            self.start_exam

        )

    # --------------------------------------------------

    def start_exam(self, username):

        self.current_user = username

        for widget in self.root.winfo_children():

            widget.destroy()

        tk.Label(

            self.root,

            text="Monitoring Active",

            fg="green",

            font=("Arial",18,"bold")

        ).pack(pady=20)

        tk.Label(

            self.root,

            text=f"Student : {username}",

            font=("Arial",12)

        ).pack()

        self.recorder = ScreenRecorder()
        self.recorder.start()

        self.monitor = ExamMonitor(username)

        threading.Thread(

            target=self.monitor.start,

            daemon=True

        ).start()

        self.process_watcher = ProcessWatcher(username)
        self.process_watcher.start()

        tk.Button(

            self.root,

            text="End Exam",

            bg="red",

            fg="white",

            width=20,

            font=("Arial",12,"bold"),

            command=self.end_exam

        ).pack(pady=30)

    # --------------------------------------------------

    def end_exam(self):

        if not messagebox.askyesno(

            "Confirm",

            "End the examination?"

        ):

            return

        try:

            if self.monitor:

                self.monitor.stop()

            recording_path = ""

            if self.recorder:

                recording_path = self.recorder.stop()

            if self.process_watcher:

                self.process_watcher.stop()

            violations = database.get_user_violations(

                self.current_user

            )

            screenshots = glob.glob(

                os.path.join(

                    config.PATHS["evidence_dir"],

                    "*.png"

                )

            )

            risk_score = database.get_total_risk(

                self.current_user

            )

            self.latest_report = self.report_generator.generate(

                student_name=self.current_user,

                student_id="N/A",

                exam_name="Smart Examination",

                violations=violations,

                screenshots=screenshots,

                recording_path=recording_path,

                risk_score=min(risk_score,100)

            )

            if self.latest_report:

                self.integrity.save_hash(

                    self.latest_report

                )

                self.integrity.create_audit_log(

                    self.current_user,

                    self.latest_report

                )

            if recording_path:

                self.integrity.save_hash(

                    recording_path

                )

            messagebox.showinfo(

                "Success",

                "Audit Report Generated Successfully."

            )

            self.show_report_option()

        except Exception as e:

            messagebox.showerror(

                "Error",

                str(e)

            )

    # --------------------------------------------------

    def show_report_option(self):

        for widget in self.root.winfo_children():

            widget.destroy()

        tk.Label(

            self.root,

            text="Exam Finished",

            font=("Arial",18,"bold")

        ).pack(pady=50)

        tk.Button(

            self.root,

            text="View Audit Report",

            bg="green",

            fg="white",

            width=20,

            height=2,

            font=("Arial",12,"bold"),

            command=self.open_report

        ).pack()

    # --------------------------------------------------

    def open_report(self):

        if self.latest_report and os.path.exists(self.latest_report):

            os.startfile(self.latest_report)

        else:

            messagebox.showwarning(

                "No Report",

                "No audit report found."

            )

    # --------------------------------------------------

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    SmartExamSystem().run()

