import os
import smtplib
from email.message import EmailMessage


SMTP_SERVER = "mx.freenet.de"
SMTP_PORT = 587

sender = os.environ["FREENET_EMAIL"]
password = os.environ["FREENET_PASSWORD"]
recipient = os.environ["MAIL_TO"]


print("Verbinde mit Freenet SMTP...")

server = smtplib.SMTP(
    SMTP_SERVER,
    SMTP_PORT,
    timeout=30
)

try:
    print("EHLO...")
    code, response = server.ehlo()
    print(code, response)

    print("STARTTLS...")
    code, response = server.starttls()
    print(code, response)

    print("EHLO nach TLS...")
    code, response = server.ehlo()
    print(code, response)

    print("Login...")
    code, response = server.docmd(
        "AUTH",
        "LOGIN"
    )
    print(code, response)

    # Falls AUTH LOGIN erfolgreich gestartet wurde,
    # müssen Benutzername und Passwort separat übertragen werden.
    if code != 334:
        raise RuntimeError(
            f"AUTH LOGIN konnte nicht gestartet werden: {code} {response}"
        )

    import base64

    username_encoded = base64.b64encode(
        sender.encode("utf-8")
    ).decode("ascii")

    password_encoded = base64.b64encode(
        password.encode("utf-8")
    ).decode("ascii")

    print("Benutzername senden...")
    code, response = server.docmd(
        "",
        username_encoded
    )
    print(code, response)

    if code != 334:
        raise RuntimeError(
            f"Benutzername wurde abgelehnt: {code} {response}"
        )

    print("Passwort senden...")
    code, response = server.docmd(
        "",
        password_encoded
    )
    print(code, response)

    if code != 235:
        raise RuntimeError(
            f"Authentifizierung fehlgeschlagen: {code} {response}"
        )

    print("Login erfolgreich.")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "STELLA Monitor Test"

    msg.set_content(
        "Dies ist eine Testmail des STELLA-NRW-Monitors.\n\n"
        "Der Freenet-SMTP-Versand wird getestet.\n\n"
        "Viele Grüße\n"
        "STELLA Monitor"
    )

    print("Sende E-Mail...")

    code, response = server.mail(sender)
    print("MAIL FROM:", code, response)

    if code != 250:
        raise RuntimeError(
            f"MAIL FROM abgelehnt: {code} {response}"
        )

    code, response = server.rcpt(recipient)
    print("RCPT TO:", code, response)

    if code != 250:
        raise RuntimeError(
            f"RCPT TO abgelehnt: {code} {response}"
        )

    code, response = server.data(msg.as_bytes())
    print("DATA:", code, response)

    if code != 250:
        raise RuntimeError(
            f"DATA abgelehnt: {code} {response}"
        )

    print("E-Mail erfolgreich versendet.")

finally:
    print("Schließe Verbindung...")
    server.quit()

print("FERTIG")
