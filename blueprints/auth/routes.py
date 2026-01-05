from flask import render_template, request, redirect, url_for
from extensions import db
from sqlalchemy import func
from . import auth_bp
from models.usuarios import Usuarios
from models.evaluaciones import Evaluaciones
from models.fases import Fases 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

#Simplemente muestra la plantilla login.html con un formulario para que el usuario ingrese sus credenciales.@auth_bp.route('/login')
@auth_bp.route('/')  # Agrega esta línea
def index():        
    return render_template('auth/login.html')

#1. Obtiene los datos enviados por el usuario (p_codigo y p_password).
#2. Busca al usuario en la base de datos con Usuarios.query.filter_by(codigo=p_codigo).first().
#3. Si el usuario existe, compara la contraseña ingresada con la contraseña almacenada en la BD usando check_password_hash().
#4. Si la contraseña es correcta, usa login_user(usuario, remember=True) para iniciar la sesión.
#5. Redirige al usuario según su rol (perfil o auth.list).
#6. Si los datos son incorrectos, muestra un mensaje de error.

@auth_bp.route('/login', methods=['POST'])
def login_post():
    p_codigo = request.form['codigo']
    p_password = request.form['password']
    #Validar esto:
    # remember = True if request.form.get('remember') else False
    usuario = Usuarios.query.filter_by(codigo=p_codigo).first()
    if usuario and check_password_hash(usuario.password, p_password):
        login_user(usuario, remember=True)
        if usuario.idrol == 1:
            return redirect(url_for('main.perfil'))
        else:
            return redirect(url_for('auth.list'))
    else:
        return render_template('auth/login.html', error='Usuario o contraseña incorrectos')

@auth_bp.route('/signup')
def signup():
    return render_template('auth/signup.html')

#Crear un nuevo usuario
@auth_bp.route('/register', methods=['POST'])
def register():
    p_codigo = request.form['codigo']
    p_nombres = request.form['nombres']
    p_apellidos = request.form['apellidos']
    p_email = request.form['email']
    p_password = request.form['password']

    #Validar si el usuario ya existe
    usuario = Usuarios.query.filter_by(codigo=p_codigo).first()
    if usuario:
        return render_template('auth/signup.html', error='El usuario ya existe')
    else:
        usuario = Usuarios(codigo=p_codigo, nombres=p_nombres, apellidos=p_apellidos, email=p_email, password=generate_password_hash(p_password, method='pbkdf2'),idrol=1)
        db.session.add(usuario)
        db.session.commit()

    return redirect(url_for('auth.list'))   

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@auth_bp.route('/list')
@login_required
def list():
    #Filtro por estudiantes
    usuarios = Usuarios.query.filter_by(idrol=1).all()
    return render_template('auth/list.html', usuarios=usuarios)


@auth_bp.route('/usuarios-evaluaciones')
def usuarios_evaluaciones():
    # Subconsulta para obtener el máximo 'resultado' por cada usuario (usando 'codigo' como clave)
    subquery = db.session.query(
        Evaluaciones.codigo,
        func.max(Evaluaciones.resultado).label('max_resultado')
    ).group_by(Evaluaciones.codigo).subquery()

    # Consulta principal para obtener los usuarios y sus evaluaciones con el resultado más alto
    query = db.session.query(
        Usuarios.nombres,
        Usuarios.apellidos,
        Evaluaciones.resultado,
        Evaluaciones.fecha
    ).join(
        subquery, subquery.c.codigo == Usuarios.codigo
    ).join(
        Evaluaciones, (Evaluaciones.codigo == Usuarios.codigo) & (Evaluaciones.resultado == subquery.c.max_resultado)
    )

    # Ejecutar la consulta y obtener los resultados
    usuarios_evaluaciones = query.all()

    # Renderizamos los datos en la plantilla
    return render_template('auth/usuarios_evaluaciones.html', usuarios_evaluaciones=usuarios_evaluaciones)