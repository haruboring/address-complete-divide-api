from fastapi import APIRouter

from src.interfaces.address import Address

router = APIRouter()


# health check
@router.post("/convert/divide_address", tags=["cinvert"])
async def health(request: list[Address]):  # type: ignore
    for address in request:
        address.complete_address()

    return request
