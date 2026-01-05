from flask import render_template, request, jsonify, abort, redirect, url_for
from . import evaluacion_bp
from models.fasesconductasview import FasesConductasView
from models.evaluaciones import Evaluaciones
from models.fases import Fases
from models.videosconductas import VideosConductas
from models.videosconductasview import VideosConductasView
from models.resultados import Resultados
from models.conductas import Conductas
from models.videos import Videos
from models.ultimo_video import obtener_videos_por_codigo
from flask_login import login_required, current_user
from datetime import datetime
from extensions import db
import pandas as pd
from sqlalchemy import and_
import json

@evaluacion_bp.route('/')
@login_required

def index():
    try:
        # Leer el valor 'fase_investigacion' de la URL.
        # El nombre 'fase_investigacion' debe coincidir con el atributo 'name' del <select> en el HTML.
        # Lo convertimos a entero (type=int)
        fase_prueba = request.args.get('fase_investigacion', type=int)

        print(f"\n\n>>>>>>>>>> DEBUG: El ID de la fase es: {fase_prueba} <<<<<<<<<<\n\n")

        # PASO 2: Validar que se recibió un id. Si no, redirigir al perfil para que elija.
        if not fase_prueba:
            # Aquí podrías agregar un mensaje de error si quieres, usando flash()
            return redirect(url_for('main.perfil'))
        
        # Obtener las fases y conductas. Esto se utiliza para crear los botones de las conductas asociadas con cada fase.
        fases_conductas = FasesConductasView.query.filter_by(idfase=fase_prueba).all()

        # Obtener la fase. Esto se usa para colocar el nombre de la fase en la página
        fase = Fases.query.filter_by(id=fase_prueba).first()

        # Crear una nueva evaluación. Se crea encabezado de la evaluación del estudiante
        evaluacion = Evaluaciones(codigo=current_user.codigo, fecha=datetime.now())
        db.session.add(evaluacion)
        db.session.commit()
        
        print(f"\n\n>>>>>>>>>> DEBUG: El ID de la evaluación es: {evaluacion} <<<<<<<<<<\n\n")

        # Obtener el último id de la evaluación. Esto se utiliza para almacenar en la tabla de resultados de la evaluación
        idevaluacion = evaluacion.id

        # Lista de videos de la fase
        # Acceder a los valores de la columna id
        ids_fases_conductas = [fc.id for fc in fases_conductas]
        video_conductas = VideosConductas.query.filter(VideosConductas.idfaseconducta.in_(ids_fases_conductas)).all()
        list_video_conductas = [video.idvideo for video in video_conductas]
        url_videos = Videos.query.filter(Videos.id.in_(list_video_conductas)).all()
        #Definir el último video que estudiante evaluo

        ult_video = obtener_videos_por_codigo(current_user.codigo, fase_prueba)

        print(f"\n\n>>>>>>>>>> DEBUG: El ID de las fases conductas es: {ids_fases_conductas} <<<<<<<<<<\n\n")


        # Lista de url de videos
        list_url_videos = [url.urlvideo for url in url_videos]
        list_url_videos_json = json.dumps(list_url_videos)

        print(f"\n\n>>>>>>>>>> DEBUG: Lista de todos los videos: {video_conductas} <<<<<<<<<<\n\n")


        # Lista de id de videos
        list_id_videos = [video.id for video in url_videos]
        list_id_videos_json = json.dumps(list_id_videos)
        
        # Lista del numero del video padre
        list_video = [video.video for video in url_videos]
        list_video_json = json.dumps(list_video)

        # Lista de secciones de videos
        list_seccion_videos = [video.seccionvideo for video in url_videos]
        list_seccion_videos_json = json.dumps(list_seccion_videos)
        
        # id del último video
        id_ultimo_video = [video.id for video in ult_video]
        id_ultimo_video_json = json.dumps(id_ultimo_video)

        # codigo del último video
        codigo_ultimo_video = [video.video for video in ult_video]
        codigo_ultimo_video_json = json.dumps(codigo_ultimo_video)

        # seccion del último video
        seccion_ultimo_video = [video.seccionvideo for video in ult_video]
        seccion_ultimo_video_json = json.dumps(seccion_ultimo_video)

        print(f"\n\n>>>>>>>>>> DEBUG: current_user: { current_user} <<<<<<<<<<\n\n")
        print(f"\n\n>>>>>>>>>> DEBUG: fase.nombre: { fase.nombre} <<<<<<<<<<\n\n")
        print(f"\n\n>>>>>>>>>> DEBUG: fases_conductas: { fases_conductas} <<<<<<<<<<\n\n")
        print(f"\n\n>>>>>>>>>> DEBUG: idevaluacion: { idevaluacion} <<<<<<<<<<\n\n")

        print(f"\n\n>>>>>>>>>> DEBUG: list_url_videos_json: { list_url_videos_json} <<<<<<<<<<\n\n")
        print(f"\n\n>>>>>>>>>> DEBUG: list_seccion_videos_json: { list_seccion_videos_json} <<<<<<<<<<\n\n")
        print(f"\n\n>>>>>>>>>> DEBUG: list_id_videos: { list_id_videos} <<<<<<<<<<\n\n")
        print(f"\n\n>>>>>>>>>> DEBUG: list_video_json: { list_video_json} <<<<<<<<<<\n\n")

        print(f"\n\n>>>>>>>>>> DEBUG: list_seccion_videos_json: { list_seccion_videos_json} <<<<<<<<<<\n\n")
        print(f"\n\n>>>>>>>>>> DEBUG: id_ultimo_video_json: {id_ultimo_video_json} <<<<<<<<<<\n\n")
        print(f"\n\n>>>>>>>>>> DEBUG: codigo_ultimo_video_json: {codigo_ultimo_video_json} <<<<<<<<<<\n\n")
        print(f"\n\n>>>>>>>>>> DEBUG: Seccion ultimo video: {seccion_ultimo_video_json} <<<<<<<<<<\n\n")
 
        return render_template('evaluacion/index.html', 
                               usuario=current_user, 
                               nombre_fase=fase.nombre,
                               fases_conductas=fases_conductas,                               
                               idevaluacion=idevaluacion,
                               list_url_videos=list_url_videos_json,
                               list_id_videos=list_id_videos_json,
                               list_video=list_video_json,
                               list_seccion_videos=list_seccion_videos_json,
                               ultimo_video_id=id_ultimo_video_json,
                               ultimo_video_codigo=codigo_ultimo_video_json,
                               ultimo_video_seccion=seccion_ultimo_video_json
                               )

    
    except Exception as e:
        print(f"Error: {e}")
        return "Ha ocurrido un error", 500


