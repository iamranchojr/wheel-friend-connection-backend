from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from . import database
from .config import settings
from .routers import user_router, auth_router, friend_router, websocket_router

# fast API instance
app = FastAPI(title='Friend Connection Backend')

cors_allowed_origins = [
    'http://localhost',
    'http://localhost:3000',
    'https://wfc-app-a07cd74c45cb.herokuapp.com',
]

# apply cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if settings.SECURE_SSL_REDIRECT:
    # apply redirect to https middleware
    app.add_middleware(HTTPSRedirectMiddleware)

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            'wfc-backend-api-8bd958c0167d.herokuapp.com',
            '*.wfc-backend-api-8bd958c0167d.herokuapp.com',
        ]
    )

# configure routing
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(friend_router)
app.include_router(websocket_router)


@app.on_event('startup')
def on_startup():
    database.init_db()


@app.get('/')
async def index():
    return {
        'message': 'Wheel Friend Connection Backend'
    }
