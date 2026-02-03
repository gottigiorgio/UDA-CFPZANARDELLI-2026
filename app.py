from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from src.models import db, Operatori, Clienti, Richieste
from datetime import date
app = Flask(__name__)
import os

from src.routes.richieste import ticketRoute
from src.routes.clienti import clientiRoute
from src.routes.operatori import operatoriRoute


# Configura la connessione a PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgre@localhost/GestioneTicket'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabilita il tracking delle modifiche per ottimizzare le performance
app.secret_key = os.urandom(24) 

db.init_app(app)

app.register_blueprint(ticketRoute, url_prefix="/tickets")
app.register_blueprint(clientiRoute, url_prefix="/clienti")
app.register_blueprint(operatoriRoute, url_prefix="/operatori")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/caparezza")
def huh():
    return render_template("capacapacapa.html")

if __name__ == '__main__':
    app.run(debug=True)