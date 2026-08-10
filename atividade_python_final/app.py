import functools
import os
import re
from datetime import date

from flask import (
    Flask,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

import banco
from requisicoes_api import frase_motivacional

STATUS_INFO = {
    "pendente": {
        "rotulo": "Pendente",
        "classe": "status-pendente",
        "badge": "text-bg-warning",
    },
    "em andamento": {
        "rotulo": "Em andamento",
        "classe": "status-em-andamento",
        "badge": "text-bg-primary",
    },
    "concluida": {
        "rotulo": "Concluída",
        "classe": "status-concluida",
        "badge": "text-bg-success",
    },
}

PADRAO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def criar_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "chave-secreta")
    app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

    @app.before_request
    def carregar_usuario():
        g.usuario = None
        if "usuario_id" in session:
            g.usuario = banco.buscar_usuario_por_id(session["usuario_id"])

    @app.context_processor
    def injetar_contexto():
        return {"status_info": STATUS_INFO, "usuario": g.get("usuario")}

    return app


app = criar_app()
banco.criar_tabelas()


def login_obrigatorio(funcao):
    """Decorator: bloqueia o acesso de visitantes nao logados."""

    @functools.wraps(funcao)
    def protegida(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)

    return protegida


def validar_email(email):
    return bool(PADRAO_EMAIL.match(email)) and len(email) <= 100


def validar_titulo(titulo):
    return 0 < len(titulo) <= 120


def validar_descricao(descricao):
    return len(descricao) <= 500


@app.route("/")
def raiz():
    if "usuario_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if "usuario_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmacao", "")

        if not all([nome, email, senha, confirmacao]):
            flash("Preencha todos os campos.", "danger")
        elif len(nome) > 100:
            flash("O nome deve ter no máximo 100 caracteres.", "danger")
        elif not validar_email(email):
            flash("Informe um e-mail válido.", "danger")
        elif len(senha) < 4:
            flash("A senha deve ter pelo menos 4 caracteres.", "danger")
        elif senha != confirmacao:
            flash("As senhas não coincidem.", "danger")
        elif banco.buscar_usuario_por_email(email):
            flash("Este e-mail já está cadastrado.", "danger")
        else:
            banco.criar_usuario(nome, email, generate_password_hash(senha))
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = banco.buscar_usuario_por_email(email)

        if usuario and check_password_hash(usuario["senha"], senha):
            session.clear()
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            flash(f"Bem-vindo(a), {usuario['nome']}!", "success")
            return redirect(url_for("dashboard"))

        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_obrigatorio
def dashboard():
    usuario_id = session["usuario_id"]
    tarefas = banco.listar_tarefas(usuario_id)
    return render_template(
        "dashboard.html",
        tarefas=tarefas,
        frase=frase_motivacional(),
        hoje=date.today().strftime("%d/%m/%Y"),
    )


@app.route("/nova_tarefa", methods=["GET", "POST"])
@login_obrigatorio
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "pendente").strip()

        if not validar_titulo(titulo):
            flash("Informe um título com até 120 caracteres.", "danger")
        elif not validar_descricao(descricao):
            flash("A descrição deve ter no máximo 500 caracteres.", "danger")
        elif status not in STATUS_INFO:
            flash("Status inválido.", "danger")
        else:
            banco.criar_tarefa(titulo, descricao, status, session["usuario_id"])
            flash("Tarefa criada com sucesso!", "success")
            return redirect(url_for("dashboard"))

    return render_template("nova_tarefa.html")


@app.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
@login_obrigatorio
def editar_tarefa(tarefa_id):
    tarefa = banco.buscar_tarefa_por_id(tarefa_id, session["usuario_id"])
    if not tarefa:
        flash("Tarefa não encontrada.", "warning")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", tarefa["status"]).strip()

        if not validar_titulo(titulo):
            flash("Informe um título com até 120 caracteres.", "danger")
        elif not validar_descricao(descricao):
            flash("A descrição deve ter no máximo 500 caracteres.", "danger")
        elif status not in STATUS_INFO:
            flash("Status inválido.", "danger")
        else:
            banco.atualizar_tarefa(
                tarefa_id,
                session["usuario_id"],
                titulo=titulo,
                descricao=descricao,
                status=status,
            )
            flash("Tarefa atualizada com sucesso!", "success")
            return redirect(url_for("dashboard"))

    return render_template("editar_tarefa.html", tarefa=tarefa)


