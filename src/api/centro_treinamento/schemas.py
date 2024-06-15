from typing import Annotated

from api.contrib.schemas import BaseSchema
from pydantic import UUID4, Field


class CentroTreinamento(BaseSchema):

    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            example="CT Example",
            max_length=20,
        ),
    ]
    endereco: Annotated[
        str,
        Field(
            description="Endereço do centro de treinamento",
            example="Rua X, Q00",
            max_length=60,
        ),
    ]
    proprietario: Annotated[
        str,
        Field(
            description="Proprietário do centro de treinamento",
            example="Roberto",
            max_length=30,
        ),
    ]


class CentroTreinamentoIn(CentroTreinamento):
    pass


class CentroTreinamentoOut(CentroTreinamentoIn):

    id: Annotated[UUID4, Field(description="Identificador do centro de treinamento")]


class CentroTreinamentoUpdate(BaseSchema):

    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            example="CT Example",
            max_length=20,
        ),
    ]
    endereco: Annotated[
        str,
        Field(
            description="Endereço do centro de treinamento",
            example="Rua X, Q00",
            max_length=60,
        ),
    ]
    proprietario: Annotated[
        str,
        Field(
            description="Proprietário do centro de treinamento",
            example="Roberto",
            max_length=30,
        ),
    ]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            example="CT Example",
            max_length=20,
        ),
    ]
