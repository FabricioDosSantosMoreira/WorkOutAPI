from fastapi import APIRouter

from api.atleta.controller import router as atleta
from api.categoria.controller import router as categoria
from api.centro_treinamento.controller import router as ct


api_router = APIRouter()
api_router.include_router(ct, prefix='/cts', tags=['cts/'])
api_router.include_router(categoria, prefix='/categorias', tags=['categorias/'])
api_router.include_router(atleta, prefix='/atletas', tags=['atletas/'])
