import os
import tempfile
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.schemas.factura import FacturaCreate, FacturaResponse
from app.crud.factura import create_factura, get_factura_by_id, get_all_facturas
from app.db.session import get_db
from typing import List

from app.utils.pdf_generator import generar_pdf_factura

router = APIRouter()

@router.post("/facturas", response_model=FacturaResponse)
def registrar_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    try:
        return create_factura(db=db, factura=factura)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/facturas", response_model=List[FacturaResponse])
def listar_facturas(db: Session = Depends(get_db)):
    return get_all_facturas(db)

@router.get("/facturas/{id}", response_model=FacturaResponse)
def obtener_factura_por_id(id: int, db: Session = Depends(get_db)):
    factura = get_factura_by_id(db, factura_id=id)
    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@router.get("/facturas/{factura_id}/download", response_class=FileResponse)
def descargar_factura_pdf(factura_id: int, db: Session = Depends(get_db)):

    try:
        factura = get_factura_by_id(db, factura_id)
        if not factura:
            raise HTTPException(status_code=404, detail="Factura no encontrada")

        with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as temp_pdf:
            pdf_path = temp_pdf.name

        generar_pdf_factura(factura_id, db, pdf_path)
        
        response = FileResponse(
            path=pdf_path,
            filename=f"factura_{factura_id}.pdf",
            media_type="application/pdf"
        )

        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
