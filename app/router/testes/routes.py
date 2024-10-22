from fastapi import APIRouter

router = APIRouter()

@router.get("/data")
async def read_data():
    return {"message": "Hello from FastAPI!"}
