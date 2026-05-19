from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', nome="Estudante de Python")

@app.route('/alunos')
def alunos():
    alunos = [{"nome": "Ana", "idade": 18}, {"nome": "Bruno", "idade": 20}, {"nome": "Carlos", "idade": 22}]
    return render_template('alunos.html', alunos=alunos)

@app.route('/usuario')
def usuario():
    usuario = {"nome": "Ana", "email": "ana@email.com"}
    return render_template('usuario.html', usuario=usuario)

@app.route('/lista_nomes')
def lista_nomes():
    nomes = ["Ana", "Bruno", "Carlos", "Daniela"]
    return render_template('lista_nomes.html', nomes=nomes)

@app.route('/notas')
def notas():
    alunos_notas = [
        {"nome": "Ana", "nota": 8.5},
        {"nome": "Bruno", "nota": 5.0},
        {"nome": "Carlos", "nota": 7.0}
    ]
    return render_template('notas.html', alunos=alunos_notas)

if __name__ == '__main__':
    app.run(debug=True)