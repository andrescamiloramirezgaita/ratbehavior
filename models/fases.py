from extensions import db
from dataclasses import dataclass

@dataclass
class Fases(db.Model):
    id: int
    nombre: str

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))

    def __repr__(self):
        return '<Fases %r>' % self.id