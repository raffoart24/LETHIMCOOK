from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Crea l'istanza dell'app Flask
app = Flask(__name__)

# Configura il percorso del database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabilita il tracking delle modifiche (opzionale)

# Inizializza SQLAlchemy
db = SQLAlchemy(app)

# Funzione per creare l'app
def create_app():
    # Qui puoi registrare altre configurazioni o blueprint se necessario
    from app.routes import bp  # Importa il blueprint delle rotte
    app.register_blueprint(bp)  # Registra il blueprint

    # Crea tutte le tabelle definite nei modelli
    with app.app_context():
        db.create_all()

    return app
