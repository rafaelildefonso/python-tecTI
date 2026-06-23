# TODO: criar dashboard
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from models import Filme, Sala, Sessao, db

dashboard_bp = Blueprint("cinema", __name__, url_prefix="/cinema")


@dashboard_bp.route("/")
def index():
    sessoes = Sessao.listar_com_detalhes()
    return render_template("cinema/lista_sessoes.html", sessoes=sessoes)


@dashboard_bp.route("/sessao/cadastrar", methods=["GET", "POST"])
def cadastrar_sessao():
    filmes = Filme.listar()
    salas = Sala.listar()

    if request.method == "POST":
        try:
            filme_id = int(request.form.get("filme_id", 0))
            sala_id = int(request.form.get("sala_id", 0))
            data_hora = datetime.fromisoformat(request.form.get("data_hora", ""))
            preco = float(request.form.get("preco", "0"))
        except (ValueError, TypeError):
            return render_template(
                "cinema/formulario_sessao.html",
                filmes=filmes,
                salas=salas,
                erro="Dados inválidos. Verifique os campos e tente novamente.",
            )

        if not db.session.get(Filme, filme_id) or not db.session.get(Sala, sala_id):
            erro = "Filme ou sala inválida."
            return render_template(
                "cinema/formulario_sessao.html",
                filmes=filmes,
                salas=salas,
                erro=erro,
            )

        Sessao.salvar(filme_id, sala_id, data_hora, preco)
        return redirect(url_for("cinema.index"))

    return render_template(
        "cinema/formulario_sessao.html",
        filmes=filmes,
        salas=salas,
    )
