from sqlalchemy.orm import Session
from app.models.incidente_factura import IncidenteFacturado


def create_incidente_facturado(db: Session, incidente: dict) -> IncidenteFacturado:
    nuevo_incidente = IncidenteFacturado(
        radicado_incidente=incidente["radicado_incidente"],
        factura_id=incidente["factura_id"],
        costo=incidente["costo"],
        fecha_incidente=incidente["fecha_incidente"],
        cliente_id=incidente["cliente_id"]
    )
    db.add(nuevo_incidente)
    db.commit()
    db.refresh(nuevo_incidente)
    return nuevo_incidente

def get_incidente_by_id(db: Session, incidente_id: int) -> IncidenteFacturado:
    return db.query(IncidenteFacturado).filter(IncidenteFacturado.id == incidente_id).first()

def get_incidentes_by_factura(db: Session, factura_id: int, currency: str = "COP") -> list[IncidenteFacturado]:
    incidentes = db.query(IncidenteFacturado).filter(IncidenteFacturado.factura_id == factura_id).all()
    
    tasa_conversion = 4000

    for incidente in incidentes:
        if currency == "USD":
            incidente.costo = round(incidente.costo / tasa_conversion, 2)

    return incidentes