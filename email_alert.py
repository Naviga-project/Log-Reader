import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load configuration
with open("config.json", "r") as file:
    config = json.load(file)


def send_email(subject, body):

    if not config["email_alert_enabled"]:
        return

    try:
        msg = MIMEMultipart()

        msg["From"] = config["sender_email"]
        msg["To"] = config["receiver_email"]
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(
            config["smtp_server"],
            config["smtp_port"]
        )

        server.starttls()

        server.login(
            config["sender_email"],
            config["sender_password"]
        )

        server.send_message(msg)

        server.quit()

        print("✅ Email Sent Successfully")

    except Exception as e:
        print("Email Error:", e)