from medical_monitoring.models import Oxygen, Temperature, HealthReport
from profiles.models import Contact
from medical_risks.services import find_symptom
from settings.exceptions import NotFoundException
from settings.layers.mail import send_email


def get_param(params, search):
    return int(params.get(search)) if params.get(search) else None


def find_oxygen(oxygen_id):
    oxygen = Oxygen.get_by_id(oxygen_id)
    if oxygen:
        return oxygen
    else:
        raise NotFoundException('oxygen', 'id', oxygen_id)


def find_temperature(temperature_id):
    temperature = Temperature.get_by_id(temperature_id)
    if temperature:
        return temperature
    else:
        raise NotFoundException('temperature', 'id', temperature_id)


def find_health_report(health_report_id):
    health_report = HealthReport.get_by_id(health_report_id)
    if health_report is not None:
        return health_report
    else:
        raise NotFoundException('health_report', 'id', health_report_id)


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
    verify_if_is_serious(created.patient, created.oxygen, created.temperature)
    return created


def verify_if_is_serious(patient, oxygen, temperature):
    if oxygen.value < 92.0 or temperature.value > 38.0:
        patient_id = patient.id
        contacts = Contact.simple_filter(**{'patient_id': patient_id})
        if len(contacts) != 0:
            emails = []
            for contact in contacts:
                emails.append(contact.email)
            send_email('Follow-up report', f'The patient {patient.first_name} has registered his follow-up'
                                           f' report, and is in poor health with oxygenation of {oxygen.value} and a'
                                           f' temperature of {temperature.value}. Take into consideration,'
                                           f' and go to the doctor as soon as possible in case the patient situation'
                                           f' deteriorates.', emails)
        send_email('Follow-up report', 'According to what you have entered in the report, you are in poor health,'
                                       ' take special care of your treatment and contact your doctor',
                   [patient.email])
