import uvicorn
from fastapi import FastAPI
from .views.users import router as users_router
app = FastAPI(docs_url='/')
app.include_router(users_router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8462)
