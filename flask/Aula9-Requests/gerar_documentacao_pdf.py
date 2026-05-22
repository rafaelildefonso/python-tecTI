# -*- coding: utf-8 -*-
"""Gera o PDF de documentacao detalhada da Aula 9."""

from pathlib import Path

from fpdf import FPDF

PASTA = Path(__file__).parent
SAIDA = PASTA / "Documentacao_Aula9_Requests.pdf"


class DocumentacaoPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")


def secao(pdf, titulo, nivel=1):
    pdf.ln(4)
    if nivel == 1:
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_fill_color(227, 242, 253)
    else:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 8, titulo, ln=True, fill=True)
    pdf.ln(2)


def paragrafo(pdf, texto, indent=0):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(pdf.l_margin + indent)
    pdf.multi_cell(0, 5.5, texto)
    pdf.ln(1)


def lista_item(pdf, texto):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(pdf.l_margin + 5)
    pdf.multi_cell(0, 5.5, "- " + texto)


def codigo(pdf, texto):
    pdf.set_font("Courier", "", 9)
    pdf.set_fill_color(240, 240, 240)
    for linha in texto.strip().split("\n"):
        pdf.cell(0, 5, "  " + linha, ln=True, fill=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)


def gerar():
    pdf = DocumentacaoPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(20, 20, 20)
    pdf.add_page()

    # Capa
    pdf.set_font("Helvetica", "B", 20)
    pdf.ln(30)
    pdf.cell(0, 12, "Documentacao Detalhada", ln=True, align="C")
    pdf.cell(0, 12, "Aula 9 - Flask Requests", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(
        0,
        7,
        "Material de apoio"
        "do projeto: app.py, dados.json, CSS, JavaScript e templates Jinja2.",
        align="C",
    )
    pdf.ln(20)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 8, "Janaína Duarte", ln=True, align="C")

    pdf.add_page()
    secao(pdf, "1. Visao geral do projeto")

    paragrafo(
        pdf,
        "Este projeto da Aula 9 demonstra duas maneiras diferentes de o navegador "
        "enviar informacoes ao servidor Flask e receber respostas. O objetivo pedagogico "
        "e consolidar conceitos vistos nas aulas anteriores (templates HTML na Aula 8, "
        "formularios na Aula 6) e introduzir JSON, jsonify, request.form, request.get_json "
        "e fetch no JavaScript.",
    )
    paragrafo(
        pdf,
        "O aluno percorre dois fluxos independentes. No Fluxo 1, a validacao da senha "
        "ocorre no servidor quando o formulario HTML e enviado por POST; o Flask le os "
        "dados com request.form. No Fluxo 2, a pagina de senha nao recarrega para validar: "
        "o JavaScript envia um fetch para uma rota de API que responde com jsonify; se a "
        "senha estiver correta, o navegador e redirecionado para uma pagina com o link "
        "oficial do site do Cotemig (https://cotemig.com.br/).",
    )

    paragrafo(pdf, "Estrutura de pastas do projeto:")
    codigo(
        pdf,
        """
Aula9-Requests/
  app.py                 (servidor Flask - rotas e logica)
  dados.json             (configuracao e textos)
  gerar_documentacao_pdf.py
  static/
    css/style.css        (estilos)
    js/main.js           (fetch no fluxo 2)
  templates/
    base.html            (layout pai - heranca Jinja)
    index.html           (pagina inicial)
    fluxo1_inicio.html
    fluxo1_senha.html
    fluxo2_inicio.html
    fluxo2_senha.html
    cotemig.html         (link externo Cotemig)
""",
    )

    paragrafo(pdf, "Senhas de demonstracao para a aula:")
    lista_item(pdf, "Fluxo 1: aluno2026")
    lista_item(pdf, "Fluxo 2: cotemig")

    paragrafo(pdf, "Como executar: python app.py e abrir http://127.0.0.1:5000/")

    # app.py
    pdf.add_page()
    secao(pdf, "2. Arquivo app.py")
    paragrafo(
        pdf,
        "O app.py e o coracao do sistema. Ele cria a aplicacao Flask, define todas as "
        "rotas (URLs), carrega o arquivo dados.json, valida senhas e decide se a resposta "
        "sera uma pagina HTML (render_template) ou dados JSON (jsonify).",
    )

    secao(pdf, "2.1 Importacoes e configuracao inicial", 2)
    codigo(
        pdf,
        """
import json
from pathlib import Path
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
ARQUIVO_DADOS = Path(__file__).parent / "dados.json"
""",
    )
    paragrafo(
        pdf,
        "Flask: framework web. jsonify: converte dicionario Python em resposta JSON. "
        "render_template: monta HTML a partir de arquivos na pasta templates. "
        "request: objeto que representa a requisicao HTTP atual (formulario, JSON, metodo). "
        "Path(__file__).parent garante que dados.json seja encontrado na mesma pasta do app.py, "
        "mesmo se o comando for executado de outro diretorio.",
    )

    secao(pdf, "2.2 Funcao carregar_dados()", 2)
    paragrafo(
        pdf,
        "Abre dados.json com encoding utf-8 e retorna um dicionario Python. Esse dicionario "
        "e usado nas rotas para comparar senhas e passar textos aos templates. Separar dados "
        "em JSON permite alterar mensagens e senhas sem mexer na logica Python - util em aula.",
    )

    secao(pdf, "2.3 Funcao dados_publicos()", 2)
    paragrafo(
        pdf,
        "Retorna apenas site_cotemig e mensagens, sem o objeto senhas. A rota /api/info "
        "usa essa funcao para ensinar que APIs publicas nao devem vazar credenciais. "
        "E um ponto importante de seguranca para comentar com a turma.",
    )

    secao(pdf, "2.4 Rota index - pagina inicial (/)", 2)
    paragrafo(
        pdf,
        "Metodo GET implicito. Renderiza index.html passando dados=carregar_dados(). "
        "A pagina inicial apresenta os dois fluxos e um link para /api/info.",
    )

    secao(pdf, "2.5 Fluxo 1 - rotas /fluxo1/ e /fluxo1/senha", 2)
    paragrafo(
        pdf,
        "fluxo1_inicio: apenas exibe HTML explicativo com link para a pagina de senha.",
    )
    paragrafo(
        pdf,
        "fluxo1_senha aceita GET e POST. No GET, mostra o formulario vazio. No POST, "
        "request.form.get('senha') le o campo enviado pelo formulario. Compara com "
        "dados['senhas']['fluxo1']. Se igual, define variavel sucesso; senao, erro. "
        "O mesmo template e renderizado de novo, mas agora com mensagem de alerta - "
        "padrao Post/Redirect/Get simplificado sem redirect, adequado para iniciantes.",
    )

    secao(pdf, "2.6 Fluxo 2 - rotas /fluxo2/", 2)
    paragrafo(
        pdf,
        "fluxo2_inicio e fluxo2_senha: paginas HTML. fluxo2_cotemig: pagina final com "
        "link para https://cotemig.com.br/. O acesso a essa pagina no fluxo ideal ocorre "
        "apos validacao via API; a rota em si nao exige senha novamente (em producao "
        "usaria-se sessao ou token).",
    )

    secao(pdf, "2.7 API /api/info", 2)
    paragrafo(
        pdf,
        "Retorna jsonify(dados_publicos(...)). O navegador recebe JSON puro. Serve para "
        "mostrar jsonify isolado e para o botao Ver /api/info na pagina inicial.",
    )

    secao(pdf, "2.8 API /api/validar-senha (POST)", 2)
    paragrafo(
        pdf,
        "request.get_json(silent=True) le o corpo JSON enviado pelo fetch. Espera "
        "fluxo: fluxo2 e senha. Se corretos, jsonify com ok: true e redirect: /fluxo2/cotemig. "
        "Se incorretos, jsonify com ok: false e codigo HTTP 401 (nao autorizado). "
        "O codigo 401 ensina que APIs comunicam estado por status HTTP, nao so pelo JSON.",
    )

    secao(pdf, "2.9 app.run(debug=True)", 2)
    paragrafo(
        pdf,
        "Inicia servidor local na porta 5000. debug=True recarrega ao salvar arquivos e "
        "mostra rastreamento de erros - apenas em desenvolvimento, nunca em producao.",
    )

    # dados.json
    pdf.add_page()
    secao(pdf, "3. Arquivo dados.json")
    paragrafo(
        pdf,
        "Arquivo de configuracao em formato JSON (JavaScript Object Notation). JSON usa "
        "chaves entre aspas duplas, valores string, numero, booleano, array ou objeto. "
        "Qualquer linguagem le JSON; por isso e padrao em APIs.",
    )

    secao(pdf, "3.1 Objeto senhas", 2)
    lista_item(pdf, "fluxo1: aluno2026 - senha do formulario POST")
    lista_item(pdf, "fluxo2: cotemig - senha validada pela API")

    secao(pdf, "3.2 site_cotemig", 2)
    paragrafo(
        pdf,
        "URL https://cotemig.com.br/ usada no template cotemig.html. O projeto nao "
        "incorpora o site dentro da aplicacao; apenas oferece um link externo (target=_blank).",
    )

    secao(pdf, "3.3 Objeto mensagens", 2)
    paragrafo(
        pdf,
        "Centraliza textos exibidos nas telas. Vantagens: um unico lugar para editar frases; "
        "templates mais limpos com {{ dados.mensagens.fluxo1_titulo }}; prepara alunos para "
        "internacionalizacao (i18n) no futuro.",
    )

    # CSS
    pdf.add_page()
    secao(pdf, "4. Arquivo static/css/style.css")
    paragrafo(
        pdf,
        "Folha de estilos simples e pedagogica. Flask serve arquivos da pasta static/ na URL "
        "/static/... O base.html referencia com url_for('static', filename='css/style.css').",
    )

    secao(pdf, "4.1 Reset e body", 2)
    paragrafo(
        pdf,
        "Seletor * zera margin e padding e usa box-sizing border-box para larguras previsiveis. "
        "body define fonte Segoe UI, fundo cinza-azulado (#f0f4f8), cor do texto e altura minima 100vh.",
    )

    secao(pdf, "4.2 Layout .container", 2)
    paragrafo(
        pdf,
        "Centraliza conteudo com max-width 520px - layout de cartao estreito, bom para formularios.",
    )

    secao(pdf, "4.3 Componentes principais", 2)
    lista_item(pdf, ".card: caixa branca com borda, sombra leve e padding")
    lista_item(pdf, ".btn e .btn-secondary: botoes azul primario e cinza secundario")
    lista_item(pdf, ".alert-erro, .alert-ok, .alert-info: feedback visual")
    lista_item(pdf, ".nav-links: flexbox para alinhar links de navegacao")
    lista_item(pdf, ".hidden: display none - usado no JS para esconder mensagem de erro")
    lista_item(pdf, ".link-externo: destaque do link do Cotemig")

    paragrafo(
        pdf,
        "Nao ha responsividade avancada nem framework CSS; proposital para a turma focar em Flask.",
    )

    # JS
    pdf.add_page()
    secao(pdf, "5. Arquivo static/js/main.js")
    paragrafo(
        pdf,
        "JavaScript carregado em todas as paginas pelo base.html, mas so atua no Fluxo 2 "
        "(quando existe #form-senha-fluxo2). Se o elemento nao existir, a funcao retorna cedo.",
    )

    secao(pdf, "5.1 DOMContentLoaded", 2)
    paragrafo(
        pdf,
        "Garante que o HTML ja foi montado antes de buscar elementos. Evita erro de null.",
    )

    secao(pdf, "5.2 Evento submit do formulario", 2)
    paragrafo(
        pdf,
        "event.preventDefault() impede o envio tradicional do formulario (que recarregaria a pagina). "
        "A validacao passa a ser assincrona via fetch.",
    )

    secao(pdf, "5.3 fetch para /api/validar-senha", 2)
    codigo(
        pdf,
        """
fetch("/api/validar-senha", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ fluxo: "fluxo2", senha: senha })
})
""",
    )
    paragrafo(
        pdf,
        "fetch e a API moderna do navegador para HTTP (equivalente pedagogico a biblioteca "
        "requests do Python, mas no cliente). Content-Type application/json informa ao Flask "
        "que o corpo e JSON (request.get_json). resposta.json() converte a resposta em objeto.",
    )

    secao(pdf, "5.4 Tratamento de sucesso e erro", 2)
    paragrafo(
        pdf,
        "Se dados.ok for true, window.location.href redireciona para /fluxo2/cotemig. "
        "Senao, exibe mensagem em #msg-erro removendo classe hidden. try/catch cobre falha de rede. "
        "finally restaura o botao - boa pratica de UX.",
    )

    # Templates
    pdf.add_page()
    secao(pdf, "6. Templates Jinja2 e heranca")
    paragrafo(
        pdf,
        "Jinja2 e o motor de templates do Flask. Heranca significa: um arquivo base define "
        "a estrutura comum; os filhos estendem com {% extends %} e preenchem {% block %}.",
    )

    secao(pdf, "6.1 base.html - template pai", 2)
    paragrafo(
        pdf,
        "Define esqueleto HTML5: head com charset UTF-8, viewport, titulo dinamico no block titulo, "
        "link do CSS, header com block cabecalho e subtitulo, main com block conteudo, footer com "
        "block rodape, script main.js e block scripts_extra para scripts adicionais por pagina.",
    )
    paragrafo(
        pdf,
        "url_for('static', filename='...') gera URL correta do arquivo estatico. "
        "url_for('nome_da_funcao') gera URL da rota pelo nome da funcao Python em app.py.",
    )

    secao(pdf, "6.2 index.html", 2)
    paragrafo(
        pdf,
        "Pagina menu com tres cards: apresentacao Fluxo 1, Fluxo 2 e link para API. "
        "Usa url_for('fluxo1_inicio'), url_for('fluxo2_inicio'), url_for('api_info').",
    )

    secao(pdf, "6.3 fluxo1_inicio.html", 2)
    paragrafo(
        pdf,
        "Estende base. Cabecalho vem de dados.mensagens.fluxo1_titulo (passado pelo Flask). "
        "Explica POST e request.form. Botao leva a fluxo1_senha.",
    )

    secao(pdf, "6.4 fluxo1_senha.html", 2)
    paragrafo(
        pdf,
        "{% if erro %} e {% if sucesso %} mostram alertas condicionais. Form method POST "
        "action url_for('fluxo1_senha') - envia para a mesma rota que processa. "
        "Campo name=senha deve coincidir com request.form.get('senha').",
    )

    secao(pdf, "6.5 fluxo2_inicio.html e fluxo2_senha.html", 2)
    paragrafo(
        pdf,
        "Inicio analogo ao fluxo 1. Senha: form id form-senha-fluxo2 sem method/action "
        "porque o JS intercepta. div msg-erro com class hidden inicialmente.",
    )

    secao(pdf, "6.6 cotemig.html", 2)
    paragrafo(
        pdf,
        "Pagina de sucesso do Fluxo 2. Link href={{ dados.site_cotemig }} target=_blank "
        "abre site oficial em nova aba. rel=noopener noreferrer e boa pratica de seguranca.",
    )

    # Fluxograma e comparacao
    pdf.add_page()
    secao(pdf, "7. Fluxo de dados passo a passo")

    secao(pdf, "7.1 Fluxo 1 - request.form", 2)
    lista_item(pdf, "Usuario abre /fluxo1/")
    lista_item(pdf, "Clica Ir para a senha -> GET /fluxo1/senha")
    lista_item(pdf, "Digita senha e clica Validar -> POST /fluxo1/senha")
    lista_item(pdf, "Flask le request.form, compara com dados.json")
    lista_item(pdf, "Re-renderiza fluxo1_senha.html com erro ou sucesso")

    secao(pdf, "7.2 Fluxo 2 - fetch + jsonify", 2)
    lista_item(pdf, "Usuario abre /fluxo2/ e depois /fluxo2/senha")
    lista_item(pdf, "Digita senha; JS envia POST JSON para /api/validar-senha")
    lista_item(pdf, "Flask responde jsonify; JS le dados.ok")
    lista_item(pdf, "Redirect para /fluxo2/cotemig com link https://cotemig.com.br/")

    secao(pdf, "8. Tabela comparativa para a aula", 2)
    codigo(
        pdf,
        """
| Aspecto          | Fluxo 1              | Fluxo 2                |
|------------------|----------------------|------------------------|
| Envio de dados   | Formulario HTML POST | fetch + JSON           |
| Leitura Flask    | request.form         | request.get_json       |
| Resposta         | HTML (template)      | JSON (jsonify)         |
| Pagina recarrega | Sim                  | Nao (ate redirect)     |
| Pagina final     | Mensagem na mesma    | cotemig.html + link    |
""",
    )

    secao(pdf, "9. Sugestoes de condução em sala")
    lista_item(pdf, "Demonstrar /api/info no navegador antes dos fluxos")
    lista_item(pdf, "Abrir Ferramentas do Desenvolvedor (Rede) no Fluxo 2 para ver o POST JSON")
    lista_item(pdf, "Comparar com Aula 8: render_template com painel completo")
    lista_item(pdf, "Discutir por que senhas em JSON de aula nao sao seguras em producao")
    lista_item(pdf, "Mencionar biblioteca requests do Python como proximo passo (cliente servidor)")

    secao(pdf, "10. Referencias")
    paragrafo(pdf, "Documentacao Flask: https://flask.palletsprojects.com/")
    paragrafo(pdf, "Site Cotemig: https://cotemig.com.br/")
    paragrafo(pdf, "MDN fetch API: https://developer.mozilla.org/pt-BR/docs/Web/API/Fetch_API")

    pdf.output(SAIDA)
    print(f"PDF gerado: {SAIDA}")


if __name__ == "__main__":
    gerar()
