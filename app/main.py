from fastapi import FastAPI
from app.routes.cats_routes import router as cats
from app.routes.missions_routes import router as missions

app = FastAPI()
app.include_router(router=cats)
app.include_router(router=missions)


@app.get("/")
async def echo(message: str = "FastAPI App 'SpyCats'"):
    return {"message": message}
