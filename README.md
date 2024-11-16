# PEV
Pasos de Plataforma de Prevención y Erradicación de la Violencia 

1. Descargar Git

Ir a la página oficial de Git: https://git-scm.com/.
Descargar e instalar Git según el sistema operativo (Windows, macOS o Linux).
Durante la instalación en Windows, selecciona la opción "Git Bash Here" para facilitar el uso de Git.
Configurar Git después de instalarlo
Abrir Git Bash (o la terminal si usas Linux/macOS).

#Configurar el nombre y el correo:

git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo@ejemplo.com"

2. Descargar Visual Studio Code

Ir a la página oficial de Visual Studio Code: https://code.visualstudio.com/.
Descargar e instalar Visual Studio Code según el sistema operativo.

3. Crear una Cuenta en GitHub

Ir a https://github.com/ y registrarse con su correo electrónico.
Verificar el correo electrónico para activar la cuenta.

4. Abre Visual Studio Code

Inicia Visual Studio Code.

Ve al menú View > Command Palette o usa el atajo Ctrl+Shift+P (Windows/Linux) o Cmd+Shift+P (macOS).
Escribe Git: Clone y selecciona la opción.

5. Pegar la URL del Repositorio
   
Pega la URL del repositorio que copiaste antes.
https://github.com/lnieto44/PEV.git

Visual Studio Code te pedirá que selecciones una carpeta local donde clonar el repositorio.

6. Verifica que se clonó correctamente
Una vez clonado:

VS Code abrirá automáticamente la carpeta del proyecto.
Deberías ver los archivos del repositorio en el panel izquierdo.
En la barra inferior de VS Code, debería mostrarse la rama actual, por ejemplo: main.

7. Comprueba el Estado del Repositorio
   
Abre la terminal integrada (Ctrl+``) o usa el menú View > Terminal`.
Escribe:

git status

Esto mostrará si el repositorio se clonó correctamente y si hay cambios pendientes.

8. instalacion de todos los paquetes requeridos: Flask, Flask-SQLAlchemy, Flask-Login y Werkzeug en la terminal de visual code

pip install flask flask-sqlalchemy flask-login werkzeug

Nota: si no funciona pip 

python -m ensurepip --upgrade

python -m ensurepip

python -m pip install --upgrade pip

pip --version

9. Intalar paquete para el chat
    pip install flask-socketio

10. ejecutar la app

python app.py

