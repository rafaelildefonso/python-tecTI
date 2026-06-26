# Atividade Aula 12 — Model, Controller e View (StreamFlix)

**Disciplina:** Python / Flask  
**Profª:** Janaína Duarte  
**Projeto:** `flask/Aula12/`  
**Objetivo:** Explorar o código, localizar arquivos e explicar o que cada camada faz.

---

## Como responder

1. Abra a pasta `flask/Aula12/` no editor ou GitHub.
2. Navegue pelas pastas `models/`, `controllers/` e `views/`.
3. Rode o site (`python app.py`) quando a pergunta pedir para testar no navegador.
4. Responda com **caminho do arquivo** + **explicação em suas palavras**.

**Identificação**

- Nome: Rafael Ildefonso Furtado
- Turma: 3A1

---

## Bloco A — Model (perguntas 1 a 10)

**1.** Em qual pasta ficam as classes que representam tabelas do banco SQLite? Cite o caminho.

Resposta: 'models/' — é a pasta onde estão os arquivos das classes de tabela.

**2.** Qual é o nome do arquivo de banco criado quando o app roda? Em qual arquivo Python essa configuração está?

Resposta: 'streamflix.db' é o arquivo do banco. A configuração está em 'app.py' na linha do 'SQLALCHEMY_DATABASE_URI'.

**3.** Quais classes Model existem no projeto (nome das classes)? Em quais arquivos `.py` cada uma está?

Resposta: 'FilmeFavorito' em 'models/filme_favorito.py' e 'HistoricoBusca' em 'models/historico_busca.py'.

**4.** De qual superclasse `FilmeFavorito` e `HistoricoBusca` herdam? O que elas ganham automaticamente por herança (cite 3 campos)?

Resposta: Elas herdam de 'ModeloBase' em 'models/base.py'. Elas ganham 'id', 'data_criacao' e 'data_atualizacao' automaticamente.

**5.** Qual é o `__tablename__` da tabela de favoritos? Por que usamos `__tablename__` em vez de só o nome da classe?

Resposta: '__tablename__' é 'filmes_favoritos'. Usamos para dizer o nome exato da tabela no banco, porque a classe pode ser diferente do nome da tabela.

**6.** No model `FilmeFavorito`, qual coluna guarda o id do filme vindo da API TMDB? Ela tem alguma restrição especial (`unique`, `nullable`)?

Resposta: A coluna é 'tmdb_id'. Ela tem 'unique=True' e 'nullable=False'.

**7.** Abra `models/filme_favorito.py`. O que o método `@classmethod adicionar` faz passo a passo? O que acontece se o filme já existir nos favoritos?

Resposta: Primeiro ele verifica se já existe um favorito com esse 'tmdb_id'. Se já existir, retorna 'None'. Se não existir, cria o objeto 'FilmeFavorito', adiciona ao banco e dá 'db.session.commit()'.

**8.** Onde está o método que lista as últimas 8 buscas? Qual é o nome da classe e do método?

Resposta: Em 'models/historico_busca.py'. Classe 'HistoricoBusca', método 'ultimas()'.

**9.** O model grava dados da API TMDB inteira ou só alguns campos espelhados? Cite 4 campos salvos em `FilmeFavorito`.

Resposta: Salva só alguns campos espelhados. Exemplo: 'tmdb_id', 'titulo', 'poster_path', 'nota', 'ano'.

**10.** Em `models/__init__.py`, o que é exportado além de `db`? Por que o controller importa `from models import FilmeFavorito` em vez de importar o arquivo inteiro da pasta?

Resposta: Exporta 'ModeloBase', 'FilmeFavorito' e 'HistoricoBusca'. O controller importa assim porque fica mais simples usar as classes diretas do pacote.

---

## Bloco B — Controller (perguntas 11 a 20)

**11.** Quantos Blueprints existem no projeto? Cite o **nome** de cada um e o **url_prefix** (se tiver).

Resposta: Existem 3 Blueprints:
'dashboard_bp' sem 'url_prefix'
'filmes_bp' com 'url_prefix='/filmes''
'favoritos_bp' com 'url_prefix='/favoritos''

**12.** Em qual arquivo está a rota `/filmes/populares`? Qual é o nome da função Python que responde essa URL?

Resposta: Está em 'controllers/filmes_controller.py'. A função é 'populares()'.

**13.** O que a função `populares()` faz antes de chamar `render_template`? Cite duas chamadas (Model, Service ou API).

Resposta: Chama 'TmdbApi().filmes_populares()' e chama 'FilmeFavorito.listar()'.

**14.** Quando o usuário busca um filme em `/filmes/buscar`, qual controller registra o termo no banco? Qual model é usado e em qual linha aproximada?

Resposta: O controller é 'controllers/filmes_controller.py'. O model usado é 'HistoricoBusca' e a linha é 'HistoricoBusca.registrar(termo, len(filmes))'.

**15.** Abra `controllers/favoritos_controller.py`. Qual método HTTP é exigido para adicionar favorito (`GET` ou `POST`)? Qual a URL completa de exemplo para adicionar o filme id 550?

