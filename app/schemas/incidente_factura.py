from pydantic import BaseModel
from datetime import date


class incidente_facturadoBase(BaseModel):
    radicado_incidente: str
    costo: float
    fecha_incidente: date
    cliente_id: int

class incidente_facturadoCreate(incidente_facturadoBase):
    pass

class incidente_facturadoResponse(incidente_facturadoBase):
    id: int

    class Config:
        orm_mode = True