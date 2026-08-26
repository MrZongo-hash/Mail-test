import os
import smtplib
from email.message import EmailMessage


SMTP_SERVER = "mx.freenet.de"
SMTP_PORT = 465

sender = os.environ["FREENET_EMAIL"]
password = os.environ["FREENET_PASSWORD"]
recipient = os.environ["MAIL_TO"]


print("Verbinde mit Freenet SMTP über Port 465...")

with smtplib.SMTP_SSL(
    SMTP_SERVER,
    SMTP_PORT,
    timeout=30
) as server:

    print("SSL-Verbindung hergestellt.")

    print("Login...")
    server.login(sender, password)

    print("Login erfolgreich.")

    msg = EmailMessage()

    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "STELLA Monitor – E-Mail-Test"

    msg.set_content(
        "Hallo,\n\n"
        "dies ist eine Test-E-Mail für den "
        "STELLA-NRW-Monitor.\n\n"
        "Wenn diese Nachricht angekommen ist, "
        "funktioniert der E-Mail-Versand über Freenet.\n\n"
        "Viele Grüße\n"
        "STELLA Monitor"
    )

    print("Sende Testmail...")

    server.send_message(msg)

    print("E-Mail erfolgreich versendet.")

print("FERTIG")
