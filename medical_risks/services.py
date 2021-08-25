from medical_risks.models import Symptom, Comorbidity
from settings.exceptions import NotFoundException


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
