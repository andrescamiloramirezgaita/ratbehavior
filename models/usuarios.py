from extensions import db
from dataclasses import dataclass
from flask_login import UserMixin

@dataclass
class Usuarios(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    __table_args__ = {'extend_existing': True}

    id: int
    codigo: str
    email: str
    password: str
    nombres: str
    apellidos: str
    idrol: int

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    idrol = db.Column(db.Integer)  

    def __repr__(self):
        return '<Usuarios %r>' % self.id