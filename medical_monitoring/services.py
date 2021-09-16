from sqlalchemy import func
from io import BytesIO
from medical_monitoring.models import HealthReport, Monitoring
from profiles.models import Contact
from medical_risks.services import find_symptom, find_oxygen, find_temperature
from settings.exceptions import NotFoundException
from settings.layers.mail import send_email
import xlsxwriter

from profiles.services import find_patient


def get_param(params, search):
    return int(params.get(search)) if params.get(search) else None


def find_health_report(health_report_id):
    health_report = HealthReport.get_by_id(health_report_id)
    if health_report is not None:
        return health_report
    else:
        raise NotFoundException('health_report', 'id', health_report_id)


def find_monitoring(doctor_id, patient_id):
    filters = {'doctor_id': doctor_id, 'patient_id': patient_id}
    monitoring = Monitoring.get_one(**filters)
    if monitoring is not None:
        return monitoring
    else:
        raise NotFoundException('monitoring', 'id', f'doctor_id: {doctor_id}, patient_id: {patient_id}')


def find_exist_monitoring(patient_id, is_active):
    filters = {'patient_id': patient_id, 'is_active': is_active}
    monitoring = Monitoring.get_one(**filters)
    if monitoring is not None:
        return monitoring
    else:
        return None


def send_mail_if_is_serious(health_report):
    patient = health_report.patient
    oxygen = health_report.oxygen
    temperature = health_report.temperature
    if oxygen.value < 92.0 or temperature.value > 38.0:
        patient_id = patient.id
        contacts = Contact.simple_filter(**{'patient_id': patient_id})
        if len(contacts) != 0:
            emails = []
            for contact in contacts:
                emails.append(contact.email)
                send_email('Follow-up report',
                           f'The patient {patient.first_name} has registered his follow-up'
                           f' report, and is in poor health with oxygenation of {oxygen.value} and a'
                           f' temperature of {temperature.value}. Take into consideration,'
                           f' and go to the doctor as soon as possible in case the patient situation'
                           f' deteriorates.', emails)
        send_email('Follow-up report', 'According to what you have entered in the report, you are in poor health,'
                                       ' take special care of your treatment and contact your doctor', [patient.email])
        # sms.send_message({
        #     'from': 'Vonage APIs',
        #     'to': f'51{patient.phone}',
        #     'text': 'According to what you have entered in the report, you are in poor health,'
        #             ' take special care of your treatment and contact your doctor'
        # })


def save_health_report(health_report, patient_id, oxygen_id, temperature_id, symptom_ids):
    symptoms = []
    health_report.patient_id = patient_id
    if oxygen_id is not None:
        if find_oxygen(oxygen_id):
            health_report.oxygen_id = oxygen_id
    if temperature_id is not None:
        if find_temperature(temperature_id):
            health_report.temperature_id = temperature_id
    if symptom_ids is not None:
        for symptom_id in symptom_ids:
            symptom = find_symptom(symptom_id)
            symptoms.append(symptom)
    created = health_report.save()
    if len(symptoms) != 0:
        for symptom in symptoms:
            created.symptoms.append(symptom)
    created.commit()
    send_mail_if_is_serious(health_report)
    return created


def get_last_health_report(patient_id):
    health_reports = HealthReport.simple_filter(**{'patient_id': patient_id})
    if len(health_reports) != 0:
        health_reports.sort(key=lambda r: r.register_date)
        last_health_report = health_reports[-1]
        return last_health_report


def create_monitoring(monitoring):
    previous_monitoring = find_exist_monitoring(monitoring.patient_id, True)
    if previous_monitoring:
        previous_monitoring.is_active = False
        previous_monitoring.end_date = func.now()
        previous_monitoring.commit()
        return monitoring.save()
    else:
        return monitoring.save()


def report_excel(health_report):
    f = BytesIO()
    workbook = xlsxwriter.Workbook(f)
    worksheet = workbook.add_worksheet('Report')
    worksheet.write('B3', 'Paciente')
    worksheet.write('C3', f'{health_report.patient.first_name} {health_report.patient.last_name}')
    worksheet.write('B4', 'Observación')
    worksheet.write('C4', health_report.observation)
    worksheet.write('B5', 'Tuvo contacto con un infectado')
    worksheet.write('C5', 'Si' if health_report.is_contact_with_infected else 'No')
    worksheet.write('B6', 'Oxigeno')
    worksheet.write('C6', health_report.oxygen.value)
    worksheet.write('B7', 'Temperatura')
    worksheet.write('C7', health_report.temperature.value)
    worksheet.write('B8', 'Fecha de registro')
    worksheet.write('C8', f'{health_report.register_date}')
    worksheet.write('B9', 'Sintomas')
    for index, symptom in enumerate(health_report.symptoms.filter().all()):
        worksheet.write(9, index + 1, symptom.name)
    worksheet.write('B11', 'Comorbilidades')
    patient = find_patient(health_report.patient.id)
    for index, comorbidity in enumerate(patient.comorbidities.filter().all()):
        worksheet.write(11, index + 1, comorbidity.name)
    workbook.close()
    return f.getvalue()
