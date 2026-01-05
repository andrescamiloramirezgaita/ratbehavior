from flask import render_template, redirect, url_for,request
from . import main_bp
from flask_login import login_required, current_user
from models.fases import Fases


@main_bp.route('/')
def index():
    return redirect(url_for('main.perfil'))

@main_bp.route('/perfil')
@login_required
def perfil():
    lista_de_fases = Fases.query.all() 
    return render_template('auth/perfil.html', 
                           nombre=current_user.nombres,
                           fases=lista_de_fases)

## Agrego la ruta de ejemplo de la evaluación -- Andres Ramirez
@main_bp.route('/ejemplo')
@login_required
def ejemplo():
    # 1. Obtenemos el id de la fase desde la URL (ej: /ejemplo?fase_investigacion=2)
    fase_id = request.args.get('fase_investigacion', type=int)

    # 2. Si alguien intenta entrar a /ejemplo sin haber elegido una fase, lo regresamos al perfil.
    if not fase_id:
        return redirect(url_for('main.perfil'))
    return render_template('auth/ejemplo.html', fase_id=fase_id)