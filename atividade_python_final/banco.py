import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).parent / "tarefas.db"

STATUS_VALIDOS = {"pendente", "em andamento", "concluida"}


def conectar():
    """Abre uma conexao com o banco e retorna o objeto de conexao."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    """Cria as tabelas usuarios e tarefas caso ainda nao existam."""
    conexao = conectar()
    try:
        with conexao:
            conexao.execute(
                """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL
                )
                """
            )
            conexao.execute(
                """
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'pendente',
                    usuario_id INTEGER NOT NULL,
                    data_criacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
                )
                """
            )
    finally:
        conexao.close()


def criar_usuario(nome, email, senha_hash):
    """Insere um novo usuario e retorna o id criado."""
    conexao = conectar()
    try:
        cursor = conexao.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash),
        )
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()


def buscar_usuario_por_email(email):
    """Retorna o usuario com o e-mail informado ou None."""
    conexao = conectar()
    try:
        linha = conexao.execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()
        return dict(linha) if linha else None
    finally:
        conexao.close()


def buscar_usuario_por_id(usuario_id):
    """Retorna o usuario com o id informado ou None."""
    conexao = conectar()
    try:
        linha = conexao.execute(
            "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()
        return dict(linha) if linha else None
    finally:
        conexao.close()


def listar_tarefas(usuario_id, status=None):
    """Lista as tarefas do usuario, com filtro opcional por status."""
    conexao = conectar()
    try:
        if status:
            linhas = conexao.execute(
                """
                SELECT * FROM tarefas
                WHERE usuario_id = ? AND status = ?
                ORDER BY data_criacao DESC
                """,
                (usuario_id, status),
            ).fetchall()
        else:
            linhas = conexao.execute(
                """
                SELECT * FROM tarefas
                WHERE usuario_id = ?
                ORDER BY data_criacao DESC
                """,
                (usuario_id,),
            ).fetchall()
        return [dict(linha) for linha in linhas]
    finally:
        conexao.close()


def buscar_tarefa_por_id(tarefa_id, usuario_id):
    """Retorna uma tarefa do usuario por id, ou None se nao existir."""
    conexao = conectar()
    try:
        linha = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?",
            (tarefa_id, usuario_id),
        ).fetchone()
        return dict(linha) if linha else None
    finally:
        conexao.close()


def criar_tarefa(titulo, descricao, status, usuario_id):
    """Insere uma nova tarefa e retorna o id criado."""
    conexao = conectar()
    try:
        cursor = conexao.execute(
            """
            INSERT INTO tarefas (titulo, descricao, status, usuario_id)
            VALUES (?, ?, ?, ?)
            """,
            (titulo, descricao, status, usuario_id),
        )
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()


def atualizar_tarefa(tarefa_id, usuario_id, titulo=None, descricao=None, status=None):
    """Atualiza os campos informados de uma tarefa do usuario."""
    conexao = conectar()
    try:
        cursor = conexao.execute(
            """
            UPDATE tarefas
            SET titulo = COALESCE(?, titulo),
                descricao = COALESCE(?, descricao),
                status = COALESCE(?, status)
            WHERE id = ? AND usuario_id = ?
            """,
            (titulo, descricao, status, tarefa_id, usuario_id),
        )
        conexao.commit()
        return cursor.rowcount > 0
    finally:
        conexao.close()


def excluir_tarefa(tarefa_id, usuario_id):
    """Remove uma tarefa do usuario. Retorna True se removeu."""
    conexao = conectar()
    try:
        cursor = conexao.execute(
            "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
            (tarefa_id, usuario_id),
        )
        conexao.commit()
        return cursor.rowcount > 0
    finally:
        conexao.close()


def contar_tarefas(usuario_id):
    """Conta tarefas por status e retorna um dicionario."""
    conexao = conectar()
    try:
        contagem = {"pendente": 0, "em andamento": 0, "concluida": 0}
        for linha in conexao.execute(
            """
            SELECT status, COUNT(*) AS quantidade
            FROM tarefas
            WHERE usuario_id = ?
            GROUP BY status
            """,
            (usuario_id,),
        ):
            if linha["status"] in contagem:
                contagem[linha["status"]] = linha["quantidade"]
        contagem["total"] = sum(contagem.values())
        return contagem
    finally:
        conexao.close()