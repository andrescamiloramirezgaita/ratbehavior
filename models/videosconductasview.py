from extensions import db
from dataclasses import dataclass

@dataclass
class VideosConductasView(db.Model):
    __tablename__ = 'videos_conductas_view'
    __table_args__ = {'extend_existing': True}

    id: int
    idvideo: int
    inicio: int
    fin: int
    nombre: str
    cantidad: int
   
    id = db.Column(db.Integer, primary_key=True)
    idvideo = db.Column(db.Integer)
    inicio = db.Column(db.Integer)
    fin = db.Column(db.Integer)
    nombre = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    

    def __repr__(self):
        return '<VideosConductasView %r>' % self.id