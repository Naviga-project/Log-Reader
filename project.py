
# # from concurrent.futures import wait
# import traceback
# import yagmail
# from datetime import datetime, time

# def send_error_email(error):

#     yag = yagmail.SMTP(
#         user="shivangisrivastava137@gmail.com",
#         password="fnicyjqsqmenlhri"
#     )

#     subject = "🚨 Website Error Alert"

#     body = f"""
#     Error Detected

#     Time: {datetime.now()}

#     Error:
#     {error}
#     """

#     yag.send(
#         to="tishyasinghal04@gmail.com",
#         subject=subject,
#         contents=body
#     )


# try:
#     x = 10 / 0

# except Exception as e:

#     error_details = traceback.format_exc()

#     send_error_email(error_details)


# import time
# import traceback

# while True:
#     try:
#         x = 10 / 0

#     except Exception:
#         error_details = traceback.format_exc()
#         send_error_email(error_details)

#     time.sleep(10)



# import traceback
# import yagmail
# from datetime import datetime
# import time

# def send_error_email(error):

#     yag = yagmail.SMTP(
#         user="shivangisrivastava137@gmail.com",
#         password="fnicyjqsqmenlhri"
#     )

#     subject = "🚨 Website Error Alert"

#     body = f"""
# Error Detected

# Time: {datetime.now()}

# Error:
# {error}
# """

#     yag.send(
#         to="tishyasinghal04@gmail.com",
#         subject=subject,
#         contents=body
#     )

# while True:
#     try:
#         x = 10 / 0

#     except Exception:
#         error_details = traceback.format_exc()

#         print("Error detected!")
#         print("Email sent at:", datetime.now())

#         send_error_email(error_details)

#     print("Waiting 60 seconds...")
#     time.sleep(60)



import os
import json
import time
import smtplib
from email.mime.text import MIMEText
# ---------------------------
# Configuration
# ---------------------------

with open("config.json", "r") as file:
    config = json.load(file)

folder_path = config["default_folder"]
ERROR_THRESHOLD = config["error_threshold"]
CHECK_INTERVAL_MINUTES = config["check_interval_minutes"]

STATE_FILE = "error_state.txt"


# ---------------------------
# Count Errors
# ---------------------------

def count_errors():

    error_count = 0

    for folder in os.listdir(folder_path):

        folder_full_path = os.path.join(folder_path, folder)

        if os.path.isdir(folder_full_path):

            for filename in os.listdir(folder_full_path):

                if filename.lower().endswith(".txt"):

                    file_path = os.path.join(
                        folder_full_path,
                        filename
                    )

                    try:
                        with open(
                            file_path,
                            "r",
                            errors="ignore"
                        ) as f:

                            for line in f:

                                if "ERROR" in line.upper():
                                    error_count += 1

                    except Exception as e:
                        print(
                            f"Could not read {file_path}: {e}"
                        )

    return error_count


# ---------------------------
# State File
# ---------------------------

def get_previous_count():

    if not os.path.exists(STATE_FILE):

        with open(STATE_FILE, "w") as f:
            f.write("0")

        return 0

    try:
        with open(STATE_FILE, "r") as f:
            return int(f.read().strip())

    except:
        return 0


def save_current_count(count):

    with open(STATE_FILE, "w") as f:
        f.write(str(count))


# ---------------------------
# Email Alert Placeholder
# ---------------------------

# import smtplib
# from email.mime.text import MIMEText

def send_email_alert(new_errors):
    print("Send_email_alert() called")
   
    sender_email =config["sender_email"]
    sender_password = config["sender_password"]
    receiver_email = config["receiver_email"]

    subject = "Naviga Log Alert"
    body = f"{new_errors} new errors detected."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        
        server.login(sender_email, sender_password)
        server.send_message(msg)

    print("Email alert sent.")

    # Email code will be added later


# ---------------------------
# Monitoring Loop
# ---------------------------

while True:

    current_count = count_errors()

    previous_count = get_previous_count()

    new_errors = current_count - previous_count

    print("\n--------------------")
    print("Previous Errors:", previous_count)
    print("Current Errors :", current_count)
    print("New Errors     :", new_errors)

    if config["email_alert_enabled"] and new_errors > ERROR_THRESHOLD:

        send_email_alert(new_errors)

    save_current_count(current_count)

    # print(
        # f"Waiting {CHECK_INTERVAL_MINUTES} minutes..."
    # )
    time.sleep(
        CHECK_INTERVAL_MINUTES * 60
    )