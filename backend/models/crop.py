from pydantic import BaseModel


class Crop(BaseModel):
    crop_id: str
    name: str
