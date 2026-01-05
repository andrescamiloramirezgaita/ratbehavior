from extensions import db
from dataclasses import dataclass

@dataclass
class FasesConductasView(db.Model):
    __tablename__ = 'fases_conductas_view'
    __table_args__ = {'extend_existing': True}

    id: int
    idfase: int
    idconducta: int
    fase: str
    conducta: str

    id = db.Column(db.Integer, primary_key=True)
    idfase = db.Column(db.Integer)
    idconducta = db.Column(db.Integer)
    fase = db.Column(db.String(100))
    conducta = db.Column(db.String(100))

    def __repr__(self):
        return '<FasesConductasView %r>' % self.id