@evaluacion_bp.route('/videosconductas/<int:idvideo>')
def videosconductas(idvideo):
    #Obtener la tabla con los resultados de validados del video
    videos_conductas = VideosConductas.query.filter_by(idvideo=idvideo).all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if len(videos_conductas) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'videos_conductas': videos_conductas            
        })
    
@evaluacion_bp.route('/videosconductasview/<int:idvideo>')
def videosconductasview(idvideo):
    #Obtener la tabla con los resultados de validados del video
    videos_conductas_view = VideosConductasView.query.filter_by(idvideo=idvideo).all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if len(videos_conductas_view) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'videos_conductas_view': videos_conductas_view            
        })

#Obterner los resultados de la evaluación
@evaluacion_bp.route('/guardar_datos', methods=['POST'])
def guardar_datos():
    totalfila = 0

    datos = request.json.get('matriz_datos')
    idvideo = request.json.get('idvideo')
    idevaluacion = request.json.get('idevaluacion')
    nombreFase = request.json.get('nombrefase')
    
    videoconductaresultados = VideosConductasView.query.filter_by(idvideo=idvideo).all()
    videoconductaresultados_list = [resultado for resultado in videoconductaresultados]
    fases_list = [fases for fases in Fases.query.all()]
    conductas_list = [conductas for conductas in Conductas.query.all()]
    
    print(f"\n\n>>>>>>>>>> DEBUG: idevaluacion: { nombreFase} <<<<<<<<<<\n\n")

        
    resultados = []

    for dato in datos:
        inicio = dato[1].split('-')[0].strip()
        fin = dato[1].split('-')[1].strip()

        if nombreFase in ('Habituación','Mantenimiento','Extinción'):
            accion = 'Palanqueo'
            cantidad = retornaCantidad(videoconductaresultados_list, inicio, fin, accion)
                
            if dato[2] == cantidad:
                totalfila += 1
                    
            resultados.append(guarda_lista_resultados(idevaluacion, idvideo, inicio, fin, nombreFase, accion, cantidad, dato[2],fases_list,conductas_list))

            accion = 'Levantamiento'
            cantidad = retornaCantidad(videoconductaresultados_list, inicio, fin, accion)
            if dato[3] == cantidad:
                totalfila += 1
        
            resultados.append(guarda_lista_resultados(idevaluacion, idvideo, inicio, fin, nombreFase, accion, cantidad, dato[3],fases_list,conductas_list))

            accion = 'Acercamiento'
            cantidad = retornaCantidad(videoconductaresultados_list, inicio, fin, accion)
            if dato[4] == cantidad:
                totalfila += 1
       
            resultados.append(guarda_lista_resultados(idevaluacion, idvideo, inicio, fin, nombreFase, accion, cantidad, dato[4],fases_list,conductas_list))

        if nombreFase in ('Moldeamiento'):
            accion = 'Palanqueo'
            cantidad = retornaCantidad(videoconductaresultados_list, inicio, fin, accion)
                
            if dato[2] == cantidad:
                totalfila += 1
                    
            resultados.append(guarda_lista_resultados(idevaluacion, idvideo, inicio, fin, nombreFase, accion, cantidad, dato[2],fases_list,conductas_list))

            accion = 'Comedero'
            cantidad = retornaCantidad(videoconductaresultados_list, inicio, fin, accion)
            if dato[5] == cantidad:
                totalfila += 1
        
            resultados.append(guarda_lista_resultados(idevaluacion, idvideo, inicio, fin, nombreFase, accion, cantidad, dato[5],fases_list,conductas_list))

            accion = 'Aproximación'
            cantidad = retornaCantidad(videoconductaresultados_list, inicio, fin, accion)
            if dato[6] == cantidad:
                totalfila += 1
       
            resultados.append(guarda_lista_resultados(idevaluacion, idvideo, inicio, fin, nombreFase, accion, cantidad, dato[6],fases_list,conductas_list))

            accion = 'Tocar Palanca'
            cantidad = retornaCantidad(videoconductaresultados_list, inicio, fin, accion)
            if dato[7] == cantidad:
                totalfila += 1
       
            resultados.append(guarda_lista_resultados(idevaluacion, idvideo, inicio, fin, nombreFase, accion, cantidad, dato[7],fases_list,conductas_list))


        if nombreFase in ('Refuerzo'):
            accion = 'Palanqueo Reforzado'
            cantidad = retornaCantidad(videoconductaresultados_list, inicio, fin, accion)
                
            if dato[2] == cantidad:
                totalfila += 1
                    
            resultados.append(guarda_lista_resultados(idevaluacion, idvideo, inicio, fin, nombreFase, accion, cantidad, dato[8],fases_list,conductas_list))

            accion = 'Palanqueo No Reforzado'
            cantidad = retornaCantidad(videoconductaresultados_list, inicio, fin, accion)
            if dato[5] == cantidad:
                totalfila += 1
        
            resultados.append(guarda_lista_resultados(idevaluacion, idvideo, inicio, fin, nombreFase, accion, cantidad, dato[9],fases_list,conductas_list))
    
    guardar_resultados(resultados)
            
    print(f'Total fila: {totalfila}')     

    return jsonify({"status": "success", "message": "Datos recibidos correctamente"})

