from extensions import db
from dataclasses import dataclass

class Resultados(db.Model):
    id: int
    idevaluacion: int
    idvideo: int
    inicio: int
    fin: int    
    idfase: int
    idconducta: int
    puntuacion: int
    esperado: int
    obtenido: int

    id = db.Column(db.Integer, primary_key=True)
    idevaluacion = db.Column(db.Integer)
    idvideo = db.Column(db.Integer)
    inicio = db.Column(db.Integer)
    fin = db.Column(db.Integer)
    idfase = db.Column(db.Integer)
    idconducta = db.Column(db.Integer)
    puntuacion = db.Column(db.Integer)
    esperado = db.Column(db.Integer)
    obtenido = db.Column(db.Integer)
    

    def __repr__(self):
        return '<Resultados %r>' % self.id