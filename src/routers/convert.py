from fastapi import APIRouter

from src.interfaces.address import AddressInfo

router = APIRouter()


@router.post("/convert/complete_and_divide_address", tags=["cinvert"])
async def health(request: list[AddressInfo]):  # type: ignore
    completed_count: int = 0
    for address_info in request:
        address_info.complete_address()
        address_info.normalize_address()
        address_info.divide_address()
        completed_count = address_info.get_completed_address_count(completed_count)
        address_info.delete_extra_attributes()

    return {"completed_count": completed_count, "addresses": request}
