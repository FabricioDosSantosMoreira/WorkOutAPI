from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status

from pydantic import UUID4
from workoutapi.centro_treinamento.models import CentroTreinamentoModel
from workoutapi.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut


from workoutapi.contrib.dependencies import DataBaseDependency

from sqlalchemy.future import select

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page


router = APIRouter()


@router.post(
        path='/',
        summary='Criar um novo Centro de treinmamento',
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut,

)
async def post(
    db_session: DataBaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    
    try:
        centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
        
        db_session.add(centro_treinamento_model)
        await db_session.commit()

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um centro de treinamento com o nome: {centro_treinamento_in.nome}'
        )
    
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir os dados no banco'
        )


    return centro_treinamento_out




@router.get(
        path='/',
        summary='Consultar todas os centros de treinamento',
        status_code=status.HTTP_200_OK,
        response_model=Page[CentroTreinamentoOut],

)
async def query(db_session: DataBaseDependency) -> Page[CentroTreinamentoOut]:
    
    return await paginate(db_session, select(CentroTreinamentoModel))


    
    
    #centros_treinamentos: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
   
    #return centros_treinamentos




@router.get(
        path='/{id}',
        summary='Consultar um centro de treinamento',
        status_code=status.HTTP_200_OK,
        response_model=CentroTreinamentoOut,

)
async def query(id: UUID4, db_session: DataBaseDependency) -> CentroTreinamentoOut:
    centros_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
   
    if not centros_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado no id: {id}')


    return centros_treinamento


