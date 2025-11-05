import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from .dependencies.database import Base, engine


app = FastAPI(title="SoftDash Linear Input Maintenance Exporter (SLIME)")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
Base.metadata.create_all(bind=engine)
indexRoute.load_routes(app)

@app.get("/")
def root():
    return {"message": "Welcome to the SLIME API"}


if __name__ == "__main__":
    uvicorn.run("api.main:app", host=conf.app_host, port=conf.app_port, reload=True)