@evaluacion_bp.route('/mostrar_resultados/<int:idevaluacion>')
def mostrar_resultados(idevaluacion):
    
    resultados = Resultados.query.filter_by(idevaluacion=idevaluacion).all()

    datos_resultados = [{key: value for key, value in resultado.__dict__.items() if not key.startswith('_')} for resultado in resultados]
    df_resultados = pd.DataFrame(datos_resultados)

    # Pivotamos la tabla para transponer los valores de 'idconducta'
    pivot_df_obtenido = df_resultados.pivot_table(
    index=['inicio', 'fin'],  # Agrupamos por inicio y fin (intervalos de tiempo)
    columns='idconducta',     # Transponemos la columna 'idconducta'
    values='obtenido',        # Usamos la columna 'obtenido' como valores
    aggfunc='sum',            # Sumamos en caso de haber valores duplicados
    fill_value=0              # Rellenamos los valores faltantes con 0
    )

    pivot_df_esperado = df_resultados.pivot_table(
    index=['inicio', 'fin'],  # Agrupamos por inicio y fin (intervalos de tiempo)
    columns='idconducta',     # Transponemos la columna 'idconducta'
    values='esperado',        # Usamos la columna 'esperado' como valores
    aggfunc='sum',            # Sumamos en caso de haber valores duplicados
    fill_value=0              # Rellenamos los valores faltantes con 0
    )

    # Unimos ambas tablas pivote, añadiendo un sufijo para diferenciar entre 'obtenido' y 'esperado'
    pivot_combined = pd.concat([pivot_df_obtenido, pivot_df_esperado], axis=1, keys=['obtenido', 'esperado'])
    pivot_combined.columns = ['_'.join(map(str, col)) for col in pivot_combined.columns]

    # Creamos la columna de comparación
    for conducta in df_resultados['idconducta'].unique():
        obtenido_col = f'obtenido_{conducta}'
        esperado_col = f'esperado_{conducta}'
        resultado_col = f'coincide_{conducta}'
        

    # Renombramos las columnas para que sean más claras
    # Las columnas con guion bajo son las que contienen los valores de 'esperado'
    pivot_combined.columns = ['Palanqueo', 'Levantamiento', 'Acercamiento', 'Entrega Pellet', 'Consumo Pellet','Palanqueo_', 'Levantamiento_', 'Acercamiento_', 'Entrega Pellet_', 'Consumo Pellet_']

    total_resultados = Resultados.query.filter(and_(Resultados.idevaluacion==idevaluacion, Resultados.fin<=899)).count()
    total_puntos_obtenidos = Resultados.query.filter(and_(Resultados.idevaluacion==idevaluacion, Resultados.fin<=899, Resultados.esperado == Resultados.obtenido )).count()

    print(f'Total resultados: {total_resultados} - Total puntos obtenidos: {total_puntos_obtenidos}')

    score = (total_puntos_obtenidos/total_resultados)*100

    # Convertir el DataFrame a una lista de listas
    pivot_combined=pivot_combined.reset_index()
    matriz_lista = pivot_combined.values.tolist()
    

    return render_template('evaluacion/resultados.html', matriz_lista=matriz_lista,enumerate=enumerate, score=score, usuario=current_user)



