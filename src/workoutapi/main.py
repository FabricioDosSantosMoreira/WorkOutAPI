from fastapi import FastAPI

app = FastAPI(title='WorkOutAPI')

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    import uvicorn

    port = 8080
    host = '127.0.0.1'

    uvicorn.run('main:app', host=host, port=port, log_level='info', reload=True)
