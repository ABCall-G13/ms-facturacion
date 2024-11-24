import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_incidente_facturado.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    app.dependency_overrides[get_db] = lambda: session
    yield TestClient(app)
    app.dependency_overrides = {}

def test_create_incidente_facturado(client):
    # Crear una factura
    factura_data = {
        "cliente_nit": "123456789",
        "fecha_inicio": "2024-01-01",
        "fecha_fin": "2024-01-31",
        "monto_base": 100.0,
        "monto_adicional": 20.0,
        "monto_total": 120.0,
        "estado": "pendiente"
    }
    client.post("/facturas", json=factura_data)

    # Crear un incidente relacionado
    incidente_data = {
        "radicado_incidente": "RAD-001",
        "costo": 50.0,
        "fecha_incidente": "2024-01-15",
        "nit": "123456789"  # Agregar el NIT necesario para la búsqueda de la factura
    }
    response = client.post("/incidentes", json=incidente_data)
    assert response.status_code == 200
    assert response.json()["radicado_incidente"] == incidente_data["radicado_incidente"]


def test_listar_incidentes_por_factura(client):
    # Crear una factura
    factura_data = {
        "cliente_nit": "123456789",
        "fecha_inicio": "2024-01-01",
        "fecha_fin": "2024-01-31",
        "monto_base": 100.0,
        "monto_adicional": 20.0,
        "monto_total": 120.0,
        "estado": "pendiente"
    }
    response = client.post("/facturas", json=factura_data)
    factura_id = response.json()["id"]

    # Crear incidentes relacionados con la factura
    incidente_1 = {
        "radicado_incidente": "RAD-002",
        "costo": 60.0,
        "fecha_incidente": "2024-01-15",
        "nit": "123456789"  # Agregar el NIT necesario para la búsqueda de la factura
    }
    incidente_2 = {
        "radicado_incidente": "RAD-003",
        "costo": 30.0,
        "fecha_incidente": "2024-01-20",
        "nit": "123456789"  # Agregar el NIT necesario para la búsqueda de la factura
    }
    client.post("/incidentes", json=incidente_1)
    client.post("/incidentes", json=incidente_2)

    # Listar los incidentes por factura
    response = client.get(f"/facturas/{factura_id}/incidentes")
    assert response.status_code == 200
    incidentes = response.json()
    assert len(incidentes) == 2
    assert incidentes[0]["radicado_incidente"] == "RAD-002"
    assert incidentes[1]["radicado_incidente"] == "RAD-003"
