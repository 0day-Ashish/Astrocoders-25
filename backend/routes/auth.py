from fastapi import APIRouter

router = APIRouter()  # ← This must exist

@router.get("/login")
def login():
    return {"message": "Login endpoint"}