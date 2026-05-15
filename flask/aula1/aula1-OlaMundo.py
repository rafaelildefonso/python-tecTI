from flask import Flask


app = Flask(__name__) # inicio o flask

@app.route('/') # Isso é o decorator, ele é usado para mapear a função abaixo para a rota '/'
def ola_mundo():
    return 'Olá, Mundo!' # Isso é o que será retornado quando a rota '/' for acessada

@app.route('/hello') # Isso é outro decorator, mapeando a função abaixo para a rota '/hello'
def hello():
    return 'Hello, World!' # Isso é o que será retornado quando a rota '/hello' for acessada

@app.route('/decorator')
def decorator():
    return ("""<b>O que é um decorator em Python:</b> Um decorator em Python é uma ferramenta poderosa que permite modificar ou estender o comportamento de funções ou classes sem alterar permanentemente o código original delas.<br><br>
            <b>Para que ele serve:</b> Basicamente, o decorator serve para evitar repetição de código (DRY - Don't Repeat Yourself) e manter sua lógica principal limpa. Ele "sequestra" a execução de uma função para injetar comportamentos extras.<br><br>
            <b>Como ele é utilizado no Flask (exemplo: @app.route):</b> Na Criação de Rotas, Proteção de Acesso, Tratamento de Erros, Ciclo de Vida da Requisição""")

if __name__ == '__main__':
    app.run(debug=True) # Isso inicia o servidor Flask em modo de depuração, o que é útil para desenvolvimento
