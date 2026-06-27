
import os
import datetime

import config

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle
)


class ReportGenerator:

    def __init__(self):

        self.report_folder = config.PATHS["reports_dir"]

        os.makedirs(self.report_folder, exist_ok=True)

    # -----------------------------------------------------

    def generate(
        self,
        student_name,
        student_id,
        exam_name,
        violations,
        screenshots,
        recording_path,
        risk_score
    ):

        filename = os.path.join(

            self.report_folder,

            f"Audit_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        )

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        title_style = styles["Title"]
        title_style.alignment = TA_CENTER

        story = []

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        story.append(

            Paragraph(

                config.REPORT["title"],

                title_style

            )

        )

        story.append(

            Paragraph(

                config.REPORT["subtitle"],

                styles["Heading2"]

            )

        )

        story.append(Spacer(1, 20))

        # -------------------------------------------------
        # Student Information
        # -------------------------------------------------

        story.append(

            Paragraph(

                "<b>Candidate Information</b>",

                styles["Heading2"]

            )

        )

        story.append(
            Paragraph(f"Student Name : {student_name}", styles["Normal"])
        )

        story.append(
            Paragraph(f"Student ID : {student_id}", styles["Normal"])
        )

        story.append(
            Paragraph(f"Exam : {exam_name}", styles["Normal"])
        )

        story.append(
            Paragraph(
                f"Generated : {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 20))

        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        story.append(

            Paragraph(

                "<b>Exam Summary</b>",

                styles["Heading2"]

            )

        )

        story.append(

            Paragraph(

                f"Total Violations : {len(violations)}",

                styles["Normal"]

            )

        )

        story.append(

            Paragraph(

                f"Total Risk Score : {risk_score}",

                styles["Normal"]

            )

        )

        if risk_score < config.RISK_LEVEL["MEDIUM"]:

            verdict = "LOW RISK"
            colour = "green"

        elif risk_score < config.RISK_LEVEL["HIGH"]:

            verdict = "MEDIUM RISK"
            colour = "orange"

        else:

            verdict = "HIGH RISK"
            colour = "red"

        story.append(

            Paragraph(

                f"Final Verdict : <font color='{colour}'><b>{verdict}</b></font>",

                styles["Normal"]

            )

        )

        story.append(Spacer(1, 20))

        # -------------------------------------------------
        # Violation Table
        # -------------------------------------------------

        story.append(

            Paragraph(

                "<b>Violation Log</b>",

                styles["Heading2"]

            )

        )

        table_data = [

            [

                "Time",

                "Violation",

                "Severity"

            ]

        ]

        if len(violations) == 0:

            table_data.append(

                [

                    "-",

                    "No Violations Detected",

                    "-"

                ]

            )

        else:

            for violation in violations:

                table_data.append(

                    [

                        violation["time"],

                        violation["type"],

                        violation["severity"]

                    ]

                )

        table = Table(table_data)

        table.setStyle(

            TableStyle([

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("ALIGN",(0,0),(-1,-1),"CENTER"),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                ("BOTTOMPADDING",(0,0),(-1,0),10)

            ])

        )

        story.append(table)

        story.append(Spacer(1, 20))

        # -------------------------------------------------
        # Recording
        # -------------------------------------------------

        story.append(

            Paragraph(

                "<b>Screen Recording</b>",

                styles["Heading2"]

            )

        )

        if recording_path:

            story.append(

                Paragraph(

                    recording_path,

                    styles["Normal"]

                )

            )

        else:

            story.append(

                Paragraph(

                    "No recording available.",

                    styles["Normal"]

                )

            )

        story.append(Spacer(1, 20))

        # -------------------------------------------------
        # Evidence
        # -------------------------------------------------

        story.append(

            Paragraph(

                "<b>Evidence Screenshots</b>",

                styles["Heading2"]

            )

        )

        if screenshots:

            for image in screenshots:

                if os.path.exists(image):

                    try:

                        story.append(

                            Image(

                                image,

                                width=5*inch,

                                height=3*inch

                            )

                        )

                        story.append(Spacer(1, 10))

                    except:

                        pass

        else:

            story.append(

                Paragraph(

                    "No screenshots captured.",

                    styles["Normal"]

                )

            )

        story.append(Spacer(1, 20))

        # -------------------------------------------------
        # Footer
        # -------------------------------------------------

        story.append(

            Paragraph(

                "<b>Digital Integrity</b>",

                styles["Heading2"]

            )

        )

        story.append(

            Paragraph(

                "This report was automatically generated by the Smart Exam Cyber Forensics System.",

                styles["Italic"]

            )

        )

        doc.build(story)

        return filename
