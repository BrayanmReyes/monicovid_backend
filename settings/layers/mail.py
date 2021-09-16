from flask_mail import Mail, Message


mail = Mail()
report_excel_name = 'report.xlsx'


def send_email(subject, text, recipients):
    message = Message(subject=subject, body=text, recipients=recipients)
    # if file is not None:
    #     message.attach(report_excel_name, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #                    report_excel(file))
    mail.send(message)
    return True
