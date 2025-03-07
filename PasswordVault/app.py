import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
from crypto_utils import encrypt_password, decrypt_password

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")  # For development
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///passwords.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

db.init_app(app)

# Import models after db initialization
from models import User, Password

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login primeiro.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def check_session_timeout():
    if 'user_id' in session:
        if 'last_activity' in session:
            last_activity = datetime.fromisoformat(session['last_activity'])
            if datetime.utcnow() - last_activity > timedelta(minutes=30):
                session.clear()
                flash('Sessão expirada. Por favor, faça login novamente.', 'warning')
                return redirect(url_for('login'))
        session['last_activity'] = datetime.utcnow().isoformat()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.first():
            flash('Apenas uma conta de usuário é permitida.', 'danger')
            return redirect(url_for('login'))

        master_password = request.form.get('master_password')
        confirm_password = request.form.get('confirm_password')

        if master_password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(master_password)
        new_user = User(master_hash=password_hash, created_at=datetime.utcnow())

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registro realizado com sucesso! Por favor, faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Falha no registro!', 'danger')
            logging.error(f"Erro no registro: {str(e)}")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        master_password = request.form.get('master_password')
        user = User.query.first()

        if user and check_password_hash(user.master_hash, master_password):
            session['user_id'] = user.id
            session.permanent = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Senha mestra inválida!', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        passwords = Password.query.all()
        decrypted_passwords = []

        for pwd in passwords:
            try:
                decrypted_password = {
                    'id': pwd.id,
                    'title': pwd.title,
                    'username': pwd.username,
                    'url': pwd.url,
                    'password': decrypt_password(pwd.password_enc),
                    'created_at': pwd.created_at
                }
                decrypted_passwords.append(decrypted_password)
            except Exception as e:
                logging.error(f"Erro ao descriptografar senha: {str(e)}")
                # Remove a senha que não pode ser descriptografada
                db.session.delete(pwd)

        if db.session.dirty:
            db.session.commit()
            flash('Algumas senhas antigas foram removidas por problemas de compatibilidade.', 'warning')

        return render_template('dashboard.html', passwords=decrypted_passwords)
    except Exception as e:
        logging.error(f"Erro no dashboard: {str(e)}")
        flash('Ocorreu um erro ao carregar suas senhas. Por favor, tente novamente.', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/add_password', methods=['POST'])
@login_required
def add_password():
    try:
        title = request.form.get('title')
        username = request.form.get('username')
        url = request.form.get('url')
        password = request.form.get('password')

        if not all([title, username, password]):
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return redirect(url_for('dashboard'))

        encrypted_password = encrypt_password(password)
        new_password = Password(
            title=title,
            username=username,
            url=url,
            password_enc=encrypted_password,
            created_at=datetime.utcnow()
        )

        db.session.add(new_password)
        db.session.commit()
        flash('Senha adicionada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao adicionar senha: {str(e)}")
        flash('Falha ao adicionar senha. Por favor, tente novamente.', 'danger')

    return redirect(url_for('dashboard'))

@app.route('/delete_password/<int:id>', methods=['POST'])
@login_required
def delete_password(id):
    try:
        password = Password.query.get_or_404(id)
        db.session.delete(password)
        db.session.commit()
        flash('Senha excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Falha ao excluir senha!', 'danger')
        logging.error(f"Erro ao excluir senha: {str(e)}")

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

with app.app_context():
    # Remove o banco de dados existente para garantir compatibilidade
    import os
    if os.path.exists("instance/passwords.db"):
        os.remove("instance/passwords.db")
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)