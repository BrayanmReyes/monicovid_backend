from medical_monitoring.models import HealthReport
import datetime as hours
from datetime import datetime

from profiles.models import Patient
from settings.layers.mail import send_email
from settings.layers.scheduler import scheduler


def alert_report():
    with scheduler.app.app_context():
        patients = Patient.get_all()
        for patient in patients:
            if not patient.recovered:
                reports = HealthReport.simple_filter(**{'patient_id': patient.id})
                if len(reports) != 0:
                    reports.sort(key=lambda r: r.register_date)
                    last_report = reports[-1]
                    next_report_date = last_report.register_date + hours.timedelta(hours=8)
                    if calculate_time(last_report.register_date):
                        send_email('Reminder about your report',
                                   f'We remind you that you must make your next report at {next_report_date}.'
                                   f' Sincerely, monicovid services.',
                                   [patient.email])
                else:
                    continue


def calculate_time(last_report_date):
    actual_date = datetime.now()
    difference = actual_date - last_report_date
    difference_min = difference.total_seconds() // 60
    if 415 <= difference_min <= 425:
        return True
    else:
        return False
