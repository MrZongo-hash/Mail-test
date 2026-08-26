import os
import smtplib


SMTP_SERVER = "mx.freenet.de"
SMTP_PORT = 587

sender = os.environ["FREENET_EMAIL"]
password = os.environ["FREENET_PASSWORD"]
recipient = os.environ["MAIL_TO"]


print("Verbinde mit Freenet...")

with smtplib.SMTP(
    SMTP_SERVER,
    SMTP_PORT,
    timeout=30
) as server:

    print("EHLO...")
    server.ehlo()

    print("STARTTLS...")
    server.starttls()

    print("EHLO nach TLS...")
    server.ehlo()

    print("Login...")
    server.login(sender, password)

    print("Login erfolgreich.")

    print("Sende Testmail...")

    result = server.sendmail(
        sender,
        [recipient],
        f"""From: {sender}
To: {recipient}
Subject: STELLA Mail Test

Dies ist eine Testmail des STELLA-Monitors.
"""
    )

    print("sendmail Ergebnis:")
    print(result)

print("FERTIG")
