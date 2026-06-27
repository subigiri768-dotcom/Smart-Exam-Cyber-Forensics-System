import os
from datetime import datetime


class ChainOfCustody:

    def __init__(self):

        self.log_file = "custody_log.txt"

        if not os.path.exists(self.log_file):

            with open(
                self.log_file,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "=" * 70 + "\n"
                )

                file.write(
                    "SMART EXAM SYSTEM - CHAIN OF CUSTODY LOG\n"
                )

                file.write(
                    "=" * 70 + "\n\n"
                )

    def record(
        self,
        username,
        evidence_file,
        file_hash,
        action="Evidence Captured"
    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                f"\nTimestamp : {timestamp}\n"
            )

            file.write(
                f"User      : {username}\n"
            )

            file.write(
                f"Action    : {action}\n"
            )

            file.write(
                f"Evidence  : {evidence_file}\n"
            )

            file.write(
                f"SHA256    : {file_hash}\n"
            )

            file.write(
                "-" * 70 + "\n"
            )

        print(
            f"[CHAIN OF CUSTODY] Logged: {evidence_file}"
        )

    def verify_hash(
        self,
        original_hash,
        current_hash
    ):

        return original_hash == current_hash