import os
import json
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

# -------------------------
# Load Config
# -------------------------

with open("config.json", "r") as file:
    config = json.load(file)

PARENT_FOLDER = config["default_folder"]
ERROR_THRESHOLD = config["error_threshold"]
CHECK_INTERVAL = config["check_interval_minutes"]

EMAIL_ALERT_ENABLED = config["email_alert_enabled"]

SMTP_SERVER = config["smtp_server"]
SMTP_PORT = config["smtp_port"]

SENDER_EMAIL = config["sender_email"]
SENDER_PASSWORD = config["sender_password"]

RECEIVER_EMAIL = config["receiver_email"]

STATE_FILE = "alert_state.json"

# -------------------------
# Alert State
# -------------------------

def load_state():

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)

    return {}

def save_state(state):

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# -------------------------
# Count Errors
# -------------------------

def count_errors(folder_path):

    error_count = 0

    for root, dirs, files in os.walk(folder_path):
        

        for file_name in files:

            if file_name.lower().endswith(".log"):

                file_path = os.path.join(root, file_name)

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as file:

                        for line in file:

                            if "ERROR" in line.upper():
                                print(f"Found ERROR in: {file_path}")
                                error_count += 1

                except Exception as e:

                    print(
                        f"Could not read {file_path}: {e}"
                    )

    return error_count

# -------------------------
# Email Alert
# -------------------------

def send_email_alert(folder_name, error_count):

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    body = f"""
ERROR THRESHOLD EXCEEDED

Folder Name:
{folder_name}

Error Count:
{error_count}

Threshold:
{ERROR_THRESHOLD}

Detection Time:
{current_time}

Status:
Folder exceeded configured error threshold.
"""

    msg = MIMEText(body)

    msg["Subject"] = (
        f"🚨 Naviga Alert - {folder_name}"
    )

    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        ) as server:

            server.starttls()

            server.login(
                SENDER_EMAIL,
                SENDER_PASSWORD
            )

            server.send_message(msg)

        print(
            f"Email sent for {folder_name}"
        )

    except Exception as e:

        print(f"Email Error: {e}")

# -------------------------
# Check Folders
# -------------------------

def check_folders():

    state = load_state()

    for folder_name in os.listdir(PARENT_FOLDER):

        folder_path = os.path.join(
            PARENT_FOLDER,
            folder_name
        )

        if not os.path.isdir(folder_path):
            continue

        errors = count_errors(folder_path)

        print(
            f"{folder_name} -> {errors} errors"
        )

        if errors > ERROR_THRESHOLD:

            if not state.get(folder_name, False):

                if EMAIL_ALERT_ENABLED:

                    send_email_alert(
                        folder_name,
                        errors
                    )

                state[folder_name] = True

        else:

            state[folder_name] = False

    save_state(state)

# -------------------------
# Main Loop
# -------------------------

print("Monitoring Started...")

while True:

    check_folders()

    print(
        f"Waiting {CHECK_INTERVAL} minute(s)..."
    )

    time.sleep(
        CHECK_INTERVAL * 60
    )


    #hii