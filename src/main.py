from fastapi import FastAPI

app = FastAPI(title='WorkOutAPI')

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost/workout"

# Criar uma instância de engine para conectar ao banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criar uma instância de SessionLocal para trabalhar com sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarar uma base para declarar modelos SQLAlchemy
Base = declarative_base()



@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8080, log_level='info', reload=True)