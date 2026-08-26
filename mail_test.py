import os
import smtplib
from email.message import EmailMessage


SMTP_SERVER = "mx.freenet.de"
SMTP_PORT = 587

sender = os.environ["FREENET_EMAIL"]
password = os.environ["FREENET_PASSWORD"]
recipient = os.environ["MAIL_TO"]


print("Verbinde mit Freenet SMTP...")

with smtplib.SMTP(
    SMTP_SERVER,
    SMTP_PORT,
    timeout=30
) as server:

    print("EHLO...")
    print(server.ehlo())

    print("STARTTLS...")
    print(server.starttls())

    print("EHLO nach TLS...")
    print(server.ehlo())

    print("Login...")
    print(server.login(sender, password))

    print("Login erfolgreich.")

    print("MAIL FROM...")
    print(
        server.mail(
            sender,
            options=["SMTPUTF8"]
        )
    )

    print("RCPT TO...")
    print(
        server.rcpt(
            recipient
        )
    )

    print("DATA...")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "STELLA Monitor Test"

    msg.set_content(
        "Dies ist eine Testmail des "
        "STELLA-NRW-Monitors.\n\n"
        "Viele Grüße\n"
        "STELLA Monitor"
    )

    print(
        server.data(
            msg.as_bytes()
        )
    )

    print("E-Mail erfolgreich versendet.")

print("FERTIG")