#Busca en la vista la cantidad de conductas
def retornaCantidad(videoconductaresultados_list, inicio, fin, accion):
    for vcr in videoconductaresultados_list:                
        if vcr.inicio == int(inicio) and vcr.fin == int(fin) and vcr.nombre == accion:                
            return vcr.cantidad
    return 0   

#Devuelve id de la fase
def retornaIdFase(nombre, fases_list):
    for fases in fases_list:
        if fases.nombre == nombre:
            return fases.id
    

#Devuelve id de la conducta
def retornaIdConducta(nombre,conductas_list):
    for conductas in conductas_list:
        if conductas.nombre == nombre:
            return conductas.id

def guarda_lista_resultados(idevaluacion, idvideo, inicio, fin, nombreFase, nombreConducta, esperado, obtenido,fases_list,conductas_list):
    resultados = {
        'idevaluacion': idevaluacion,
        'idvideo': idvideo,
        'inicio': 0,
        'fin': 0,        
        'idfase': 0,
        'idconducta': 0,
        'puntuacion': 0,
        'esperado': 0,
        'obtenido': 0
    }

    resultados['inicio'] = inicio
    resultados['fin'] = fin    
    #Ajustar para todas las fases
    resultados['idfase'] = retornaIdFase(nombreFase,fases_list)
    resultados['idconducta'] = retornaIdConducta(nombreConducta,conductas_list)
    resultados['puntuacion'] = 50 if esperado == obtenido else 0
    resultados['esperado'] = esperado
    resultados['obtenido'] = obtenido
    
    return resultados

