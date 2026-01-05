from extensions import db
from dataclasses import dataclass

@dataclass
class Conductas(db.Model):
    __tablename__ = 'conductas'
    __table_args__ = {'extend_existing': True}

    id: int
    nombre: str
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    

    def __repr__(self):
        return '<Conductas %r>' % self.id