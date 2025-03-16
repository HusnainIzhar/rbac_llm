from typing import Union
from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.admin import router as admin_router
from app.controllers.llm_controller import router as llm_router
from app.routes.rag import router as rag_router

app = FastAPI()

# Include routers from separate route files
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(llm_router)
app.include_router(rag_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
