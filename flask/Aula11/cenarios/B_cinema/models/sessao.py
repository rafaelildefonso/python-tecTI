from . import db
from .base import ModeloBase


class Sessao(ModeloBase):
    __tablename__ = "sessoes"

    # TODO ALUNO: FK filme_id → filmes.id
    # TODO ALUNO: FK sala_id → salas.id
    data_hora = db.Column(db.DateTime, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    # TODO ALUNO: relationship filme, sala, ingressos

    @classmethod
    def listar_com_detalhes(cls):
        return cls.query.order_by(cls.data_hora.desc()).all()
