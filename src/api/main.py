from fastapi import FastAPI
from fastapi_pagination import add_pagination

from api.routers import api_router

app = FastAPI(title="WorkOutAPI")
app.include_router(api_router)
add_pagination(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8080, log_level="info", reload=True)
