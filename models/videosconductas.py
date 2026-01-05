from extensions import db
from dataclasses import dataclass

@dataclass
class VideosConductas(db.Model):
    id: int
    idvideo: int
    inicio: int
    fin: int
    idfaseconducta: int
    cantidad: int

    id = db.Column(db.Integer, primary_key=True)
    idvideo = db.Column(db.Integer)
    inicio = db.Column(db.Integer)
    fin = db.Column(db.Integer)
    idfaseconducta = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    

    def __repr__(self):
        return '<VideosConductas %r>' % self.id