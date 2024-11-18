from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.factura import Factura
from app.schemas.incidente_factura import incidente_facturadoCreate, incidente_facturadoResponse
from app.crud.incidente_factura import create_incidente_facturado, get_incidente_by_id, get_incidentes_by_factura
from app.db.session import get_db
from typing import List

router = APIRouter()

@router.post("/incidentes", response_model=incidente_facturadoResponse)
def registrar_incidente(incidente: incidente_facturadoCreate, db: Session = Depends(get_db)):
    # Buscar la factura que corresponde a la fecha del incidente
    factura = db.query(Factura).filter(
        Factura.fecha_inicio <= incidente.fecha_incidente,
        Factura.fecha_fin >= incidente.fecha_incidente
    ).first()

    if not factura:
        raise HTTPException(status_code=404, detail="No se encontró una factura para la fecha proporcionada")

    # Crear el incidente facturado con el factura_id calculado
    incidente_facturado_data = {
        "radicado_incidente": incidente.radicado_incidente,
        "factura_id": factura.id,  # Usar el id de la factura encontrada
        "costo": incidente.costo,
        "fecha_incidente": incidente.fecha_incidente
    }

    return create_incidente_facturado(db=db, incidente=incidente_facturado_data)
    

@router.get("/incidentes/{id}", response_model=incidente_facturadoResponse)
def obtener_incidente(id: int, db: Session = Depends(get_db)):
    incidente = get_incidente_by_id(db, incidente_id=id)
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    return incidente

@router.get("/facturas/{factura_id}/incidentes", response_model=List[incidente_facturadoResponse])
def listar_incidentes_por_factura(factura_id: int, db: Session = Depends(get_db)):
    return get_incidentes_by_factura(db=db, factura_id=factura_id)
