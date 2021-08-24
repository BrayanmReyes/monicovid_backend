from settings.layers.database import db, BaseModel


class Oxygen(db.Model, BaseModel):
    __tablename__ = 'oxygens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float, nullable=False)
    register_date = db.Column(db.Date, nullable=False)

    def __init__(self, name):
        self.name = name
