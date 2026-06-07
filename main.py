from fastapi import FastAPI
from routers import auth, notes
from service import lifespan






# config = AuthXConfig()
app = FastAPI(lifespan=lifespan)

# config.JWT_SECRET_KEY = settings.secret_key
# config.JWT_ALGORITHM = settings.algorithm
# config.JWT_ACCESS_COOKIE_NAME = "access_token"
# config.JWT_TOKEN_LOCATION = ["cookies"]


app.include_router(auth.router)
app.include_router(notes.router)



# sequrity = AuthX(config = config)


