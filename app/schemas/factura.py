from pydantic import BaseModel
from datetime import date
from typing import List, Optional

from app.schemas.incidente_factura import incidente_facturadoResponse

class FacturaBase(BaseModel):
    cliente_nit: str
    fecha_inicio: date
    fecha_fin: date
    monto_base: float
    monto_adicional: Optional[float] = 0.0
    monto_total: float
    estado: Optional[str] = "pendiente"
    cliente_id: int
    
    
class FacturaCreate(FacturaBase):
    pass


class FacturaResponse(FacturaBase):
    id: int
    incidentes: List[incidente_facturadoResponse] = []

    class Config:
        orm_mode = True
