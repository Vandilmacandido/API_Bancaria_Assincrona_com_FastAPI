from fastapi import FastAPI
from .database import engine, Base
from .routes import auth, transactions

app = FastAPI(title="Banking API", description="Async configuration for banking operations", version="1.0.0")

@app.on_event("startup")
async def startup():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Banking API"}
