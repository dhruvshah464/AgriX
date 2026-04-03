from pydantic import BaseModel


class Farm(BaseModel):
    farm_id: str
    area_hectares: float
