from flask import Flask, render_template, redirect, session, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Inicializar Socket.IO
socketio = SocketIO(app)

# Modelo de usuario
class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # Roles: 'admin', 'user'

# Modelo para registrar acciones (logs)
class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text, nullable=True)

# Cargar usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Función para registrar acciones
def log_action(user_id, action, details=None):
    log = Log(user_id=user_id, action=action, details=details)
    db.session.add(log)
    db.session.commit()

# Ruta principal
@app.route('/')
def home():
    return render_template('Usuarios/home.html')

# Rutas principales de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            log_action(user.id, 'login', 'Usuario inició sesión')
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard' if user.role == 'admin' else 'user_page'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('Usuarios/login.html')

@app.route('/logout')
def logout():
    log_action(current_user.id, 'logout', 'Usuario cerró sesión')
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está registrado', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('login'))

    return render_template('Usuarios/register.html')

# Rutas específicas para usuarios y administradores
@app.route('/dashboard')
def dashboard():
    if current_user.role != 'admin':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('user_page'))

    total_users = User.query.count()
    logs = Log.query.order_by(Log.id.desc()).limit(10).all()
    return render_template('Administrador/dashboard.html', total_users=total_users, logs=logs)

@app.route('/user_page')
def user_page():
    return render_template('Usuarios/user_page.html')

# Ruta para el chat flotante
@app.route('/chat')

def chat_page():
    return render_template('Usuarios/principal.html')

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

# Funciones del Chat
@socketio.on('chatMessage')
def handle_chat_message(data):
    user_message = data.get('message', '')
    bot_response = generate_bot_response(user_message)
    emit('message', {'user': 'PEV', 'message': bot_response}, broadcast=True)

def generate_bot_response(user_message):
    if "hola" in user_message.lower():
        return "¡Hola! ¿Cómo puedo ayudarte hoy?"
    elif "ayuda" in user_message.lower():
        return "¡Claro! Estoy aquí para ayudarte."
    else:
        return "No entendí tu mensaje. ¿Puedes intentarlo de nuevo?"

# Módulos de geolocalización
@app.route('/centros_ayuda', methods=['GET'])
def centros_ayuda():
    return render_template('Usuarios/centros_ayuda.html')

@app.route('/api/centros_ayuda', methods=['GET'])
def api_centros_ayuda():
    # Simulación de datos para centros de ayuda
    centros = [
        {"id": 1, "name": "Centro 1", "address": "Dirección 1", "latitude": 4.123, "longitude": -74.123},
        {"id": 2, "name": "Centro 2", "address": "Dirección 2", "latitude": 4.234, "longitude": -74.234},
    ]
    return jsonify(centros)

# Rutas informativas
@app.route('/quienes_somos')
def quienes_somos():
    return render_template('Usuarios/quienes_somos.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']
        flash("Tu mensaje ha sido enviado. Nos pondremos en contacto contigo pronto.", "success")
        return redirect(url_for('contacto'))
    return render_template('Usuarios/contacto.html')

@app.route('/caracteristicas')
def caracteristicas():
    return render_template('Usuarios/sobre-mi.html')

@app.route('/servicios')
def servicios():
    return render_template('Usuarios/servicios.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Verificar si el correo existe en la base de datos
        token = serializer.dumps(email, salt='password-reset')
        link = url_for('reset_password', token=token, _external=True)
        msg = Message("Restablecimiento de Contraseña", sender="your_email@example.com", recipients=[email])
        msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {link}'
        mail.send(msg)
        flash("Se ha enviado un enlace de recuperación a tu correo", "info")
    return render_template('Usuarios/forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)  # 1 hora de validez
    except:
        flash("El enlace de restablecimiento ha expirado o es inválido", "danger")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_password = request.form['new_password']
        # Actualizar la contraseña en la base de datos
        flash("Tu contraseña ha sido restablecida", "success")
        return redirect(url_for('login'))
    
    return render_template('Usuarios/reset_password.html', token=token)

# Inicialización manual de tablas
if __name__ == '__main__':
    app.app_context().push()  # Crear un contexto explícito para la aplicación
    db.create_all()  # Crear tablas en la base de datos si no existen
    socketio.run(app, debug=True)

