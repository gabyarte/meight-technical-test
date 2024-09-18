from math import isnan
from typing import Optional
from pydantic import BaseModel, field_validator


class NaNToNoneBaseModel(BaseModel):
    @field_validator('*', mode='before')
    def change_nan_to_none(cls, v, info):
        if str(v) == 'nan':
            return None
        return v


class APIResponse(NaNToNoneBaseModel):
    service_type: Optional[str]
    pickup_coordinate: Optional[str]
    delivery_coordinate: Optional[str]
    price: Optional[float]
    trailer_type: Optional[str]
