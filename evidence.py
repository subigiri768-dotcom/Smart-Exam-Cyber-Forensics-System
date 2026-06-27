import os
from datetime import datetime

import pyautogui
import pygetwindow as gw

import database
import config
from integrity import IntegrityManager


class EvidenceCollector:

    def __init__(self):

        self.evidence_dir = config.PATHS["evidence_dir"]

        os.makedirs(self.evidence_dir, exist_ok=True)

        self.integrity = IntegrityManager()

    # -----------------------------------------------------

    def get_risk_points(self, violation):

        if "Browser Opened" in violation:
            return 20

        elif "No Face" in violation:
            return 10

        elif "Multiple Faces" in violation:
            return 20

        elif "Discord" in violation:
            return 25

        elif "WhatsApp" in violation:
            return 25

        elif "Telegram" in violation:
            return 25

        elif "Task Manager" in violation:
            return 30

        return 10

    # -----------------------------------------------------

    def capture_window(self, keyword):

        windows = gw.getWindowsWithTitle(keyword)

        if len(windows) == 0:
            return None

        window = windows[0]

        try:

            if window.isMinimized:
                window.restore()

            window.activate()

        except:
            pass

        x = window.left
        y = window.top
        w = window.width
        h = window.height

        if w <= 0 or h <= 0:
            return None

        return pyautogui.screenshot(

            region=(x, y, w, h)

        )

    # -----------------------------------------------------

    def capture(self, username, violation):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        safe = violation.replace(" ", "_").replace("(", "").replace(")", "")

        filename = os.path.join(

            self.evidence_dir,

            f"{username}_{safe}_{timestamp}.png"

        )

        screenshot = None

        if "Chrome" in violation:

            screenshot = self.capture_window("Chrome")

        elif "Edge" in violation:

            screenshot = self.capture_window("Edge")

        elif "Firefox" in violation:

            screenshot = self.capture_window("Firefox")

        elif "Brave" in violation:

            screenshot = self.capture_window("Brave")

        elif "Opera" in violation:

            screenshot = self.capture_window("Opera")

        elif "Discord" in violation:

            screenshot = self.capture_window("Discord")

        elif "Telegram" in violation:

            screenshot = self.capture_window("Telegram")

        elif "WhatsApp" in violation:

            screenshot = self.capture_window("WhatsApp")

        if screenshot is None:

            screenshot = pyautogui.screenshot()

        screenshot.save(filename)

        risk = self.get_risk_points(violation)

        database.add_violation(

            username,

            violation,

            risk,

            filename

        )

        self.integrity.save_hash(filename)

        print("[INFO] Evidence Saved:", filename)

        return filename