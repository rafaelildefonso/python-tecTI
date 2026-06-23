from . import db
from .base import ModeloBase


class Filme(ModeloBase):
    __tablename__ = "filmes"

    titulo = db.Column(db.String(150), nullable=False)
    # TODO ALUNO: duracao_min (Integer), classificacao (String 5)
    # TODO ALUNO: relationship sessoes

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.titulo).all()
