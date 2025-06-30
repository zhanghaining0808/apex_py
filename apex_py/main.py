import uvicorn
from db.db import init_db
from controls.ctr_hero import hero_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(hero_router)

if __name__ == "__main__":
    init_db()
    uvicorn.run(
        "main:app",
        host="localhost",
        port=25357,
    )
