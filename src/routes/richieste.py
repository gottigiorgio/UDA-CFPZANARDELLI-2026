from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from src.models import db, Operatori, Clienti, Richieste
from datetime import date

ticketRoute = Blueprint('richieste', __name__)

@ticketRoute.route("/list")
def listTicket():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Richieste.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return render_template("ticket/list.html", tickets=pagination.items, pagination=pagination)

@ticketRoute.route("/new", methods=["GET", "POST"])
def addTicket():
    tipologie=[
        'Accessi',
        'Stampante',
        'Hardware',
        'Software',
        'Rete'
    ]

    if request.method == 'POST':
        titolo = request.form['titolo']
        tipo = request.form['tipologia']
        descrizione = request.form['descrizione']
        data_richiesta = date.today().strftime("%d/%m/%Y")
        stato_lavoro = 'Aperto'
        id_operatore = None
        data_chiusura = None
        new_ticket = Richieste(titolo, tipo, descrizione, data_richiesta, stato_lavoro, id_operatore, data_chiusura)
        db.session.add(new_ticket)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('ticket/new.html', tipologie=tipologie)

@ticketRoute.route("/<string:ticket_id>/edit", methods=["GET", "POST"])
def editTicket(ticket_id):

    # Recupero ticket
    ticket = Richieste.query.get_or_404(ticket_id)

    stati = ['Aperto', 'In lavorazione', 'Chiuso']
    operatori = Operatori.query.all()

    if request.method == 'POST':
        ticket.titolo = request.form['titolo']
        ticket.tipologia = request.form['tipologia']
        ticket.descrizione = request.form['descrizione']
        ticket.stato_laboro = request.form['stato_laboro']
        id_operatore = request.form.get('id_operatore')
        ticket.id_operatore = id_operatore if id_operatore else None

        # Se chiuso setto data chiusura
        if ticket.stato_laboro == 'Chiuso' and not ticket.data_chiusura:
            ticket.data_chiusura = date.today()
        elif ticket.stato_laboro != 'Chiuso':
            ticket.data_chiusura = None

        db.session.commit()
        return redirect(url_for('richieste.listTicket'))

    return render_template(
        'ticket/edit.html',
        ticket=ticket,
        stati=stati,
        operatori=operatori
    )

@ticketRoute.route("/<string:ticket_id>")
def viewTicket(ticket_id):
    ticket = Richieste.query.get_or_404(ticket_id)
    return render_template("ticket/view.html", ticket=ticket)
