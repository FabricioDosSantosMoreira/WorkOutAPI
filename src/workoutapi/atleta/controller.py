from typing import Any, List, Optional
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


from datetime import datetime, UTC
from pydantic import UUID4
from workoutapi.atleta.models import AtletaModel
from workoutapi.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaGetAll
from workoutapi.categoria.models import CategoriaModel
from workoutapi.centro_treinamento.models import CentroTreinamentoModel
from workoutapi.contrib.dependencies import DataBaseDependency

from sqlalchemy.future import select
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page


router = APIRouter()





@router.get(
    path='/',
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model= Any
) 
async def query(
    request: Request,
    db_session: DataBaseDependency,
    cpf: Optional[str] = Query(None, description='Filtrar por CPF do Atleta'),
    nome: Optional[str] = Query(None, description='Filtrar por nome do Atleta')
)-> Any:
    
    query = select(AtletaModel)

    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

    if nome:
        query = query.filter(AtletaModel.nome == nome)

    atletas = (await db_session.execute(query)).scalars().all()

    if not atletas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Nenhum atleta encontrado com os critérios fornecidos'
        )
    
    response_data = [
        {
            "id": str(atleta.id),  
            "created_at": atleta.created_at.isoformat(),  
            "nome": atleta.nome,
            "centro_treinamento": atleta.centro_treinamento.nome,
            "categoria": atleta.categoria.nome
        }
        for atleta in atletas
    ]
    
    return JSONResponse(content=response_data)
   
















@router.post(
        path='/',
        summary='Criar um novo atleta',
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaOut

)
async def post(
    db_session: DataBaseDependency,
    atleta_in: AtletaIn = Body(...)
):  
    categoria_name = atleta_in.categoria.nome
    centro_treinamento_name = atleta_in.centro_treinamento.nome


    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_name))
    ).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_name} não foi encontarada'
        )  
    
    centro_treinamento = (await db_session.execute(
            select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_name))
    ).scalars().first()
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_name} não foi encontarado'
        )

    created_at_naive = datetime.now().replace(tzinfo=None)

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=created_at_naive, **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude=('categoria', 'centro_treinamento')))

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}'
        )
    
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir os dados no banco'
        )

    return atleta_out



@router.get(
    path='/all',
    summary='Consultar todos os Atletas com paginação',
    status_code=status.HTTP_200_OK,
    response_model= Page[AtletaGetAll]
) 
async def query(
    request: Request,
    db_session: DataBaseDependency,
    cpf: Optional[str] = Query(None, description='Filtrar por CPF do Atleta'),
    nome: Optional[str] = Query(None, description='Filtrar por nome do Atleta')
)-> Page[AtletaGetAll]:
    
    query = select(AtletaModel)

    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

    if nome:
        query = query.filter(AtletaModel.nome == nome)

    return await paginate(db_session, query)




@router.get(
        path='/{id}',
        summary='Consultar um Atleta por id',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
   
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')


    return atleta






@router.patch(
        path='/{id}',
        summary='Editar um Atleta por id',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
   
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')

    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    

    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta




@router.delete(
        path='/{id}',
        summary='Deletar um Atleta por id',
        status_code=status.HTTP_204_NO_CONTENT,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
   
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')

    await db_session.delete(atleta)
    await db_session.commit()