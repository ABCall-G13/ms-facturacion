from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class IncidenteFacturado(Base):
    __tablename__ = "incidentes_facturados"

    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    radicado_incidente = Column(String, nullable=False)
    costo = Column(Float, nullable=False)
    fecha_incidente = Column(Date, nullable=False)

    factura = relationship("Factura", back_populates="incidentes")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
