from flask import Flask, request, render_template_string

app = Flask(__name__)

usuarios = [
    {'usuario': 'rafael', 'senha': '12402010'},
    {'usuario': 'marcos', 'senha': 'cotemig2026'},
    {'usuario': 'janaina', 'senha': 'cotemig2026'}
]

def verificar_credenciais(usuario, senha):
    """
    Função que PERCORRE o dicionário com FOR
    Itera sobre a lista de dicionários 'usuarios'
    """
    for u in usuarios:
        if u['usuario'] == usuario and u['senha'] == senha:
            return True
    return False

def show_the_login_form():
    return render_template_string("""
        <h2>Login</h2>
        <form action="/login" method="POST">
            <input type="text" name="usuario" placeholder="Usuário"><br><br>
            <input type="password" name="senha" placeholder="Senha"><br><br>
            <button type="submit">Entrar</button>
        </form>
    """)

def do_the_login():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    if verificar_credenciais(usuario, senha):
        return f"<h1>Bem-vindo, {usuario}!</h1><a href='/login'>Voltar</a>"
    else:
        return "<h1>Login inválido</h1><a href='/login'>Tentar novamente</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

@app.route('/')
def index():
    return login()

if __name__ == "__main__":
    app.run(debug=True)
