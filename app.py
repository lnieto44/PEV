from flask import Flask, jsonify, render_template, redirect, session, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Definición del modelo de Usuario
class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")


# Cargar usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, password, role_id FROM usuarios WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['role_id'] = user[2]

            # Registrar el inicio de sesión en la tabla logs
            log_action(user_id=user[0], action="login", details="El usuario inició sesión")

            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard' if session['role_id'] == 1 else 'denuncia_form'))
        else:
            flash('Credenciales incorrectas', 'danger')
    
    return render_template('Usuarios/login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        # Registrar el cierre de sesión en la tabla logs
        log_action(user_id=user_id, action="logout", details="El usuario cerró sesión")
        
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        tipo_documento = request.form.get('tipo_documento')
        cedula = request.form.get('cedula')
        primer_nombre = request.form.get('primer_nombre')
        segundo_nombre = request.form.get('segundo_nombre')
        primer_apellido = request.form.get('primer_apellido')
        segundo_apellido = request.form.get('segundo_apellido')
        edad = request.form.get('edad')

        # Encriptar la contraseña para seguridad
        hashed_password = generate_password_hash(password)

        # Definir el role_id para el usuario (ejemplo: 2 para usuarios regulares)
        role_id = 2  # Suponiendo que 2 es el ID para el rol 'user' en la tabla roles

        # Insertar el nuevo usuario en la base de datos
        try:
            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (username, password, email, tipo_documento, cedula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, edad, role_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (username, hashed_password, email, tipo_documento, cedula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, edad, role_id))
            conn.commit()
            conn.close()

            flash('Usuario registrado exitosamente!', 'success')
            return redirect(url_for('register'))
        except sqlite3.Error as e:
            flash(f'Error al registrar el usuario: {e}', 'danger')
            return redirect(url_for('register'))

    return render_template('Usuarios/register.html')


# Vista de dashboard para administradores
@app.route('/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Acceso denegado. Solo los administradores pueden ver esta página.')
        return redirect(url_for('user_page'))
    
    # Conectar a la base de datos y obtener datos para la vista
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Obtener el total de denuncias
    total_denuncias = cursor.execute('SELECT COUNT(*) FROM denuncias').fetchone()[0]
    
    # Obtener el total de usuarios
    total_usuarios = cursor.execute('SELECT COUNT(*) FROM usuarios').fetchone()[0]

    # Obtener el número de denuncias activas
    casos_activos = cursor.execute('SELECT COUNT(*) FROM denuncias WHERE estado = "activo"').fetchone()[0]

    # Obtener denuncias mensuales (ejemplo de datos para 5 meses)
    labels_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo"]
    datos_mensuales = []
    for mes in range(1, 6):  # Enero = 1, Mayo = 5 (por ejemplo)
        count = cursor.execute('SELECT COUNT(*) FROM denuncias WHERE strftime("%m", fecha_creacion) = ?', 
                               (f"{mes:02d}",)).fetchone()[0]
        datos_mensuales.append(count)
    
    # Obtener la distribución de tipos de denuncias
    labels_tipos = ["Física", "Psicológica", "Sexual", "Económica"]
    datos_tipos = []
    for tipo in labels_tipos:
        count = cursor.execute('SELECT COUNT(*) FROM denuncias WHERE tipo = ?', (tipo,)).fetchone()[0]
        datos_tipos.append(count)
    
    # Obtener la distribución de estados de denuncias
    labels_estados = ["Activo", "En Proceso", "Cerrado"]
    datos_estados = []
    for estado in labels_estados:
        count = cursor.execute('SELECT COUNT(*) FROM denuncias WHERE estado = ?', (estado,)).fetchone()[0]
        datos_estados.append(count)

    conn.close()

    return render_template('dashboard.html', 
                           total_denuncias=total_denuncias, 
                           casos_activos=casos_activos,
                           total_usuarios=total_usuarios,
                           labels_meses=labels_meses,
                           datos_mensuales=datos_mensuales,
                           labels_tipos=labels_tipos,
                           datos_tipos=datos_tipos,
                           labels_estados=labels_estados,
                           datos_estados=datos_estados)


# Página de usuario

# Ruta para mostrar el formulario de denuncia 
@app.route('/denuncia', methods=['GET'])
def denuncia_form():
    return render_template('Usuarios/denuncia.html')

# Ruta para procesar el formulario de denuncia
@app.route('/submit_denuncia', methods=['POST'])
def submit_denuncia():
    # Obtener datos del formulario
    description = request.form['description']
    incident_type = request.form['incident_type']
    location = request.form['location']
    nombre = request.form.get('nombre')  # Campo opcional
    telefono = request.form.get('telefono')  # Campo opcional
    email = request.form.get('email')  # Campo opcional

    # Conectar a la base de datos y guardar la denuncia
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO denuncias (description, incident_type, location, nombre, telefono, email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (description, incident_type, location, nombre, telefono, email))
    conn.commit()
    
    # Registrar la creación de la denuncia en logs
    user_id = session.get('user_id')  # Obtén el ID del usuario de la sesión
    if user_id:
        log_action(user_id=user_id, action="crear_denuncia", details=f"Descripción: {description}")

    conn.close()

    flash('Denuncia enviada exitosamente', 'success')
    return redirect(url_for('denuncia_form'))

# Módulo de geolocalización

# Ruta para "centros_ayuda" (ubicada en Usuarios/centros_ayuda.html)
@app.route('/')
def centros_ayuda():
    return render_template('Usuarios/centros_ayuda.html')

# Ruta para "centro_ayuda" (ubicada en Administrador/centro_ayuda.html)
@app.route('/centro_ayuda')
def centro_ayuda():
    return render_template('Administrador/centro_ayuda.html')


@app.route('/get_help_centers', methods=['GET'])
def get_help_centers():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, address, latitude, longitude FROM centros_ayuda")
    centers = cursor.fetchall()
    conn.close()

    centers_data = [
        {"id": center[0], "name": center[1], "address": center[2], "latitude": center[3], "longitude": center[4]}
        for center in centers
    ]

    # Registrar en logs que los centros de ayuda fueron solicitados
    user_id = session.get('user_id')  # Obtiene el ID del usuario de la sesión
    if user_id:
        log_action(user_id=user_id, action="obtener_centros_ayuda", details="Lista de centros de ayuda solicitada")

    return jsonify(centers_data)

@app.route('/sync_help_center', methods=['POST'])
def sync_help_center():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Conectar a la base de datos y agregar/actualizar el centro de ayuda
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO centros_ayuda (name, address, latitude, longitude)
        VALUES (?, ?, ?, ?)
    """, (name, address, latitude, longitude))
    conn.commit()
    conn.close()

    # Registrar en logs que se ha sincronizado un centro de ayuda
    user_id = session.get('user_id')  # Obtiene el ID del usuario de la sesión
    if user_id:
        log_action(user_id=user_id, action="sync_help_center", details=f"Centro de ayuda sincronizado: {name}")

    return jsonify({"status": "success"})


# Gestión de roles para administradores
@app.route('/administrar_roles', methods=['GET', 'POST'])
@login_required
def manage_roles():
    if current_user.role != 'admin':
        flash('Acceso denegado.')
        return redirect(url_for('user_page'))
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_role = request.form.get('role')
        user = User.query.get(user_id)
        if user:
            user.role = new_role
            db.session.commit()
            flash('Rol actualizado con éxito.')
        else:
            flash('Usuario no encontrado.')
    users = User.query.all()
    return render_template('Administrador/administrar_roles.html', users=users)

#log llevar la traza de los registros de los eventos de la platafoma
def log_action(user_id, action, details=None):
    """Registra una acción del usuario en la tabla logs."""
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (user_id, action, details)
        VALUES (?, ?, ?)
    """, (user_id, action, details))
    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('Usuarios/home.html')

@app.route('/quienes_somos')
def quienes_somos():
    return render_template('Usuarios/quienes_somos.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']
        # Aquí puedes manejar el mensaje, como almacenarlo en una base de datos o enviarlo por correo
        flash("Tu mensaje ha sido enviado. Nos pondremos en contacto contigo pronto.", "success")
        return redirect(url_for('contacto'))
    return render_template('Usuarios/contacto.html')

@app.route('/api/centros_ayuda')
def api_centros_ayuda():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, address, latitude, longitude FROM centros_ayuda")
    centros = cursor.fetchall()
    conn.close()

    centros_data = [
        {"id": centro[0], "name": centro[1], "address": centro[2], "latitude": centro[3], "longitude": centro[4]}
        for centro in centros
    ]
    return jsonify(centros_data)


@app.route('/caracteristicas')
def caracteristicas():
    return render_template('Usuarios/sobre-mi.html')  # Página de características

@app.route('/servicios')
def servicios():
    return render_template('Usuarios/servicios.html')  # Página de servicios


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear tablas si no existen en la base de datos
    app.run(debug=True)


