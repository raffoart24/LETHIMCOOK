from app import db

class Ricetta(db.Model):
    __tablename__ = 'ricette'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # Es. "vegano", "vegetariano", ecc.
    ingredienti = db.Column(db.Text, nullable=False)  # Lista di ingredienti separata da virgola

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'categoria': self.categoria,
            'ingredienti': self.ingredienti.split(', ')
        }

class PianoSettimanale(db.Model):
    __tablename__ = 'piano_settimanale'
    id = db.Column(db.Integer, primary_key=True)
    giorno = db.Column(db.String(20), nullable=False)  # Es. "Lunedì", "Martedì"
    pasto = db.Column(db.String(20), nullable=False)  # Es. "Colazione", "Pranzo"
    ricetta_id = db.Column(db.Integer, db.ForeignKey('ricette.id'), nullable=False)
    ricetta = db.relationship('Ricetta', backref='piani')

    def to_dict(self):
        return {
            'id': self.id,
            'giorno': self.giorno,
            'pasto': self.pasto,
            'ricetta': self.ricetta.to_dict()
        }
