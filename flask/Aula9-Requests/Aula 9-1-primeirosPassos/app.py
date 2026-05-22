from flask import Flask, redirect, render_template, request, url_for

# url_for  → monta a URL a partir do NOME da função da rota (ex: 'login' → '/login')
# redirect → manda o navegador para outra página (HTTP 302)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if username:
            # redirect + url_for: após o login, vai para /nome-do-usuario
            return redirect(url_for("usuario", user=username))
    return render_template("login.html")


@app.route("/<user>")
def usuario(user):
    return f"<h1>Bem-vindo, {user}!</h1><p><a href='{url_for('index')}'>Início</a></p>"


if __name__ == "__main__":
    app.run(debug=True)
