from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware              # For CORS

from .routers import post, user, auth, vote



# from .config import settings                      When we moved out the settings to env/config, this is no longer needed

# -- This is ORM way: But more to the point: It used to tell SQLAlchemy that it needs to create the tables found in models.py!
# Now that we have tied in alembic, we do not need this functionality.
# from . import models
# from .database import engine
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]                # for public APIs it can be "*"

app.add_middleware(                                 # Added for CORS demonstration
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# -- This is the RAW SQL way
# while True:                                 # Keep on trying connection, until we get one! Dumb approach?
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='pgadmin', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print(f'Connecting to database failed. Error: {error}')
#         time.sleep(2)


@app.get("/")                               # this is a decorator, that changes the function into a path operation
def root():
    return {"message": "Hello there, World!"}       # python dictionary returned converted as JSON by fastapi
