from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from src.models import db, Operatori, Clienti, Richieste
from datetime import date

operatoriRoute = Blueprint('operatori', __name__)

@operatoriRoute.route("/list")
def listOperatori():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Operatori.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return render_template("operatori/list.html", operatori=pagination.items, pagination=pagination)


@operatoriRoute.route("/new", methods=["GET", "POST"])
def addOperatore():
    if request.method == "POST":
        operatore = Operatori(
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

        db.session.add(operatore)
        db.session.commit()
        return redirect(url_for("operatori.listOperatori"))

    return render_template("operatori/new.html")

@operatoriRoute.route("/<string:id>/edit", methods=["GET", "POST"])
def editOperatore(id):
    operatore = Operatori.query.get_or_404(id)

    if request.method == "POST":
        operatore.nome = request.form["nome"]
        operatore.cognome = request.form["cognome"]
        operatore.settore = request.form["settore"]
        operatore.regione = request.form["regione"]
        operatore.indirizzo = request.form["indirizzo"]
        operatore.email = request.form["email"]
        operatore.telefono = request.form["telefono"]
        operatore.nome_utente = request.form["nome_utente"]

        db.session.commit()
        return redirect(url_for("operatori.listOperatori"))

    return render_template("operatori/edit.html", operatore=operatore)

@operatoriRoute.route("/<string:id>")
def viewOperatore(id):
    operatore = Operatori.query.get_or_404(id)
    return render_template("operatori/view.html", operatore=operatore)

@operatoriRoute.route("/delete/<string:id>")
def deleteOperatore(id):
    operatore = Operatori.query.get_or_404(id)
    db.session.delete(operatore)
    db.session.commit()
    flash("Operatore eliminato con successo.", "success")
    return redirect(url_for("operatori.listOperatori"))
