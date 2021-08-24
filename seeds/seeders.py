from flask_seeder import Seeder
from medical_risks.models import Comorbidity, Symptom


class ComorbiditySeeder(Seeder):
    def run(self):
        values = ['Obesidad', 'Diabetes', 'Hipertensión', 'Enf.Resp.Crónica', 'Enf.Cardiovascular']
        for index, value in enumerate(values):
            comorbidity = Comorbidity(value)
            self.db.session.add(comorbidity)


class SymptomSeeder(Seeder):
    def run(self):
        values = ['Dolor Muscular o articulaciones', 'Malestar general o fatiga', 'Tos seca', 'Dolor de garganta',
                  'Pérdida del gusto', 'Pérdida del olfato', 'Enrojecimiento de la piel', 'Diarrea', 'Vómitos']
        for index, value in enumerate(values):
            symptom = Symptom(value)
            self.db.session.add(symptom)
