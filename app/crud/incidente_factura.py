from sqlalchemy.orm import Session
from app.models.incidente_factura import IncidenteFacturado


def create_incidente_facturado(db: Session, incidente: dict) -> IncidenteFacturado:
    nuevo_incidente = IncidenteFacturado(
        radicado_incidente=incidente["radicado_incidente"],
        factura_id=incidente["factura_id"],
        costo=incidente["costo"],
        fecha_incidente=incidente["fecha_incidente"],
    )
    db.add(nuevo_incidente)
    db.commit()
    db.refresh(nuevo_incidente)
    return nuevo_incidente

def get_incidente_by_id(db: Session, incidente_id: int) -> IncidenteFacturado:
    return db.query(IncidenteFacturado).filter(IncidenteFacturado.id == incidente_id).first()

def get_incidentes_by_factura(db: Session, factura_id: int) -> list[IncidenteFacturado]:
    return db.query(IncidenteFacturado).filter(IncidenteFacturado.factura_id == factura_id).all()
