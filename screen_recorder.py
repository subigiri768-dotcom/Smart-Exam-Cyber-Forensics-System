import cv2
import numpy as np
import pyautogui
import threading
import time
import os
from datetime import datetime
import config


class ScreenRecorder:

    def __init__(self):

        self.recording = False
        self.thread = None
        self.output_file = None
        self.video_writer = None

        os.makedirs(
            config.PATHS["recordings_dir"],
            exist_ok=True
        )

    def start(self):

        if self.recording:
            return

        self.recording = True

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.output_file = os.path.join(
            config.PATHS["recordings_dir"],
            f"screen_recording_{timestamp}.avi"
        )

        self.thread = threading.Thread(
            target=self.record_screen,
            daemon=True
        )

        self.thread.start()

        print("[INFO] Screen recording started.")

    def stop(self):

        self.recording = False

        if self.thread is not None:
            self.thread.join()

        print("[INFO] Screen recording stopped.")
        print(f"[INFO] Recording saved at: {self.output_file}")

        return self.output_file

    def record_screen(self):

        try:

            screen_size = pyautogui.size()

            width = screen_size.width // 2 * 2
            height = screen_size.height // 2 * 2

            fourcc = cv2.VideoWriter_fourcc(*"XVID")

            self.video_writer = cv2.VideoWriter(
                self.output_file,
                fourcc,
                10.0,
                (width, height)
            )

            if not self.video_writer.isOpened():
                print("[ERROR] Unable to create video file.")
                return

            while self.recording:

                screenshot = pyautogui.screenshot()

                frame = np.array(screenshot)

                frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_RGB2BGR
                )

                if frame.shape[1] != width or frame.shape[0] != height:
                    frame = cv2.resize(
                        frame,
                        (width, height)
                    )

                # Date & Time
                cv2.putText(
                    frame,
                    datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

                # REC Indicator
                cv2.circle(
                    frame,
                    (width - 40, 30),
                    8,
                    (0, 0, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    "REC",
                    (width - 85, 38),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

                self.video_writer.write(frame)

                time.sleep(0.1)

            self.video_writer.release()

            print(f"[INFO] Recording successfully saved: {self.output_file}")

        except Exception as e:

            print(f"[SCREEN RECORDER ERROR] {e}")

            if self.video_writer:
                self.video_writer.release()