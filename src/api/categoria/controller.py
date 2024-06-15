from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from api.categoria.models import CategoriaModel
from api.categoria.schemas import CategoriaIn, CategoriaOut

from api.contrib.dependencies import DataBaseDependency

from sqlalchemy.future import select


from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page


router = APIRouter()


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
        categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
        categoria_model = CategoriaModel(**categoria_out.model_dump())
    
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
            detail=f'Ocorreu um erro ao inserir os dados no banco'
        )

    return categoria_out












@router.get(
        path='/',
        summary='Consultar todas as Categorias',
        status_code=status.HTTP_200_OK,
        response_model=Page[CategoriaOut],

)
async def query(db_session: DataBaseDependency) -> Page[CategoriaOut]:

    return await paginate(db_session, select(CategoriaModel))



    #categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
   
    #return categorias


@router.get(
        path='/{id}',
        summary='Consultar uma Categoria',
        status_code=status.HTTP_200_OK,
        response_model=CategoriaOut,

)
async def query(id: UUID4, db_session: DataBaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
   
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoria não encontrada no id: {id}')


    return categoria