import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request, url_for

app = Flask(__name__)

ARQUIVO_DADOS = Path(__file__).parent / "dados.json"


def carregar_dados():
    with open(ARQUIVO_DADOS, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def dados_publicos(dados):
    """Retorna JSON sem expor senhas (para API e aula)."""
    return {
        "site_cotemig": dados["site_cotemig"],
        "mensagens": dados["mensagens"],
    }


@app.route("/")
def index():
    return render_template("index.html", dados=carregar_dados())


# --- Fluxo 1: request.form (POST tradicional) ---


@app.route("/fluxo1/")
def fluxo1_inicio():
    return render_template("fluxo1_inicio.html", dados=carregar_dados())


@app.route("/fluxo1/senha", methods=["GET", "POST"])
def fluxo1_senha():
    dados = carregar_dados()
    erro = None
    sucesso = None

    if request.method == "POST":
        senha = request.form.get("senha", "")
        if senha == dados["senhas"]["fluxo1"]:
            sucesso = dados["mensagens"]["sucesso_fluxo1"]
        else:
            erro = dados["mensagens"]["erro_senha"]

    return render_template(
        "fluxo1_senha.html",
        dados=dados,
        erro=erro,
        sucesso=sucesso,
    )


# --- Fluxo 2: fetch + jsonify ---


@app.route("/fluxo2/")
def fluxo2_inicio():
    return render_template("fluxo2_inicio.html", dados=carregar_dados())


@app.route("/fluxo2/senha")
def fluxo2_senha():
    return render_template("fluxo2_senha.html", dados=carregar_dados())


@app.route("/fluxo2/cotemig")
def fluxo2_cotemig():
    return render_template("cotemig.html", dados=carregar_dados())


@app.route("/api/info")
def api_info():
    return jsonify(dados_publicos(carregar_dados()))


@app.route("/api/validar-senha", methods=["POST"])
def api_validar_senha():
    dados = carregar_dados()
    corpo = request.get_json(silent=True) or {}

    fluxo = corpo.get("fluxo")
    senha = corpo.get("senha", "")

    if fluxo == "fluxo2" and senha == dados["senhas"]["fluxo2"]:
        return jsonify(
            {
                "ok": True,
                "mensagem": dados["mensagens"]["sucesso_fluxo2"],
                # url_for gera a URL da rota fluxo2_cotemig (evita path fixo no JSON)
                "redirect": url_for("fluxo2_cotemig"),
            }
        )

    return jsonify(
        {
            "ok": False,
            "mensagem": dados["mensagens"]["erro_senha"],
        }
    ), 401


if __name__ == "__main__":
    app.run(debug=True)
