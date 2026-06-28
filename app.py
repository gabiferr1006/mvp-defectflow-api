from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from model import Session, Defeito
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="DefectFlow API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc"
)

defeito_tag = Tag(
    name="Defeito",
    description="Cadastro, consulta, atualização e remoção de defeitos"
)


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/defeito', tags=[defeito_tag],
          responses={"200": DefeitoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_defeito(form: DefeitoSchema):
    """Adiciona um novo Defeito à base de dados.

    Esta rota cadastra um defeito, calcula automaticamente o comitê sugerido
    com base na severidade e no impacto de segurança, e retorna o registro criado.
    """
    defeito = Defeito(
        titulo=form.titulo,
        descricao=form.descricao,
        origem=form.origem,
        componente=form.componente,
        categoria=form.categoria,
        severidade=form.severidade,
        impacto_operacional=form.impacto_operacional,
        impacto_seguranca=form.impacto_seguranca,
        responsavel=form.responsavel,
        status=form.status
    )

    logger.debug(f"Adicionando defeito de título: '{defeito.titulo}'")
    session = Session()

    try:
        session.add(defeito)
        session.commit()

        logger.debug(f"Defeito adicionado: '{defeito.titulo}'")
        return apresenta_defeito(defeito), 200

    except IntegrityError:
        session.rollback()
        error_msg = "Defeito com o mesmo título já cadastrado na base."
        logger.warning(f"Erro ao adicionar defeito '{defeito.titulo}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception:
        session.rollback()
        error_msg = "Não foi possível salvar o novo defeito."
        logger.warning(f"Erro ao adicionar defeito '{defeito.titulo}', {error_msg}")
        return {"message": error_msg}, 400

    finally:
        session.close()


@app.get('/defeitos', tags=[defeito_tag],
         responses={"200": ListagemDefeitosSchema, "404": ErrorSchema})
def get_defeitos():
    """Faz a busca por todos os defeitos cadastrados.

    Retorna uma lista com os defeitos registrados na base.
    """
    logger.debug("Coletando defeitos cadastrados")
    session = Session()

    try:
        defeitos = session.query(Defeito).all()

        if not defeitos:
            return {"defeitos": []}, 200

        logger.debug(f"{len(defeitos)} defeito(s) encontrado(s)")
        return apresenta_defeitos(defeitos), 200

    finally:
        session.close()


@app.get('/defeito', tags=[defeito_tag],
         responses={"200": DefeitoViewSchema, "404": ErrorSchema})
def get_defeito(query: DefeitoBuscaSchema):
    """Faz a busca por um defeito a partir do ID.

    Retorna os dados de um defeito específico cadastrado na base.
    """
    defeito_id = query.id
    logger.debug(f"Coletando dados do defeito ID: {defeito_id}")
    session = Session()

    try:
        defeito = session.query(Defeito).filter(Defeito.id == defeito_id).first()

        if not defeito:
            error_msg = "Defeito não encontrado na base."
            logger.warning(f"Erro ao buscar defeito ID {defeito_id}, {error_msg}")
            return {"message": error_msg}, 404

        logger.debug(f"Defeito encontrado ID: {defeito.id}")
        return apresenta_defeito(defeito), 200

    finally:
        session.close()


@app.put('/defeito', tags=[defeito_tag],
         responses={"200": DefeitoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_defeito(form: DefeitoUpdateSchema):
    """Atualiza o status de um defeito a partir do ID informado.

    Retorna os dados atualizados do defeito.
    """
    defeito_id = form.id
    novo_status = form.status

    logger.debug(f"Atualizando defeito ID {defeito_id} para status: {novo_status}")
    session = Session()

    try:
        defeito = session.query(Defeito).filter(Defeito.id == defeito_id).first()

        if not defeito:
            error_msg = "Defeito não encontrado na base."
            logger.warning(f"Erro ao atualizar defeito ID {defeito_id}, {error_msg}")
            return {"message": error_msg}, 404

        defeito.status = novo_status
        session.commit()

        logger.debug(f"Status do defeito ID {defeito_id} atualizado para: {novo_status}")
        return apresenta_defeito(defeito), 200

    except Exception:
        session.rollback()
        error_msg = "Não foi possível atualizar o status do defeito."
        logger.warning(f"Erro ao atualizar defeito ID {defeito_id}, {error_msg}")
        return {"message": error_msg}, 400

    finally:
        session.close()


@app.delete('/defeito', tags=[defeito_tag],
            responses={"200": DefeitoDelSchema, "404": ErrorSchema})
def del_defeito(query: DefeitoBuscaSchema):
    """Deleta um defeito a partir do ID informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    defeito_id = query.id
    logger.debug(f"Deletando defeito ID: {defeito_id}")
    session = Session()

    try:
        count = session.query(Defeito).filter(Defeito.id == defeito_id).delete()
        session.commit()

        if count:
            logger.debug(f"Defeito deletado ID: {defeito_id}")
            return {"message": "Defeito removido", "id": defeito_id}, 200

        error_msg = "Defeito não encontrado na base."
        logger.warning(f"Erro ao deletar defeito ID {defeito_id}, {error_msg}")
        return {"message": error_msg}, 404

    except Exception:
        session.rollback()
        error_msg = "Não foi possível deletar o defeito."
        logger.warning(f"Erro ao deletar defeito ID {defeito_id}, {error_msg}")
        return {"message": error_msg}, 400

    finally:
        session.close()