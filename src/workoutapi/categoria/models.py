from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from workoutapi.contrib.models import BaseModel


class CategoriaModel(BaseModel):
    _tablename__ = 'categorias'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(11), nullable=False)