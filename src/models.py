from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Operatori(db.Model):
    id = db.Column(db.String(5), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    data_assunzione = db.Column(db.Date)

    def __repr__(self):
        return f"<Operatore id: {self.id}>"
    
class Clienti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    settore = db.Column(db.String(100), nullable=False)
    regione = db.Column(db.String(100), nullable=False)
    indirizzo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(100), nullable=False)
    nome_utente = db.Column(db.String(100), nullable=False)
    richieste = db.Column(db.Integer)

    def __repr__(self):
            return f"<Cliente {self.id}>"
    
class Richieste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clienti.id', ondelete="CASCADE"))
    tipologia = db.Column(db.String(100), nullable=False)
    titolo = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.String(200), nullable=False)
    data_richiesta = db.Column(db.Date)
    id_operatore = db.Column(db.String(5))
    stato_lavoro = db.Column(db.String(20))
    data_chiusura = db.Column(db.Date)

    def __repr__(self):
        return f"<Ticket id: {self.id}>"