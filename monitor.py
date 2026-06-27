import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time

from evidence import EvidenceCollector
from database import get_total_risk


class ExamMonitor:

    def __init__(self, username):

        self.username = username
        self.running = True

        self.evidence = EvidenceCollector()

        self.risk_score = 0

        cascade = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

        self.face_detector = cv2.CascadeClassifier(cascade)

        self.last_no_face_time = 0
        self.last_multiple_face_time = 0

        # ----------------------------
        # Monitor Window
        # ----------------------------

        self.root = tk.Toplevel()

        self.root.title("Smart Exam Monitor")

        self.root.attributes("-topmost", True)

        self.root.resizable(False, False)

        screen_width = self.root.winfo_screenwidth()

        self.root.geometry(f"330x300+{screen_width-350}+20")

        self.video_label = tk.Label(self.root)

        self.video_label.pack()

        self.status = tk.Label(
            self.root,
            text="Monitoring...",
            fg="green",
            font=("Arial",11,"bold")
        )

        self.status.pack(pady=5)

        self.risk_label = tk.Label(
            self.root,
            text="Risk Score : 0",
            fg="red",
            font=("Arial",11,"bold")
        )

        self.risk_label.pack()

    # ------------------------------------

    def add_violation(self, points, reason):

        self.risk_score += points

        self.risk_label.config(
            text=f"Risk Score : {self.risk_score}"
        )

        try:

            # EvidenceCollector already saves the screenshot
            # and writes the violation to the database.

            self.evidence.capture(

                self.username,

                reason

            )

        except Exception as e:

            print(f"[MONITOR ERROR] {e}")

    # ------------------------------------

    def start(self):

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():

            print("[ERROR] Camera not found.")

            return

        self.update_feed()

    # ------------------------------------

    def stop(self):

        self.running = False

        if hasattr(self, "cap"):

            self.cap.release()

        try:

            self.root.destroy()

        except:

            pass

    # ------------------------------------

    def update_feed(self):

        if not self.running:
            return

        success, frame = self.cap.read()

        if success:

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = self.face_detector.detectMultiScale(
                gray,
                1.1,
                6,
                minSize=(80,80)
            )

            now = time.time()

            # ----------------------------
            # No Face
            # ----------------------------

            if len(faces) == 0:

                if now-self.last_no_face_time > 15:

                    self.add_violation(

                        10,

                        "No Face Detected"

                    )

                    self.last_no_face_time = now

            # ----------------------------
            # Multiple Faces
            # ----------------------------

            elif len(faces) > 1:

                if now-self.last_multiple_face_time > 10:

                    self.add_violation(

                        20,

                        "Multiple Faces Detected"

                    )

                    self.last_multiple_face_time = now

            # ----------------------------
            # Draw Rectangle
            # ----------------------------

            for (x,y,w,h) in faces:

                cv2.rectangle(

                    frame,

                    (x,y),

                    (x+w,y+h),

                    (0,255,0),

                    2

                )

            cv2.putText(

                frame,

                f"Risk : {self.risk_score}",

                (10,30),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                (0,0,255),

                2

            )

            rgb = cv2.cvtColor(

                frame,

                cv2.COLOR_BGR2RGB

            )

            img = Image.fromarray(rgb)

            img = img.resize((320,240))

            imgtk = ImageTk.PhotoImage(img)

            self.video_label.configure(image=imgtk)

            self.video_label.image = imgtk

        self.root.after(40,self.update_feed)

    # ------------------------------------

    def get_risk_score(self):

        return get_total_risk(self.username)