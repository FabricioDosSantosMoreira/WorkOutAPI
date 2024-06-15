from typing import Annotated

from api.configs.database import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


DataBaseDependency = Annotated[AsyncSession, Depends(get_session)]
