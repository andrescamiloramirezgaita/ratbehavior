from extensions import db
from dataclasses import dataclass

@dataclass
class Videos(db.Model):
    __tablename__ = 'videos'
    __table_args__ = {'extend_existing': True}

    id: int
    urlvideo: str
    descripcion: str
    seccionvideo: str #nuevo
    
    id = db.Column(db.Integer, primary_key=True)
    urlvideo = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
    seccionvideo = db.Column(db.Integer) #nuevo
    video =db.Column(db.Integer) #nuevo
    

    def __repr__(self):
        return '<videos %r>' % self.id