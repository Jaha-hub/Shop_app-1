import uvicorn
from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.category.router import router as category_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(category_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


#User4_test