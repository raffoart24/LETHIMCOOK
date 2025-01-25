from flask import Blueprint, jsonify, request
from app.models import Ricetta, PianoSettimanale
from app import db

bp = Blueprint('routes', __name__)


import random

@bp.route('/genera_piano', methods=['POST'])
def genera_piano():
    data = request.get_json()
    categoria = data.get('categoria')  # Es. "vegano", "vegetariano"

    if not categoria:
        return jsonify({'message': 'La categoria è obbligatoria!'}), 400

    # Seleziona ricette dalla categoria
    ricette = Ricetta.query.filter_by(categoria=categoria).all()
    if not ricette:
        return jsonify({'message': f'Nessuna ricetta trovata per la categoria "{categoria}".'}), 404

    giorni = ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato", "Domenica"]
    pasti = ["Colazione", "Pranzo", "Spuntino", "Cena"]

    # Controlla che ci siano abbastanza ricette
    if len(ricette) < len(giorni) * len(pasti):
        return jsonify({'message': 'Non ci sono abbastanza ricette disponibili per completare il piano.'}), 400

    # Mescola le ricette casualmente
    random.shuffle(ricette)

    # Genera il piano settimanale
    piano = []
    index = 0
    for giorno in giorni:
        for pasto in pasti:
            ricetta = ricette[index]  # Prendi la ricetta successiva
            piano.append(PianoSettimanale(giorno=giorno, pasto=pasto, ricetta_id=ricetta.id))
            index += 1  # Passa alla prossima ricetta

    # Salva il piano settimanale nel database
    db.session.bulk_save_objects(piano)
    db.session.commit()

    return jsonify({'message': 'Piano settimanale generato con successo!'}), 200




@bp.route('/get_piano', methods=['GET'])
def get_piano():
    piano = PianoSettimanale.query.all()
    return jsonify([p.to_dict() for p in piano]), 200






@bp.route('/get_ricette', methods=['GET'])
def get_ricette():
    ricette = Ricetta.query.all()
    return jsonify([r.to_dict() for r in ricette]), 200









@bp.route('/delete_piano/<int:id>', methods=['DELETE'])
def delete_piano(id):
    # Trova il piano settimanale con l'ID specificato
    piano = PianoSettimanale.query.get(id)

    if not piano:
        return jsonify({'message': f'Piano settimanale con ID {id} non trovato!'}), 404
    
    # Elimina il piano dal database
    db.session.delete(piano)
    db.session.commit()

    return jsonify({'message': f'Piano settimanale con ID {id} eliminato con successo!'}), 200











@bp.route('/update_piano/<int:id>', methods=['PATCH'])
def update_piano(id):
    # Recupera i dati dal corpo della richiesta
    data = request.get_json()
    
    # Trova il piano settimanale con l'ID specificato
    piano = PianoSettimanale.query.get(id)

    if not piano:
        return jsonify({'message': f'Piano settimanale con ID {id} non trovato!'}), 404
    
    # Verifica se sono presenti i dati da aggiornare
    if 'giorno' in data:
        piano.giorno = data['giorno']
    if 'pasto' in data:
        piano.pasto = data['pasto']
    if 'ricetta_id' in data:
        ricetta = Ricetta.query.get(data['ricetta_id'])
        if not ricetta:
            return jsonify({'message': 'Ricetta non trovata!'}), 404
        piano.ricetta_id = ricetta.id

    # Salva i cambiamenti
    db.session.commit()

    return jsonify({'message': f'Piano settimanale con ID {id} aggiornato con successo!'}), 200

