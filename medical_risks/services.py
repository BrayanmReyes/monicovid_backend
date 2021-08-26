from medical_risks.models import Symptom, Comorbidity, Oxygen, Temperature
from settings.exceptions import NotFoundException


def get_param(params, search):
    return int(params.get(search)) if params.get(search) else None


def find_symptom(symptom_id):
    symptom = Symptom.get_by_id(symptom_id)
    if symptom:
        return symptom
    else:
        raise NotFoundException('symptom', 'id', symptom_id)


def find_comorbidity(comorbidity_id):
    comorbidity = Comorbidity.get_by_id(comorbidity_id)
    if comorbidity:
        return comorbidity
    else:
        raise NotFoundException('comorbidity', 'id', comorbidity)


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
