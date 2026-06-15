from . import db
from .base import ModeloBase


class OfertaTroca(ModeloBase):
    __tablename__ = "ofertas_troca"

    # TODO ALUNO: FK colecionador_id → colecionadores.id
    observacao = db.Column(db.String(255), nullable=True)

    # TODO ALUNO: relationship colecionador, itens

    @classmethod
    def listar_com_colecionador(cls):
        return cls.query.order_by(cls.data_criacao.desc()).all()


class ItemOferta(ModeloBase):
    __tablename__ = "itens_oferta"

    # TODO ALUNO: FK oferta_id, FK figurinha_id
    tipo = db.Column(db.String(20), nullable=False)  # "oferece" ou "deseja"
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    # TODO ALUNO: relationship oferta, figurinha
