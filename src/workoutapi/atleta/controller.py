from fastapi import APIRouter, Body, status

from workoutapi.atleta.schemas import AtletaIn
from workoutapi.contrib.dependencies import DataBaseDependency


router = APIRouter()


@router.post(
        path='/',
        summary='Criar novo atleta',
        status_code=status.HTTP_201_CREATED

)
async def post(
    db_session: DataBaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    pass