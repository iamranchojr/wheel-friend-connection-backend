from fastapi import FastAPI

from . import database
from .routers import user_router, auth_router, friend_router

# fast API instance
app = FastAPI(title='Friend Connection Backend')


# configure routing
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(friend_router)


@app.on_event('startup')
def on_startup():
    database.create_db_and_tables()


@app.get('/')
async def index():
    return {
        'message': 'Wheel Friend Connection Backend'
    }
