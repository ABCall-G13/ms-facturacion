from datetime import date
import os
import tempfile

from fastapi import HTTPException
from fastapi.responses import FileResponse
from app.crud.factura import get_factura_by_id
from app.db.base import Base
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.models.factura import Factura
from app.models.incidente_factura import IncidenteFacturado
from app.utils.pdf_generator import generar_pdf_factura

@pytest.fixture(scope='module')
def db_engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def db_session(db_engine):
    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()

    Base.metadata.drop_all(bind=db_engine)
    Base.metadata.create_all(bind=db_engine)

    try:
        yield session
    finally:
        session.close()
