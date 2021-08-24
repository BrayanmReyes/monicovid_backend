from settings.layers.database import db, BaseModel


class Symptom(db.Model, BaseModel):
    __tablename__ = 'symptoms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))

    def __init__(self, name):
        self.name = name


class Comorbidity(db.Model, BaseModel):
    __tablename__ = 'comorbidities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))

    def __init__(self, name):
        self.name = name
