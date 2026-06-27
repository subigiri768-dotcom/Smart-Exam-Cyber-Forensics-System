import threading
import time
import win32gui

from database import add_violation


class WindowMonitor:

    def __init__(self, username):

        self.username = username
        self.running = False

        # Titles allowed during exam
        self.allowed = [
            "Smart Exam",
            "Smart Exam Cyber Forensics System",
            "Monitor"
        ]

        self.last_title = ""

    def start(self):

        self.running = True

        threading.Thread(
            target=self.monitor,
            daemon=True
        ).start()

    def stop(self):

        self.running = False

    def monitor(self):

        while self.running:

            hwnd = win32gui.GetForegroundWindow()

            title = win32gui.GetWindowText(hwnd)

            if title != self.last_title:

                self.last_title = title

                if title != "":

                    allowed = False

                    for app in self.allowed:

                        if app.lower() in title.lower():

                            allowed = True
                            break

                    if not allowed:

                        print("[TAB SWITCH]", title)

                        add_violation(
                            self.username,
                            f"Opened Application : {title}",
                            5,
                            ""
                        )

            time.sleep(1)