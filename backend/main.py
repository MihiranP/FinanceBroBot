from fastapi import FastAPI
from config.settings import settings
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
