from typing import Any
from uuid import uuid4

from api.centro_treinamento.models import CentroTreinamentoModel
from api.centro_treinamento.schemas import (
    CentroTreinamentoIn,
    CentroTreinamentoOut,
    CentroTreinamentoUpdate,
)
from api.contrib.dependencies import DataBaseDependency
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

router = APIRouter()


@router.get(
    path="/",
    summary="Consultar todos os centros de treinamento",
    status_code=status.HTTP_200_OK,
    response_model=Page[CentroTreinamentoOut],
)
async def query(db_session: DataBaseDependency) -> Page[CentroTreinamentoOut]:

    return await paginate(db_session, select(CentroTreinamentoModel))


@router.get(
    path="/{id}",
    summary="Consultar um centro de treinamento por Id",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> CentroTreinamentoOut:

    query = select(CentroTreinamentoModel).filter_by(id=id)

    result: CentroTreinamentoOut = (await db_session.execute(query)).scalars().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de treinamento não encontrado no Id: {id}",
        )

    return result


@router.post(
    path="/",
    summary="Criar um novo Centro de treinmamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DataBaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:

    try:
        centro_treinamento_out = CentroTreinamentoOut(
            id=uuid4(), **centro_treinamento_in.model_dump()
        )
        centro_treinamento_model = CentroTreinamentoModel(
            **centro_treinamento_out.model_dump()
        )

        db_session.add(centro_treinamento_model)

        await db_session.commit()

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um centro de treinamento com o nome: {centro_treinamento_in.nome}",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir no banco de dados",
        )

    return centro_treinamento_out


@router.patch(
    path="/",
    summary="Editar um centro de treinamento por Id",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def query(
    id: UUID4,
    db_session: DataBaseDependency,
    centro_treinamento_up: CentroTreinamentoUpdate = Body(...),
) -> CentroTreinamentoOut:

    query = select(CentroTreinamentoModel).filter_by(id=id)

    result: CentroTreinamentoOut = (await db_session.execute(query)).scalars().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de treinamento não encontrado no Id: {id}",
        )

    centro_treinamento_up = centro_treinamento_up.model_dump(exclude_unset=True)
    for key, value in centro_treinamento_up.items():
        setattr(result, key, value)

    await db_session.commit()
    await db_session.refresh(result)

    return result


@router.delete(
    path="/{id}",
    summary="Deletar um centro de treinamento por Id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> None:

    query = select(CentroTreinamentoModel).filter_by(id=id)

    result: CentroTreinamentoOut = (await db_session.execute(query)).scalars().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de treinamento não encontrado no Id: {id}",
        )

    try:
        await db_session.delete(result)
        await db_session.commit()

    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Impossível deletar um centro de treinamento que está relacionado a um atleta",
        )

    return None
