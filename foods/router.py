import io

from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter

from foods.dao import FoodsDAO
from foods.schemas import SFoods

router = APIRouter(prefix="/food", tags=["Foods"])


@router.post("/add_food/")
async def render_add_food(
    name: str, image: UploadFile,
    price: str, description: str, category_id: int
):
    image_data = image.file.read()
    await FoodsDAO.add(
        name = name, image=image_data,
        price=price, description=description, category_id=category_id
    )


@router.get("/foods_with_validation/", response_model=list[SFoods])
async def render_foods_with_validation():
    foods = await FoodsDAO.get_all_foods_with_category()
    return foods


@cache(expire=20)
async def get_foods():
    foods = await FoodsDAO.get_all_foods_with_category()
    sfood_list = [SFoods.model_validate(food) for food in foods]
    foods_json = TypeAdapter(list[SFoods]).validate_python(sfood_list)

    return foods_json


@router.get("/image_food/{id}")
async def get_image_food(id: int):
    food = await FoodsDAO.get_by_params(id=id)
    return StreamingResponse(io.BytesIO(food["Foods"].image), media_type="image/jpeg")