#Gaurda resultados de la evaluación
def guardar_resultados(resultados):
    # Inserción masiva
    db.session.bulk_insert_mappings(Resultados, resultados)
    db.session.commit()

#---------------------------------------------------
def calcular_porcentajes(idevaluacion):
    # Consulta los resultados de la evaluación específica
    resultados = Resultados.query.filter_by(idevaluacion=idevaluacion).all()

    # Obtener el id del video de la evaluación
    idvideo = Resultados.query.filter_by(idevaluacion=idevaluacion).first().idvideo

    # Obtener las conductas asociadas al video
    video_conductas = VideosConductas.query.filter_by(idvideo=idvideo).all()
    id_fase_conducta_list = [vc.idfaseconducta for vc in video_conductas]

    fase_conductas = FasesConductasView.query.filter(FasesConductasView.id.in_(id_fase_conducta_list)).all()
    fase_conductas_list = [fc.idconducta for fc in fase_conductas]

    # Obtener los nombres de las conductas en un diccionario (ej. {1: 'Palanqueo', 2: 'Levantamiento', ...})
    conductas_dict = {conducta.id: conducta.nombre for conducta in Conductas.query.filter(Conductas.id.in_(fase_conductas_list)).all()}

    print(conductas_dict)
    print('-------------------')
    # Contadores para los cálculos
    total_obtenido = 0
    total_esperado = 0
    aciertos_por_conducta = {}
    total_por_conducta = {}

    # Calcular el total de aciertos por conducta y el total general
    for resultado in resultados:
        conducta_id = resultado.idconducta
        nombre_conducta = conductas_dict.get(conducta_id, f"Conducta {conducta_id}")
        obtenido = resultado.obtenido or 0
        esperado = resultado.esperado or 0

        # Sumar al total obtenido y esperado
        
        total_esperado += 1

        # Calcular aciertos y totales por cada conducta
        if nombre_conducta not in aciertos_por_conducta:
            aciertos_por_conducta[nombre_conducta] = 0
            total_por_conducta[nombre_conducta] = 0

        if obtenido == esperado:
            aciertos_por_conducta[nombre_conducta] += 1
            total_obtenido += 1

        total_por_conducta[nombre_conducta] += 1

    # Calcular porcentajes por conducta
    porcentaje_por_conducta = {
        nombre_conducta: (aciertos_por_conducta[nombre_conducta] / total_por_conducta[nombre_conducta]) * 100
        for nombre_conducta in aciertos_por_conducta
    }

    # Calcular el porcentaje total de acierto en la evaluación
    porcentaje_total = (total_obtenido / total_esperado) * 100 if total_esperado > 0 else 0

    # Determinar el resultado final de la competencia
    logro_competencia = porcentaje_total >= 80
    conductas_fallidas = [
        nombre_conducta for nombre_conducta, porcentaje in porcentaje_por_conducta.items() if porcentaje < 80
    ]

    # Actualizar el campo 'resultado' en la tabla Evaluaciones con el porcentaje_total
    evaluacion = Evaluaciones.query.filter_by(id=idevaluacion).first()
    if evaluacion:
        evaluacion.resultado = porcentaje_total
        db.session.commit()

    
    return porcentaje_por_conducta, porcentaje_total, logro_competencia, conductas_fallidas

# Ruta para mostrar los resultados
@evaluacion_bp.route('/resultado/<int:idevaluacion>')
@login_required
def mostrar_resultado(idevaluacion):
    porcentaje_por_conducta, porcentaje_total, logro_competencia, conductas_fallidas = calcular_porcentajes(idevaluacion)

    return render_template(
        'evaluacion/resultado.html',
        porcentaje_por_conducta=porcentaje_por_conducta,
        porcentaje_total=porcentaje_total,
        logro_competencia=logro_competencia,
        conductas_fallidas=conductas_fallidas,
        usuario=current_user
    )