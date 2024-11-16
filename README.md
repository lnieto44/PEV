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

7.1 Descargar Python

Accede a la página oficial de Python:
Ve a https://www.python.org/downloads/.

Descarga la última versión estable:

Haz clic en el botón de descarga correspondiente a tu sistema operativo (Windows, macOS, Linux).

7.2. Instalar Python en Windows

Ejecuta el instalador descargado:

Haz doble clic en el archivo descargado para iniciar la instalación.
Marca la casilla "Add Python to PATH":

Esto es muy importante para que Python funcione desde la línea de comandos sin problemas.

Selecciona "Customize installation" (Opcional):

Asegúrate de que las opciones básicas (pip, IDLE, documentación) estén marcadas.
Si necesitas instalar Python para todos los usuarios, selecciona "Install for all users".
Instala Python:

Haz clic en "Install Now" o personaliza la instalación si tienes requisitos específicos.
Espera a que termine la instalación:

Una vez finalizada, selecciona la opción "Disable path length limit" si aparece.

7.3. Validar la instalación de Python
   
Abre una terminal o línea de comandos:

Presiona Win + R, escribe cmd y presiona Enter.

Verifica la versión de Python:

Escribe el siguiente comando y presiona Enter:

cmd

python --version

o

python3 --version

Verifica que pip esté instalado:

python -m pip --version

Si ves un mensaje con la versión de pip, significa que se instaló correctamente.

Prueba Python interactivo:

Escribe python en la terminal y presiona Enter para entrar al intérprete interactivo.

Escribe:

print("¡Python está funcionando correctamente!")

Deberías ver:

¡Python está funcionando correctamente!

Sal del intérprete escribiendo exit() y presionando Enter.

7.4. Configuración de variables de entorno (si es necesario)
   
Si Python o pip no funcionan, verifica que las rutas estén en el PATH:

Encuentra la carpeta de instalación de Python:

Generalmente está en:

C:\Users\<tu_usuario>\AppData\Local\Programs\Python\PythonXX\

Agrega las rutas a las variables de entorno:

La ruta de Python (por ejemplo: C:\PythonXX\).

La carpeta Scripts (por ejemplo: C:\PythonXX\Scripts\).

Sigue estos pasos:

Ve a Configuración del sistema > Configuración avanzada del sistema.

Haz clic en Variables de entorno.

Selecciona Path y haz clic en Editar.

Agrega las rutas mencionadas.

Reinicia la terminal:

Abre una nueva terminal y prueba nuevamente.

7.5. Instala un paquete de prueba

Para validar que pip funciona correctamente:

Instala un paquete de prueba:

python -m pip install requests

Si la instalación es exitosa, verifica:

cmd

python -m pip show requests


8. instalacion de todos los paquetes requeridos: Flask, Flask-SQLAlchemy, Flask-Login y Werkzeug en la terminal de visual code

pip install flask flask-sqlalchemy flask-login werkzeug

Nota: si no funciona pip 

python -m ensurepip --upgrade

python -m ensurepip

python -m pip install --upgrade pip

pip --version

9. Intalar paquete para el chat
    
    pip install flask-socketio

11. ejecutar la app

python app.py

