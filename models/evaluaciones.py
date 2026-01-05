from extensions import db
from dataclasses import dataclass

@dataclass
class Evaluaciones(db.Model):
    id: int
    codigo: str
    fecha: str

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10))
    fecha = db.Column(db.DateTime())
    resultado = db.Column(db.Float())
    

    def __repr__(self):
        return '<Evaluaciones %r>' % self.id