@app.route("/excluir/<int:tarefa_id>", methods=["POST"])
@login_obrigatorio
def excluir_tarefa(tarefa_id):
    if banco.excluir_tarefa(tarefa_id, session["usuario_id"]):
        flash("Tarefa excluída.", "success")
    else:
        flash("Tarefa não encontrada.", "warning")
    return redirect(url_for("dashboard"))


@app.route("/concluir/<int:tarefa_id>", methods=["POST"])
@login_obrigatorio
def concluir_tarefa(tarefa_id):
    tarefa = banco.buscar_tarefa_por_id(tarefa_id, session["usuario_id"])
    if tarefa:
        banco.atualizar_tarefa(tarefa_id, session["usuario_id"], status="concluida")
        flash("Tarefa marcada como concluída!", "success")
    else:
        flash("Tarefa não encontrada.", "warning")
    return redirect(url_for("dashboard"))


@app.route("/api/tarefas", methods=["GET"])
@login_obrigatorio
def api_listar_tarefas():
    status = request.args.get("status", "").strip()
    if status and status not in STATUS_INFO:
        return jsonify({"erro": "Status inválido."}), 400
    tarefas = banco.listar_tarefas(session["usuario_id"], status or None)
    return jsonify(tarefas)


@app.route("/api/tarefas", methods=["POST"])
@login_obrigatorio
def api_criar_tarefa():
    dados = request.get_json(silent=True) or request.form
    titulo = str(dados.get("titulo", "")).strip()
    descricao = str(dados.get("descricao", "")).strip()
    status = str(dados.get("status", "pendente")).strip()

    if not validar_titulo(titulo):
        return jsonify({"erro": "Título é obrigatório (até 120 caracteres)."}), 400
    if not validar_descricao(descricao):
        return jsonify({"erro": "Descrição muito longa (máx. 500)."}), 400
    if status not in STATUS_INFO:
        return jsonify({"erro": "Status inválido."}), 400

    tarefa_id = banco.criar_tarefa(titulo, descricao, status, session["usuario_id"])
    return (
        jsonify(banco.buscar_tarefa_por_id(tarefa_id, session["usuario_id"])),
        201,
    )


@app.route("/api/tarefas/<int:tarefa_id>", methods=["PUT", "POST"])
@login_obrigatorio
def api_atualizar_tarefa(tarefa_id):
    tarefa = banco.buscar_tarefa_por_id(tarefa_id, session["usuario_id"])
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada."}), 404

    dados = request.get_json(silent=True) or request.form
    titulo = str(dados.get("titulo", tarefa["titulo"])).strip()
    descricao = str(dados.get("descricao", tarefa["descricao"])).strip()
    status = str(dados.get("status", tarefa["status"])).strip()

    if not validar_titulo(titulo):
        return jsonify({"erro": "Título não pode ficar vazio (até 120)."}), 400
    if not validar_descricao(descricao):
        return jsonify({"erro": "Descrição muito longa (máx. 500)."}), 400
    if status not in STATUS_INFO:
        return jsonify({"erro": "Status inválido."}), 400

    banco.atualizar_tarefa(
        tarefa_id,
        session["usuario_id"],
        titulo=titulo,
        descricao=descricao,
        status=status,
    )
    return jsonify(banco.buscar_tarefa_por_id(tarefa_id, session["usuario_id"]))


@app.route("/api/tarefas/<int:tarefa_id>", methods=["DELETE"])
@login_obrigatorio
def api_excluir_tarefa(tarefa_id):
    if banco.excluir_tarefa(tarefa_id, session["usuario_id"]):
        return jsonify({"mensagem": "Tarefa excluída com sucesso."})
    return jsonify({"erro": "Tarefa não encontrada."}), 404


@app.route("/api/estatisticas")
@login_obrigatorio
def api_estatisticas():
    return jsonify(banco.contar_tarefas(session["usuario_id"]))


if __name__ == "__main__":
    producao = os.environ.get("FLASK_ENV") == "production"
    app.run(debug=not producao)