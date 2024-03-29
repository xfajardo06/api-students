# Proyecto Sistema de Calificación de Notas de una Universidad

## Descripción
Este proyecto es una aplicación web desarrollada en Python con Flask y Flask-RestX para proporcionar una API de servicios. Utiliza JWT para la autenticación de usuarios.

## Instalación

### Requisitos previos
- Python 3.8 instalado en tu sistema.
- MongoDB 5.0.3

### Configuración del entorno virtual
1. Clona el repositorio desde GitHub:
git clone https://github.com/xfajardo06/api-students.git

2. Navega al directorio del proyecto:
cd api-students

3. Crea un entorno virtual:
python3.8 -m venv venv

4. Activa el entorno virtual:
- En Windows:
  ```
  venv\Scripts\activate
  ```
- En macOS/Linux:
  ```
  source venv/bin/activate
  ```

### Instalación de dependencias
Instala las dependencias del proyecto usando pip:
pip install -r requirements.txt


## Uso
1. Configura las variables de entorno necesarias, como la configuración de la base de datos y las claves secretas.

export ENV='development'
export DEV_MONGODB_URI='mongodb://localhost:27017/calificaciones'
export APP_SETTINGS="app.config.DevelopmentConfig"
export DEV_SECRET_KEY="ASDFGHJKL"

2. Comando para ejecutar la aplicación: python main.py
3. Ir al admin: '/admin/subject' para visualizar los datos de la base de datos cargados. Confirmar que se haya cargado los datos de Las Materías Base (Subjects)
4. Accede a la API desde tu navegador o herramienta de desarrollo de API (Postman).

## Documentación de la API
Documentación donde se describe cada endpoint disponible y los parametros necesarios https://documenter.getpostman.com/view/18745239/2sA2r3YR3E#intro

