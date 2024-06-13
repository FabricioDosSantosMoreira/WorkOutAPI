from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status

from datetime import datetime, UTC
from workoutapi.atleta.models import AtletaModel
from workoutapi.atleta.schemas import AtletaIn, AtletaOut
from workoutapi.categoria.models import CategoriaModel
from workoutapi.centro_treinamento.models import CentroTreinamentoModel
from workoutapi.contrib.dependencies import DataBaseDependency

from sqlalchemy.future import select


router = APIRouter()


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
    except Exception: # a manipulação vai ser aq
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir os dados no banco'
        )

    return atleta_out
    