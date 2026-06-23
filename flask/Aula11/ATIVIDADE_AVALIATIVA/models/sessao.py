from . import db
from .base import ModeloBase


class Sessao(ModeloBase):
    __tablename__ = "sessoes"

    filme_id = db.Column(db.Integer, db.ForeignKey("filmes.id"), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey("salas.id"), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    filme = db.relationship("Filme", back_populates="sessoes", lazy=True)
    sala = db.relationship("Sala", back_populates="sessoes", lazy=True)

    @classmethod
    def listar_com_detalhes(cls):
        return cls.query.order_by(cls.data_hora.desc()).all()

    @classmethod
    def salvar(cls, filme_id, sala_id, data_hora, preco):
        sessao = cls(
            filme_id=filme_id,
            sala_id=sala_id,
            data_hora=data_hora,
            preco=preco,
        )
        db.session.add(sessao)
        db.session.commit()
        return sessao

    def __repr__(self):
        return f"<Sessao {self.id} filme={self.filme_id} sala={self.sala_id}>"
