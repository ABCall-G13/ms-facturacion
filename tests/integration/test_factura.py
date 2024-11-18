import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_factura.db"
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

def test_create_factura(client):
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
    assert response.status_code == 200
    assert response.json()["cliente_nit"] == factura_data["cliente_nit"]

def test_listar_facturas(client):
    factura_1 = {
        "cliente_nit": "123456789",
        "fecha_inicio": "2024-01-01",
        "fecha_fin": "2024-01-31",
        "monto_base": 100.0,
        "monto_adicional": 20.0,
        "monto_total": 120.0,
        "estado": "pendiente"
    }
    factura_2 = {
        "cliente_nit": "987654321",
        "fecha_inicio": "2024-02-01",
        "fecha_fin": "2024-02-28",
        "monto_base": 200.0,
        "monto_adicional": 50.0,
        "monto_total": 250.0,
        "estado": "pagada"
    }
    client.post("/facturas", json=factura_1)
    client.post("/facturas", json=factura_2)

    response = client.get("/facturas")
    assert response.status_code == 200
    facturas = response.json()
    assert len(facturas) == 2
    assert facturas[0]["cliente_nit"] == factura_1["cliente_nit"]
    assert facturas[1]["cliente_nit"] == factura_2["cliente_nit"]

def test_obtener_factura_por_id(client):
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

    response = client.get(f"/facturas/{factura_id}")
    assert response.status_code == 200
    assert response.json()["cliente_nit"] == factura_data["cliente_nit"]

def test_descargar_factura(client):
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

    response = client.get(f"/facturas/{factura_id}/download")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
