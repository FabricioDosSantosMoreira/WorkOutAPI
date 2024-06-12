from fastapi import FastAPI

app = FastAPI(title='WorkOutAPI')

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8080, log_level='info', reload=True)
