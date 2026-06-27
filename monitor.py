import time
import json

from monitor_state import check_all_logs
from email_alert import send_email

# Load config
with open("config.json", "r") as file:
    config = json.load(file)

CHECK_INTERVAL = config["check_interval_minutes"] * 60
THRESHOLD = config["error_threshold"]

print("Log Monitor Started...")

while True:

    folder_errors = check_all_logs()

    for folder, errors in folder_errors.items():

        if errors > THRESHOLD:

            subject = f"⚠️ Error Alert - {folder}"

            body = f"""
Error limit exceeded!

Folder Name : {folder}

Total Errors : {errors}

Threshold : {THRESHOLD}

Please check the log files.
"""

            send_email(subject, body)

            print(f"Email sent for {folder}")

    print(f"Waiting {config['check_interval_minutes']} minutes...")

    time.sleep(CHECK_INTERVAL)