from datetime import datetime
from typing import Optional
from uuid import uuid4

from api.atleta.models import AtletaModel
from api.atleta.schemas import AtletaGetAll, AtletaIn, AtletaOut, AtletaUpdate
from api.categoria.models import CategoriaModel
from api.categoria.schemas import CategoriaOut
from api.centro_treinamento.models import CentroTreinamentoModel
from api.centro_treinamento.schemas import CentroTreinamentoOut
from api.contrib.dependencies import DataBaseDependency
from fastapi import APIRouter, Body, HTTPException, Query, status
from fastapi_pagination import Page, paginate
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

router = APIRouter()


@router.get(
    path="/",
    summary="Consultar todos os atletas",
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaGetAll],
)
async def query(
    db_session: DataBaseDependency,
    cpf: Optional[str] = Query(None, description="Filtrar por CPF do atleta"),
    nome: Optional[str] = Query(None, description="Filtrar por nome do atleta"),
) -> Page[AtletaGetAll]:

    query = (
        select(
            AtletaModel.cpf.label("cpf"),
            AtletaModel.nome.label("atleta_nome"),
            CategoriaModel.nome.label("categoria_nome"),
            CentroTreinamentoModel.nome.label("centro_treinamento_nome"),
        )
        .join(CategoriaModel, AtletaModel.categoria_id == CategoriaModel.pk_id)
        .join(
            CentroTreinamentoModel,
            AtletaModel.centro_treinamento_id == CentroTreinamentoModel.pk_id,
        )
    )

    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

    if nome:
        query = query.filter(AtletaModel.nome == nome)

    result = (await db_session.execute(query)).fetchall()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Nenhum atleta encontrado"
        )

    # A row[0] corresponde ao CPF, então não é usada no retorno
    response_data = [
        AtletaGetAll(nome=row[1], nome_categoria=row[2], nome_centro_treinamento=row[3])
        for row in result
    ]

    return paginate(response_data)


@router.get(
    path="/{id}",
    summary="Consultar um atleta por Id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> AtletaOut:

    query = select(AtletaModel).filter_by(id=id)

    result: AtletaOut = (await db_session.execute(query)).scalars().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no Id: {id}"
        )

    return result


@router.post(
    path="/",
    summary="Criar um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(db_session: DataBaseDependency, atleta_in: AtletaIn = Body(...)) -> AtletaOut:

    nome_categoria = atleta_in.categoria.nome
    nome_centro_treinamento = atleta_in.centro_treinamento.nome

    query = select(CategoriaModel).filter_by(nome=nome_categoria)
    categoria: CategoriaOut = (await db_session.execute(query)).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria {nome_categoria} não foi encontrada",
        )

    query = select(CentroTreinamentoModel).filter_by(nome=nome_centro_treinamento)
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(query)).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento {nome_centro_treinamento} não foi encontrado",
        )

    created_at_naive = datetime.now().replace(tzinfo=None)

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=created_at_naive, **atleta_in.model_dump())
        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude=("categoria", "centro_treinamento"))
        )

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir no banco de dados",
        )

    return atleta_out


@router.patch(
    path="/{id}",
    summary="Editar um atleta por Id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(
    id: UUID4, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)
) -> AtletaOut:

    query = select(AtletaModel).filter_by(id=id)

    result: AtletaOut = (await db_session.execute(query)).scalars().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no id: {id}"
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(result, key, value)

    await db_session.commit()
    await db_session.refresh(result)

    return result


@router.delete(
    path="/{id}",
    summary="Deletar um atleta por Id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> None:

    query = select(AtletaModel).filter_by(id=id)

    result: AtletaOut = (await db_session.execute(query)).scalars().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no id: {id}"
        )

    try:
        await db_session.delete(result)
        await db_session.commit()

    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Erro ao deletar o atleta",
        )

    return None
