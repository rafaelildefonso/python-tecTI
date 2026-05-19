from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    nome = "Turma de Python"
    return render_template('index.html', nome=nome)

@app.route('/ola/<nome>/<idade>')
def cumprimento(nome, idade):
    return render_template('index.html', nome=nome, idade=idade)

@app.route('/dados')
def mostrar_dados():
    dados = {"nome": "Ana", "email": "ana@email.com"}
    return render_template('dados.html', dados=dados)

@app.route('/alunos')
def alunos():
    lista_alunos = [
        {"nome": "Ana", "nota": 8},
        {"nome": "Bruno", "nota": 5},
        {"nome": "Carlos", "nota": 7}
    ]
    return render_template('alunos.html', alunos=lista_alunos)

if __name__ == '__main__':
    app.run(debug=True)