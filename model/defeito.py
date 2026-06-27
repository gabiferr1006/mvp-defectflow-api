from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import datetime
from typing import Union

from model import Base


class Defeito(Base):
    __tablename__ = 'defeito'

    id = Column("pk_defeito", Integer, primary_key=True)
    titulo = Column(String(140), unique=True)
    descricao = Column(String(4000))
    origem = Column(String(100))
    componente = Column(String(100))
    categoria = Column(String(100))
    severidade = Column(String(10))
    impacto_operacional = Column(String(200))
    impacto_seguranca = Column(Boolean)
    comite_sugerido = Column(String(20))
    responsavel = Column(String(100))
    status = Column(String(50))
    data_abertura = Column(DateTime, default=datetime.now())

    def __init__(
        self,
        titulo: str,
        descricao: str,
        origem: str,
        componente: str,
        categoria: str,
        severidade: str,
        impacto_operacional: str,
        impacto_seguranca: bool,
        responsavel: str,
        status: str = "Aberto",
        data_abertura: Union[DateTime, None] = None
    ):
        """
        Cria um registro de Defeito.

        Arguments:
            titulo: título resumido do defeito.
            descricao: descrição detalhada do problema identificado.
            origem: origem do defeito, como cliente, teste interno ou operação.
            componente: componente ou módulo impactado.
            categoria: categoria técnica ou processual do defeito.
            severidade: classificação inicial da severidade, como S1, S2, S3 ou S4.
            impacto_operacional: resumo do impacto percebido na operação.
            impacto_seguranca: indica se há potencial impacto à segurança.
            responsavel: pessoa ou área responsável pela análise.
            status: status atual da tratativa.
            data_abertura: data de abertura do registro.
        """
        self.titulo = titulo
        self.descricao = descricao
        self.origem = origem
        self.componente = componente
        self.categoria = categoria
        self.severidade = severidade
        self.impacto_operacional = impacto_operacional
        self.impacto_seguranca = impacto_seguranca
        self.responsavel = responsavel
        self.status = status

        self.comite_sugerido = self.definir_comite_sugerido()

        if data_abertura:
            self.data_abertura = data_abertura

    def definir_comite_sugerido(self):
        """
        Define uma sugestão simples de comitê com base na severidade
        e no possível impacto de segurança.
        """
        if self.impacto_seguranca:
            return "ECRB"

        if self.severidade in ["S1", "S2"]:
            return "ECRB"

        if self.severidade in ["S3", "S4"]:
            return "CRB"

        return "Não definido"