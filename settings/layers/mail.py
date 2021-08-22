from flask_mail import Mail, Message

mail = Mail()


def send_email(subject, text, recipients):
    message = Message(subject=subject, body=text, recipients=recipients)
    mail.send(message)
    return True
