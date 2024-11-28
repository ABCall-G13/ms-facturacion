from sqlalchemy.orm import Session
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate

def create_factura(db: Session, factura: FacturaCreate) -> Factura:
    nueva_factura = Factura(
        cliente_nit=factura.cliente_nit,
        fecha_inicio=factura.fecha_inicio,
        fecha_fin=factura.fecha_fin,
        monto_base=factura.monto_base,
        monto_adicional=factura.monto_adicional,
        monto_total=factura.monto_total,
        estado=factura.estado,
        cliente_id=factura.cliente_id
    )
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    return nueva_factura

def get_factura_by_id(db: Session, factura_id: int) -> Factura:
    return db.query(Factura).filter(Factura.id == factura_id).first()

def get_all_facturas(db: Session) -> list[Factura]:
    return db.query(Factura).all()


def get_facturas_by_cliente(db: Session, nit = str) -> list[Factura]:
    return db.query(Factura).filter(Factura.cliente_nit == nit).all()




