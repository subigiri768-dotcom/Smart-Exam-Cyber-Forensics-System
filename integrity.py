import hashlib
import os
from datetime import datetime


class IntegrityManager:

    def __init__(self):
        self.hash_records = {}

    def generate_hash(self, filepath):

        sha256 = hashlib.sha256()

        try:
            with open(filepath, "rb") as file:

                while True:

                    chunk = file.read(4096)

                    if not chunk:
                        break

                    sha256.update(chunk)

            return sha256.hexdigest()

        except Exception as e:

            print(f"[ERROR] Hash Generation Failed: {e}")
            return None

    def save_hash(self, filepath):

        file_hash = self.generate_hash(filepath)

        if file_hash:
            self.hash_records[filepath] = file_hash

        return file_hash

    def verify_file(self, filepath):

        if filepath not in self.hash_records:

            print(
                f"[WARNING] No stored hash found for {filepath}"
            )
            return False

        current_hash = self.generate_hash(filepath)

        if current_hash == self.hash_records[filepath]:

            print(
                f"[OK] Integrity Verified: {filepath}"
            )

            return True

        else:

            print(
                f"[ALERT] File Tampering Detected: {filepath}"
            )

            return False

    def verify_folder(self, folder_path):

        results = {}

        if not os.path.exists(folder_path):

            print(
                f"[ERROR] Folder Not Found: {folder_path}"
            )

            return results

        for root, dirs, files in os.walk(folder_path):

            for file in files:

                full_path = os.path.join(
                    root,
                    file
                )

                if full_path in self.hash_records:

                    results[full_path] = self.verify_file(
                        full_path
                    )

        return results

    def create_audit_log(
        self,
        username,
        report_file
    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        report_hash = self.generate_hash(
            report_file
        )

        log_file = f"audit_log_{username}.txt"

        with open(
            log_file,
            "a",
            encoding="utf-8"
        ) as log:

            log.write(
                f"\n[{timestamp}] "
                f"Report: {report_file} | "
                f"SHA256: {report_hash}\n"
            )

        print(
            f"[INFO] Audit Log Updated: {log_file}"
        )