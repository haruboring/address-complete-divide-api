from fastapi import APIRouter

router = APIRouter()


# health check
@router.get("/health", tags=["health"])
async def health():  # type: ignore
    return {"status": "ok"}
