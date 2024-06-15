from typing import Annotated

from api.contrib.schemas import BaseSchema
from pydantic import UUID4, Field


class Categoria(BaseSchema):

    nome: Annotated[
        str, Field(description="Nome da Categoria", example="Scale", max_length=10)
    ]


class CategoriaIn(Categoria):
    pass


class CategoriaOut(CategoriaIn):

    id: Annotated[UUID4, Field(description="Identificador da categoria")]


class CategoriaUpdate(BaseSchema):

    nome: Annotated[
        str, Field(description="Nome da Categoria", example="Scale", max_length=10)
    ]


class CategoriaAtleta(BaseSchema):

    nome: Annotated[
        str, Field(description="Nome da Categoria", example="Scale", max_length=10)
    ]
