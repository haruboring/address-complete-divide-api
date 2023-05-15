from fastapi import APIRouter

from src.interfaces.address import Address

router = APIRouter()


@router.post("/convert/divide_and_complete_address", tags=["cinvert"])
async def health(request: list[Address]):  # type: ignore
    for address in request:
        address.complete_address()
        address.divide_address()
        address.delete_extra_attributes()

    return request
