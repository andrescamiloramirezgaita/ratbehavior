from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
from flask_cors import CORS
from extensions import db
import config
from blueprints.main import main_bp
from blueprints.admin import admin_bp
from blueprints.evaluacion import evaluacion_bp # Ejercicio 
#from blueprints.ejemplo import ejemplo_bp # Nuevo
from blueprints.auth import auth_bp # Modulo de autenticación
from flask_login import LoginManager # para el login de usuarios
from models.usuarios import Usuarios 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SECRET_KEY'] = config.SECRET_KEY

db.init_app(app)
login_manager = LoginManager()
#login_manager.login_view = 'auth.login_post' #indica que, si un usuario no autenticado intenta acceder a una ruta protegida, será redirigido a /auth/login_post.
login_manager.login_view = 'auth.index' #indica que, si un usuario no autenticado intenta acceder a una ruta protegida, será redirigido a /auth/login_post.

login_manager.init_app(app) #vincula Flask-Login con la aplicación

#Cuando un usuario inicia sesión, Flask-Login almacena su ID en la sesión.
#Este método recupera el usuario desde la base de datos con Usuarios.query.get(int(user_id)).
@login_manager.user_loader
def load_user(user_id):
# since the user_id is just the primary key of our user table, use it in the query for the user
    return Usuarios.query.get(int(user_id))


CORS(app, resources={r"/*": {"origins": "*"}})

# # Inicialización de la estructura de datos para almacenar las observaciones
# data = {
#     "minute": [],
#     "palanqueo": [],
#     "levantamiento": [],
#     "acercamiento": []
# }

# @app.route('/log_observation', methods=['POST'])
# def log_observation():
#     global data
#     observation = request.json
#     minute = observation.get('minute')
#     action = observation.get('action')
    
#     if minute is not None and action in data:
#         data["minute"].append(minute)
#         data["palanqueo"].append(1 if action == "palanqueo" else 0)
#         data["levantamiento"].append(1 if action == "levantamiento" else 0)
#         data["acercamiento"].append(1 if action == "acercamiento" else 0)
#         return jsonify({"message": "Observation logged"}), 200
#     return jsonify({"message": "Invalid data"}), 400
    

# @app.route('/get_summary', methods=['GET'])
# def get_summary():
#     global data
#     df = pd.DataFrame(data)
#     summary = df.groupby('minute').sum().reset_index().to_dict(orient='records')
#     return jsonify(summary), 200


app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(evaluacion_bp, url_prefix='/evaluacion')
#app.register_blueprint(ejemplo_bp, url_prefix='/ejemplo') # Nuevo
app.register_blueprint(auth_bp, url_prefix='/auth') #las rutas relacionadas con autenticación estarán bajo el prefijo /auth


from models.ultimo_video import obtener_videos_por_codigo
@app.route('/probar_video/<codigo>')
def probar_video(codigo):
    video = obtener_videos_por_codigo(codigo)
    if video:
        video = video[0]  # Accede al primer video de la lista
        return f"ID: {video.id}, Video: {video.video}, Sección: {video.seccionvideo}"
    else:
        return "No se encontraron videos para este código."

if __name__ == '__main__':
    app.run(debug=True)
