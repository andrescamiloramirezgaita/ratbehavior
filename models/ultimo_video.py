from extensions import db 
from dataclasses import dataclass
from sqlalchemy import text

# Esta clase es solo para representar el resultado
@dataclass
class VideoSeleccionado:
    id: int
    video: str
    seccionvideo: int

# Determina el último video que evaluó el estudiante
def obtener_videos_por_codigo(codigo,fase_prueba):
    sql = text("""
        SELECT DISTINCT v.id, v.video, v.seccionvideo
        FROM resultados r
        INNER JOIN videos v ON v.id = r.idvideo
        WHERE idevaluacion = (
            SELECT MAX(e.id)
            FROM evaluaciones e
            INNER JOIN resultados r ON e.id = r.idevaluacion
            WHERE codigo = :codigo
            AND r.idfase = :fase
        )
    """)
    result = db.session.execute(sql, {'codigo': codigo,'fase':fase_prueba})
    videos = [VideoSeleccionado(id=row[0], video=row[1], seccionvideo=row[2]) for row in result]
    return videos
