# ratbehavior
Este repositorio contiene la información necesaria para la instalación y ejecución de la aplicación ratbehavior

RatBehavior es una aplicación web desarrollada en Python con el framework Flask, diseñada para apoyar la enseñanza del análisis conductual en entornos académicos. El sistema permite a los estudiantes observar videos de laboratorio y registrar conductas en tiempo real para obtener una calificación automatizada.

🚀 Requisitos Previos
Antes de la instalación, asegúrate de contar con el siguiente software:

Python 3.10 o superior.
XAMPP (con el módulo MySQL/MariaDB activo).
Navegador Web actualizado (Chrome, Edge o Firefox).

🛠️ Instalación y Configuración
Sigue estos pasos para poner en marcha el proyecto en tu entorno local:

1. Preparación de la Base de Datos (MySQL)
Abre el panel de control de XAMPP e inicia el servicio de MySQL.
Accede a phpMyAdmin y crea una base de datos nueva llamada ratbehavior.
Importa y ejecuta los scripts SQL en el siguiente orden estricto:
sql_scripts/20251119_ratbahavior.sql: Crea la estructura base y tablas del sistema.
sql_scripts/20251119_actualizacion_vistas.sql: Actualiza las vistas necesarias para el funcionamiento correcto.

2. Configuración del Código
Clona este repositorio o descarga la carpeta del proyecto.
Instala las librerías necesarias ejecutando en tu terminal:

pip install -r requirements.txt
Verifica la conexión en el archivo config.py.

3. Ejecución
Inicia el servidor con el siguiente comando:

python app.py
Accede desde tu navegador a: http://127.0.0.1:5000.


🏗️ Arquitectura del Sistema
El proyecto sigue un patrón de diseño estructurado en capas:

Backend: Python 3.13.7 con Flask y SQLAlchemy (ORM).
Frontend: HTML5, Jinja2 y Bootstrap 5 para un diseño responsivo.
Persistencia: MySQL gestionado a través de XAMPP.

👥 Roles de Usuario

Estudiante: Puede seleccionar laboratorios, observar videos y registrar conductas.
Administrador: Gestión total de usuarios, videos, conductas y consulta de evaluaciones.
