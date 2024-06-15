from uuid import uuid4

from api.categoria.models import CategoriaModel
from api.categoria.schemas import CategoriaIn, CategoriaOut, CategoriaUpdate
from api.contrib.dependencies import DataBaseDependency
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select


router = APIRouter()


@router.get(
    path='/',
    summary='Consultar todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=Page[CategoriaOut],

)
async def query(db_session: DataBaseDependency) -> Page[CategoriaOut]:

    return await paginate(db_session, select(CategoriaModel))


@router.get(
    path='/{id}',
    summary='Consultar uma categoria por Id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def query(
    id: UUID4, 
    db_session: DataBaseDependency
) -> CategoriaOut:
    
    query = select(CategoriaModel).filter_by(id=id)
    
    result: CategoriaOut = (await db_session.execute(query)).scalars().first()
   
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoria não encontrada no Id: {id}')


    return result


@router.post(
    path='/',
    summary='Criar uma nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DataBaseDependency,
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    
    try:
        categoria_out = CategoriaOut(
            id=uuid4(), 
            **categoria_in.model_dump()
        )
        categoria_model = CategoriaModel(
            **categoria_out.model_dump()
        )
    
        db_session.add(categoria_model)

        await db_session.commit()

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe uma Categoria com o nome: {categoria_in.nome}'
        )
    
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir no banco de dados'
        )


    return categoria_out


@router.patch(
    path="/",
    summary="Editar uma categoria por Id",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def query(
    id: UUID4,
    db_session: DataBaseDependency,
    categoria_up: CategoriaUpdate = Body(...),
) -> CategoriaOut:
    
    query = select(CategoriaModel).filter_by(id=id)

    result: CategoriaOut = (await db_session.execute(query)).scalars().first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria não encontrada no Id: {id}",
        )

    categoria_up = categoria_up.model_dump(exclude_unset=True)
    for key, value in categoria_up.items():
        setattr(result, key, value)

    await db_session.commit()
    await db_session.refresh(result)


    return result


@router.delete(
    path="/{id}",
    summary="Deletar uma categoria por Id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> None:

    query = select(CategoriaModel).filter_by(id=id)

    result: CategoriaOut = (await db_session.execute(query)).scalars().first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria não encontrada no Id: {id}",
        )

    try:
        await db_session.delete(result)
        await db_session.commit()

    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Impossível deletar uma categoria que está relacionada a um atleta",
        )


    return None
