import os
import smtplib


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

    message = f"""From: {sender}
To: {recipient}
Subject: STELLA Mail Test

Dies ist eine Testmail des STELLA-Monitors.

Der Versand über Freenet SMTP funktioniert.
"""

    print("Sende Testmail...")

    server.sendmail(
        sender,
        [recipient],
        message
    )

    print("E-Mail erfolgreich versendet.")

print("FERTIG")
