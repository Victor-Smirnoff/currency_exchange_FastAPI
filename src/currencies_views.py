from typing import Annotated
from fastapi import APIRouter, Form, Path

router = APIRouter(tags=["currencies"])


@router.get("/currencies")
async def currencies():
    return ["list all currencies"]


@router.post("/currencies")
async def currencies(
    name: Annotated[str, Form(..., min_length=3, max_length=30)],
    code: Annotated[str, Form(..., min_length=3, max_length=3)],
    sign: Annotated[str, Form(..., min_length=1, max_length=5)],
):
    return {"name": name, "code": code, "sign": sign}


@router.get("/currency/{code}")
async def currency(code: Annotated[str, Path(min_length=3, max_length=3)]):
    return {"currency": code}
