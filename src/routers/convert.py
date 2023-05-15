from fastapi import APIRouter

from src.interfaces.address import Address

router = APIRouter()


@router.post("/convert/complete_and_divide_address", tags=["cinvert"])
async def health(request: list[Address]):  # type: ignore
    completed_count: int = 0
    for address in request:
        address.complete_address()
        address.normalize_address()
        address.divide_address()
        completed_count = address.get_completed_address_count(completed_count)
        address.delete_extra_attributes()

    return {"completed_count": completed_count, "addresses": request}
