# 💠 WorkOutAPI

O WorkOutAPI é uma API desenvolvida em `Python` utilizando o framework `FastAPI` (async), juntamente com as libs: `SQLAlchemy`, `Alembic` e `Pydantic`. Já na parte de banco de dados, foi utilizado o `Postgres` localmente.


## 🔷 Instalação

### 🔹 Clone o repositório do projeto:
```bash
git clone https://github.com/FabricioDosSantosMoreira/WorkOutAPI.git
```

### 🔹 Navegue até o diretório do projeto:
```bash
cd WorkOutAPI/src
```

### 🔹 Instale as dependências do projeto:
❗ Caso não tenha o `Poetry`, use: 
```bash
pip install poetry
```
Instale as dependências via `Poetry`:
```bash
poetry shell
```
```bash
poetry install
```

### 🔹 Configure o Postgres:
Crie um novo banco de dados localmente usando o `Postgres`, ele deve conter:
- Usuário: postgres;
- Senha: 123456;
- Nome: workout;
- Host: localhost;
- Porta: 5432.

Ou, se preferir edite as váriaveis em `configs/settings.py`.


## 🔷 Execução da API
Utilize o `Make` para criar as migrações, rodar elas e subir a API:
```bash
make first-run
```
Com as migrações criadas, caso queira subir a API novamente, utilize:
```bash
make run
```

### 🔹 Rotas da API
A API possui as seguintes rotas principais:

- `/cts (Centros de Treinamento)`
- `/categorias (Categorias)`
- `/atletas (Atletas)`

Cada rota possui endpoints para as operações CRUD (Create, Read, Update, Delete) correspondentes.

### 🔹 Documentação da API
Você pode visualizar a documentação da API e testar as rotas interativamente via Swagger em `/docs`.
