from fastapi import FastAPI
from routers import auth, notes
from service import lifespan
from fastapi.middleware import CORSMiddleware






app = FastAPI(lifespan=lifespan)


app.include_router(auth.router)
app.include_router(notes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

