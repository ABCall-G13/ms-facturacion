from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.incidente_factura import IncidenteFacturado  # Importar la clase relacionada

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_nit = Column(String, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    monto_base = Column(Float, nullable=False)
    monto_adicional = Column(Float, default=0.0)
    monto_total = Column(Float, nullable=False)
    estado = Column(String(50), default="pendiente")
    pdf_url = Column(String(255))

    # Relación con IncidenteFacturado
    incidentes = relationship(
        "IncidenteFacturado",  # Nombre del modelo como cadena
        back_populates="factura",
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
