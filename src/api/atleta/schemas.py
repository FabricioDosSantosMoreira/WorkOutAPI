from typing import Annotated

from api.categoria.schemas import CategoriaAtleta
from api.centro_treinamento.schemas import CentroTreinamentoAtleta
from api.contrib.schemas import BaseSchema, OutMixin
from pydantic import Field, PositiveFloat


class Atleta(BaseSchema):

    nome: Annotated[str, Field(description="Nome do atleta", example="Fabrício", max_length=50)]
    idade: Annotated[int, Field(description="Idade do atleta", example="19")]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example="1.78")]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example="75.5")]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="12345678900", max_length=11)]

    categoria: Annotated[CategoriaAtleta, Field(description="Categoria do atleta")]

    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]


class AtletaIn(Atleta):
    pass


class AtletaOut(AtletaIn, OutMixin):
    pass


class AtletaUpdate(BaseSchema):

    nome: Annotated[str, Field(description="Nome do atleta", example="Fabrício", max_length=50)]
    idade: Annotated[int, Field(description="Idade do atleta", example="19")]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example="1.78")]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example="75.5")]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]


class AtletaGetAll(BaseSchema):

    nome: Annotated[str, Field(description="Nome do atleta", example="Anya")]

    nome_categoria: Annotated[str, Field(description="Nome da categoria", example="Scale")]
    nome_centro_treinamento: Annotated[str, Field(description="Nome do centro de treinamento", example="Ct King")]
