from datetime import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    HttpUrl,
    PositiveInt,
    computed_field,
)

from memesapi.config import config


class MemeCreate(BaseModel):
    id: int
    image_name: str
    text: str
    created_at: datetime

    model_config = {'from_attributes': True}

    def model_post_init(self, __context):
        # simplify image_name for user
        self.image_name = str(self.image_name).split('_', maxsplit=1)[1]


class MemeRead(MemeCreate):
    @computed_field
    @property
    def image_link(self) -> HttpUrl:
        return HttpUrl(f'{config.main_server_url}memes/{self.id}/image')


class OrderByEnum(str, Enum):
    id = 'id'
    image_name = 'image_name'
    text = 'text'
    created_at = 'created_at'


class Pagination(BaseModel):
    limit: PositiveInt = 10
    page: int = 1
    order_by: OrderByEnum = OrderByEnum.id
