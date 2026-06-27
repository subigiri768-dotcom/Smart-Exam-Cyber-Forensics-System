import psutil
import threading
import time
import pygetwindow as gw

from evidence import EvidenceCollector


class ProcessWatcher:

    def __init__(self, username):

        self.username = username
        self.running = False

        self.evidence = EvidenceCollector()

        # Process Name : Friendly Name
        self.forbidden_apps = {

            "chrome.exe": "Google Chrome",
            "msedge.exe": "Microsoft Edge",
            "firefox.exe": "Mozilla Firefox",
            "brave.exe": "Brave Browser",
            "opera.exe": "Opera Browser",

            "discord.exe": "Discord",
            "telegram.exe": "Telegram",
            "whatsapp.exe": "WhatsApp",

            "teamviewer.exe": "TeamViewer",
            "anydesk.exe": "AnyDesk",

            "taskmgr.exe": "Task Manager"

        }

        # Prevent repeated logging
        self.last_detection = {}

        # Seconds before the same application can be logged again
        self.cooldown = 30

    # ---------------------------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        threading.Thread(
            target=self.monitor,
            daemon=True
        ).start()

        print("[INFO] Process Watcher Started")

    # ---------------------------------------------------

    def stop(self):

        self.running = False

        print("[INFO] Process Watcher Stopped")

    # ---------------------------------------------------

    def wait_for_window(self, process_name):

        keywords = {

            "chrome.exe": "Chrome",
            "msedge.exe": "Edge",
            "firefox.exe": "Firefox",
            "brave.exe": "Brave",
            "opera.exe": "Opera",

            "discord.exe": "Discord",
            "telegram.exe": "Telegram",
            "whatsapp.exe": "WhatsApp",

            "teamviewer.exe": "TeamViewer",
            "anydesk.exe": "AnyDesk",

            "taskmgr.exe": "Task Manager"

        }

        keyword = keywords.get(process_name)

        if keyword is None:
            return

        # Wait up to 3 seconds for the window
        for _ in range(30):

            try:

                windows = gw.getWindowsWithTitle(keyword)

                if windows:

                    window = windows[0]

                    try:

                        if window.isMinimized:
                            window.restore()

                        window.activate()

                    except Exception:
                        pass

                    time.sleep(1)

                    return

            except Exception:
                pass

            time.sleep(0.1)

    # ---------------------------------------------------

    def monitor(self):

        while self.running:

            now = time.time()

            try:

                for proc in psutil.process_iter(["name"]):

                    try:

                        name = proc.info["name"]

                        if not name:
                            continue

                        name = name.lower()

                        if name in self.forbidden_apps:

                            # Cooldown check
                            if name in self.last_detection:

                                if now - self.last_detection[name] < self.cooldown:
                                    continue

                            self.last_detection[name] = now

                            app_name = self.forbidden_apps[name]

                            if "Browser" in app_name or \
                               "Chrome" in app_name or \
                               "Edge" in app_name or \
                               "Firefox" in app_name or \
                               "Brave" in app_name or \
                               "Opera" in app_name:

                                violation = f"Browser Opened ({app_name})"

                            else:

                                violation = f"{app_name} Opened"

                            print(f"[WARNING] {violation}")

                            # Wait until window is visible
                            self.wait_for_window(name)

                            # Small delay so the window is fully drawn
                            time.sleep(1)

                            # Capture evidence
                            self.evidence.capture(

                                self.username,

                                violation

                            )

                    except (
                        psutil.NoSuchProcess,
                        psutil.AccessDenied,
                        psutil.ZombieProcess
                    ):
                        continue

                time.sleep(2)

            except Exception as e:

                print(f"[PROCESS WATCHER ERROR] {e}")

                time.sleep(2)