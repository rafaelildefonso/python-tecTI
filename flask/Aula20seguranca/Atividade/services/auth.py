# ATIVIDADE — regras de auth quebradas. Arrume senha, fresh, blocklist.

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_jwt,
)

from models import TokenRevogado, Usuario, db

USUARIOS_DEMO = [
    ("admin", "Admin da Torre", "admin123", "admin"),
    ("piloto", "Piloto da Sala", "piloto123", "piloto"),
    ("visitante", "Visitante do Hangar", "visitante123", "visitante"),
]


def emitir_tokens(usuario: Usuario, fresh: bool = True) -> dict:
    access_token = create_access_token(identity=usuario, fresh=fresh)
    refresh_token = create_refresh_token(identity=usuario)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "fresh": fresh,
        "usuario": usuario.para_dict(),
    }


def autenticar(username: str, senha: str) -> Usuario:
    usuario = Usuario.buscar_por_username((username or "").strip().lower())
    if not usuario or not usuario.senha_confere(senha):
        raise ValueError("username ou senha incorretos")
    return usuario


def registrar(dados: dict) -> Usuario:
    usuario = Usuario.a_partir_de_dict(dados)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def renovar_access(usuario: Usuario) -> dict:
    access_token = create_access_token(identity=usuario, fresh=False)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "fresh": False,
        "usuario": usuario.para_dict(),
    }


def revogar_jwt_atual() -> dict:
    payload = get_jwt()
    jti = payload.get("jti")
    tipo = payload.get("type")
    usuario_id = payload.get("sub")
    
    token_revogado = TokenRevogado(jti=jti, tipo=tipo, usuario_id=usuario_id)
    db.session.add(token_revogado)
    db.session.commit()
    
    return {
        "mensagem": "Logout realizado. Token revogado.",
        "jti": jti,
        "tipo": tipo,
    }


def trocar_senha(usuario: Usuario, senha_atual: str, senha_nova: str) -> None:
    if not usuario.senha_confere(senha_atual):
        raise ValueError("Senha atual incorreta")
    usuario.definir_senha(senha_nova)
    db.session.commit()


def popular_usuarios() -> None:
    if Usuario.query.count() > 0:
        return
    for username, nome, senha, papel in USUARIOS_DEMO:
        usuario = Usuario(username=username, nome=nome, papel=papel)
        usuario.definir_senha(senha)
        db.session.add(usuario)
    db.session.commit()
