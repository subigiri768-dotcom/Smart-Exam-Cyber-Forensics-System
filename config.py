"""
=========================================================
 Smart Exam Cyber Forensics System
 Configuration File
=========================================================
"""

import os

# =========================================================
# Application
# =========================================================

APP_NAME = "Smart Exam Cyber Forensics System"
APP_VERSION = "1.0.0"
DEVELOPER = "Subi Giri"

# =========================================================
# Folder Paths
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATHS = {

    "database": os.path.join(BASE_DIR, "exam_system.db"),

    "evidence_dir": os.path.join(BASE_DIR, "evidence"),

    "recordings_dir": os.path.join(BASE_DIR, "recordings"),

    "reports_dir": os.path.join(BASE_DIR, "reports"),

    "logs_dir": os.path.join(BASE_DIR, "logs"),

    "images_dir": os.path.join(BASE_DIR, "images")

}

# Automatically create folders

for folder in [

    PATHS["evidence_dir"],

    PATHS["recordings_dir"],

    PATHS["reports_dir"],

    PATHS["logs_dir"],

    PATHS["images_dir"]

]:

    os.makedirs(folder, exist_ok=True)

# =========================================================
# Risk Points
# =========================================================

RISK_POINTS = {

    "Tab Switch": 10,

    "No Face Detected": 10,

    "Multiple Faces Detected": 20,

    "Browser Opened": 20,

    "WhatsApp Opened": 25,

    "Discord Opened": 25,

    "Telegram Opened": 25,

    "USB Device Detected": 25,

    "Phone Detected": 30,

    "Screen Minimized": 15,

    "Virtual Machine Detected": 30

}

# =========================================================
# Risk Levels
# =========================================================

RISK_LEVEL = {

    "LOW": 0,

    "MEDIUM": 30,

    "HIGH": 60

}

# =========================================================
# Camera Settings
# =========================================================

CAMERA = {

    "index": 0,

    "width": 640,

    "height": 480,

    "fps": 30

}

# =========================================================
# Face Detection
# =========================================================

FACE_DETECTION = {

    "cascade": "haarcascade_frontalface_default.xml",

    "scaleFactor": 1.1,

    "minNeighbors": 6,

    "minSize": (80, 80),

    "no_face_delay": 15,

    "multiple_face_delay": 10

}

# =========================================================
# Screen Recorder
# =========================================================

SCREEN_RECORDER = {

    "fps": 10,

    "codec": "XVID",

    "extension": ".avi"

}

# =========================================================
# PDF Report
# =========================================================

REPORT = {

    "title": "SMART EXAM CYBER FORENSICS SYSTEM",

    "subtitle": "Digital Examination Audit Report",

    "author": "Smart Exam Cyber Forensics System",

    "subject": "Cyber Forensics Audit Report"

}

# =========================================================
# Evidence
# =========================================================

EVIDENCE = {

    "image_extension": ".png",

    "hash_algorithm": "SHA256"

}

# =========================================================
# Monitor
# =========================================================

MONITOR = {

    "refresh_rate": 40,

    "window_width": 330,

    "window_height": 300

}

# =========================================================
# Colors
# =========================================================

COLORS = {

    "success": "#28A745",

    "warning": "#FFC107",

    "danger": "#DC3545",

    "primary": "#007BFF",

    "background": "#FFFFFF"

}

# =========================================================
# Login
# =========================================================

LOGIN = {

    "window_width": 500,

    "window_height": 350

}

# =========================================================
# Welcome Screen
# =========================================================

WELCOME = {

    "window_width": 900,

    "window_height": 600

}

# =========================================================
# Print Configuration
# =========================================================

print(f"[CONFIG] {APP_NAME} v{APP_VERSION} Loaded Successfully")