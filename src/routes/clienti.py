from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from src.models import db, Operatori, Clienti, Richieste
from datetime import date

clientiRoute = Blueprint('clienti', __name__)

@clientiRoute.route("/list")
def listClienti():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Clienti.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return render_template("clienti/list.html", clienti=pagination.items, pagination=pagination)

@clientiRoute.route("/new", methods=["GET", "POST"])
def addCliente():
    if request.method == "POST":
        cliente = Clienti(
            nome=request.form["nome"],
            cognome=request.form["cognome"],
            settore=request.form["settore"],
            regione=request.form["regione"],
            indirizzo=request.form["indirizzo"],
            email=request.form["email"],
            telefono=request.form["telefono"],
            nome_utente=request.form["nome_utente"],
            richieste=0
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for("clienti.listClienti"))

    return render_template("clienti/new.html")

@clientiRoute.route("/edit/<int:id>", methods=["GET", "POST"])
def editCliente(id):
    cliente = Clienti.query.get_or_404(id)

    if request.method == "POST":
        cliente.nome = request.form["nome"]
        cliente.cognome = request.form["cognome"]
        cliente.settore = request.form["settore"]
        cliente.regione = request.form["regione"]
        cliente.indirizzo = request.form["indirizzo"]
        cliente.email = request.form["email"]
        cliente.telefono = request.form["telefono"]
        cliente.nome_utente = request.form["nome_utente"]

        db.session.commit()
        return redirect(url_for("clienti.listClienti"))

    return render_template("clienti/edit.html", cliente=cliente)

@clientiRoute.route("/view/<int:id>")
def viewCliente(id):
    cliente = Clienti.query.get_or_404(id)
    return render_template("clienti/view.html", cliente=cliente)

@clientiRoute.route("/delete/<int:id>")
def deleteCliente(id):
    cliente = Clienti.query.get_or_404(id)
    if cliente.richieste:  # Se ci sono richieste collegate
        flash("Impossibile eliminare il cliente: ci sono richieste associate.", "danger")
        return redirect(url_for("clienti.listClienti"))
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente eliminato con successo.", "success")
    return redirect(url_for("clienti.listClienti"))