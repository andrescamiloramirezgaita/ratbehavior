from flask import Blueprint
evaluacion_bp = Blueprint('evaluacion', __name__)
#evaluacion_bp = Blueprint('evaluacion', __name__, template_folder='templates')
from . import routes