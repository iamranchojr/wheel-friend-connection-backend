from fastapi import FastAPI

from . import database


# fast API instance
app = FastAPI()


@app.on_event('startup')
def on_startup():
    database.create_db_and_tables()


@app.get('/')
async def root():
    return {
        'message': 'Wheel Friend Connection Backend'
    }
