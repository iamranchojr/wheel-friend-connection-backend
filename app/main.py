from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import database
from .routers import user_router, auth_router, friend_router, websocket_router

# fast API instance
app = FastAPI(title='Friend Connection Backend')

cors_allowed_origins = [
    'http://localhost',
    'http://localhost:3000',
]

# apply cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# configure routing
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(friend_router)
app.include_router(websocket_router)


@app.on_event('startup')
def on_startup():
    database.create_db_and_tables()


@app.get('/')
async def index():
    return {
        'message': 'Wheel Friend Connection Backend'
    }
