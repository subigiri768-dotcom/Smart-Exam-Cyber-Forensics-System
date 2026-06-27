import os
from database import get_user_violations

def generate_report(username, risk_score):
    # 'reports' फोल्डर छ कि छैन चेक गर्ने, छैन भने बनाउने
    if not os.path.exists("reports"):
        os.makedirs("reports")

    violations = get_user_violations(username)
    # फाइल पाथ: reports/Report_username.txt
    filename = f"reports/Report_{username}.txt"

    with open(filename, "w", encoding="utf-8") as report:
        report.write("SMART EXAM AUDIT REPORT\n")
        report.write("=" * 40 + "\n")
        report.write(f"Student : {username}\n")
        report.write(f"Risk Score : {risk_score}\n\n")
        report.write("Detected Violations:\n\n")

        for violation in violations:
            # violation = type, violation = points
            report.write(f"Violation: {violation} | Risk Points: {violation}\n")

    print(f"Report Generated : {filename}")