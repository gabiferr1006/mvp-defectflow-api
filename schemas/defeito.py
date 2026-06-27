from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from model.defeito import Defeito


class DefeitoSchema(BaseModel):
    """Define como um novo defeito deve ser representado para cadastro.
    """
    titulo: str = "Falha na abertura de tela operacional"
    descricao: str = "Usuário reportou erro ao acessar funcionalidade crítica do sistema."

    origem: Literal[
        "Cliente",
        "Teste interno",
        "Operação",
        "Monitoramento",
        "Auditoria",
        "Outro"
    ] = "Teste interno"

    componente: str = "Interface operacional"

    categoria: Literal[
        "Fadiga",
        "Desgaste",
        "Sobrecarga",
        "Fluência",
        "Falha de interface",
        "Falha de comunicação",
        "Falha de configuração",
        "Falha operacional",
        "Outro"
    ] = "Falha de interface"

    severidade: Literal[
        "S1",
        "S2",
        "S3",
        "S4"
    ] = "S2"

    impacto_operacional: str = "Funcionalidade indisponível para parte dos usuários."

    impacto_seguranca: bool = Field(
        default=False,
        description="Indica se existe potencial impacto à segurança. Use true para Sim e false para Não."
    )

    responsavel: str = "Time Técnico"

    status: Optional[Literal[
        "Aberto",
        "Em triagem",
        "Em análise técnica",
        "Aguardando comitê",
        "Plano de ação definido",
        "Em correção",
        "Encerrado",
        "Rejeitado"
    ]] = "Aberto"


class DefeitoBuscaSchema(BaseModel):
    """Define como deve ser a estrutura para busca de um defeito específico.
    A busca será feita pelo ID.
    """
    id: int = 1


class DefeitoUpdateSchema(BaseModel):
    """Define como deve ser a estrutura para atualização do status de um defeito.
    """
    id: int = 1

    status: Literal[
        "Aberto",
        "Em triagem",
        "Em análise técnica",
        "Aguardando comitê",
        "Plano de ação definido",
        "Em correção",
        "Encerrado",
        "Rejeitado"
    ] = "Em análise técnica"


class DefeitoViewSchema(BaseModel):
    """Define como um defeito será retornado pela API.
    """
    id: int = 1
    codigo_defeito: str = "DEF-0001"
    titulo: str = "Falha na abertura de tela operacional"
    descricao: str = "Usuário reportou erro ao acessar funcionalidade crítica do sistema."
    origem: str = "Teste interno"
    componente: str = "Interface operacional"
    categoria: str = "Falha de interface"
    severidade: str = "S2"
    impacto_operacional: str = "Funcionalidade indisponível para parte dos usuários."
    impacto_seguranca: bool = False
    comite_sugerido: str = "ECRB"
    responsavel: str = "Time Técnico"
    status: str = "Aberto"


class ListagemDefeitosSchema(BaseModel):
    """Define como uma listagem de defeitos será retornada.
    """
    defeitos: List[DefeitoViewSchema]


class DefeitoDelSchema(BaseModel):
    """Define a estrutura retornada após exclusão de um defeito.
    """
    message: str
    id: int


def gera_codigo_defeito(defeito_id: int):
    """Gera um código amigável para o defeito a partir do ID técnico.
    """
    return f"DEF-{defeito_id:04d}"


def apresenta_defeitos(defeitos: List[Defeito]):
    """Retorna uma representação da lista de defeitos.
    """
    result = []

    for defeito in defeitos:
        result.append({
            "id": defeito.id,
            "codigo_defeito": gera_codigo_defeito(defeito.id),
            "titulo": defeito.titulo,
            "descricao": defeito.descricao,
            "origem": defeito.origem,
            "componente": defeito.componente,
            "categoria": defeito.categoria,
            "severidade": defeito.severidade,
            "impacto_operacional": defeito.impacto_operacional,
            "impacto_seguranca": defeito.impacto_seguranca,
            "comite_sugerido": defeito.comite_sugerido,
            "responsavel": defeito.responsavel,
            "status": defeito.status
        })

    return {"defeitos": result}


def apresenta_defeito(defeito: Defeito):
    """Retorna uma representação de um defeito específico.
    """
    return {
        "id": defeito.id,
        "codigo_defeito": gera_codigo_defeito(defeito.id),
        "titulo": defeito.titulo,
        "descricao": defeito.descricao,
        "origem": defeito.origem,
        "componente": defeito.componente,
        "categoria": defeito.categoria,
        "severidade": defeito.severidade,
        "impacto_operacional": defeito.impacto_operacional,
        "impacto_seguranca": defeito.impacto_seguranca,
        "comite_sugerido": defeito.comite_sugerido,
        "responsavel": defeito.responsavel,
        "status": defeito.status
    }