Resposta: O método é 'POST'. A URL de exemplo é '/favoritos/adicionar/550'.

**16.** No `filmes_controller.py`, rota `detalhe(filme_id)`: o que acontece se `api.detalhe(filme_id)` retornar `None`?

Resposta: Ele redireciona para 'filmes.populares'.

**17.** Onde os Blueprints são **registrados** no Flask? Cite o arquivo e o comando usado (3 registros).

Resposta: Em 'app.py', com:
'app.register_blueprint(dashboard_bp)'
'app.register_blueprint(filmes_bp)'
'app.register_blueprint(favoritos_bp)'

**18.** Qual controller cuida da página inicial `/`? Quais variáveis ele envia para o template `index.html`?

Resposta: 'controllers/dashboard_controller.py'. Envia 'populares', 'melhores', 'total_favoritos', 'historico' e 'modo_demo'.

**19.** A pasta `services/tmdb_api.py` é Model, Controller ou View? Justifique: quem chama essa classe e para quê?

Resposta: É Service. Os controllers chamam essa classe para buscar dados da API TMDB como filmes populares, melhores, busca, detalhe e streaming.

**20.** No controller de busca, de onde vem o termo digitado quando o usuário usa o formulário da home (`index.html`)? É `request.form` ou `request.args`? Explique a diferença nesse projeto.

Resposta: Vem de 'request.args' quando o formulário usa 'method="GET"'. 'request.args' pega os dados da URL, e 'request.form' pega dados enviados por POST.

---

## Bloco C — View (perguntas 21 a 30)

**21.** Onde ficam os templates HTML? Qual caminho completo da pasta?

Resposta: Ficam em 'views/templates/'.

**22.** Qual template é a “base” de todas as páginas (layout com menu)? Como os outros templates usam esse layout (qual comando Jinja)?

Resposta: A base é 'views/templates/layout.html'. Os outros templates usam com '{% extends "layout.html" %}'.

**23.** Abra `views/templates/layout.html`. Liste os 5 links do menu e o `url_for` de cada um.

Resposta:
'StreamFlix' → 'url_for('dashboard.index')'
'Populares' → 'url_for('filmes.populares')'
'Melhores' → 'url_for('filmes.melhores')'
'Buscar' → 'url_for('filmes.buscar')'
'Favoritos' → 'url_for('favoritos.listar')'

**24.** Qual arquivo HTML exibe a seção **“Onde assistir (Brasil)”**? De onde vem a variável `streaming` usada nessa tela?

Resposta: Está em 'views/templates/filmes/detalhe.html'. A variável 'streaming' vem do controller 'controllers/filmes_controller.py', na função 'detalhe()' que chama 'api.streaming(filme_id)'.

**25.** O arquivo `filmes/_card.html` é uma página inteira ou um pedaço reutilizado? Quem inclui esse arquivo e com qual tag Jinja?

Resposta: É um pedaço reutilizado. Ele é incluído com '{% include "filmes/_card.html" %}' em 'filmes/buscar.html'.

**26.** Em `filmes/detalhe.html`, como a View sabe se o filme já está nos favoritos? Qual variável booleana/objeto controla o botão “Salvar” vs “Remover”?

Resposta: A view usa a variável 'favorito'. Se 'favorito' existe, mostra 'Remover', se não existe, mostra 'Salvar favorito'.

**27.** Onde está o CSS do site? Como o `layout.html` carrega esse arquivo (função Flask/Jinja)?

Resposta: O CSS está em 'views/static/css/style.css'. O layout carrega com '{{ url_for('static', filename='css/style.css') }}'.

**28.** Na listagem de favoritos (`favoritos/lista.html`), qual loop Jinja percorre os registros? Cite 3 campos exibidos na tabela.

Resposta: O loop é '{% for fav in favoritos %}'. Mostra 'fav.titulo', 'fav.nota', 'fav.ano', 'fav.data_criacao'.

**29.** O que significa `{% if modo_demo %}` no layout? Quem disponibiliza essa variável para **todos** os templates?

Resposta: Significa mostrar aviso de modo demonstração. A variável vem de 'app.context_processor' em 'app.py'.

**30.** Desenhe ou descreva o fluxo completo quando o aluno clica em **“Salvar favorito”** no detalhe do filme, indicando **View → Controller → Model** (e redirect de volta). Cite arquivos envolvidos.

Resposta: A view 'views/templates/filmes/detalhe.html' envia um POST para '/favoritos/adicionar/<tmdb_id>'. O controller em 'controllers/favoritos_controller.py' recebe o POST e chama 'FilmeFavorito.adicionar(...)' em 'models/filme_favorito.py'. O model salva o favorito no banco e o controller faz 'redirect(voltar)' para voltar à página anterior.

---

## Entrega

- Arquivo `.txt` ou `.md` com as 30 respostas 

**Critério:** respostas que mostrem que você **abriu o código**, não chute.

Boa exploração!
