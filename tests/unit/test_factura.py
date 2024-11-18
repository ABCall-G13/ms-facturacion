import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.schemas.factura import FacturaCreate
from app.crud.factura import create_factura, get_all_facturas, get_factura_by_id

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


def test_create_factura(db_session):
    factura_data = FacturaCreate(
        cliente_nit="123456789",
        fecha_inicio="2024-01-01",
        fecha_fin="2024-01-31",
        monto_base=100.0,
        monto_adicional=20.0,
        monto_total=120.0,
        estado="pendiente"
    )

    factura = create_factura(db_session, factura_data)

    assert factura.cliente_nit == factura_data.cliente_nit
    assert factura.fecha_inicio.isoformat() == factura_data.fecha_inicio.isoformat()
    assert factura.fecha_fin.isoformat() == factura_data.fecha_fin.isoformat() 
    assert factura.monto_total == factura_data.monto_total


def test_get_all_facturas(db_session):
    # Crear varias facturas
    factura_1 = FacturaCreate(
        cliente_nit="123456789",
        fecha_inicio="2024-01-01",
        fecha_fin="2024-01-31",
        monto_base=100.0,
        monto_adicional=20.0,
        monto_total=120.0,
        estado="pendiente"
    )
    factura_2 = FacturaCreate(
        cliente_nit="987654321",
        fecha_inicio="2024-02-01",
        fecha_fin="2024-02-28",
        monto_base=200.0,
        monto_adicional=50.0,
        monto_total=250.0,
        estado="pagada"
    )
    create_factura(db_session, factura_1)
    create_factura(db_session, factura_2)

    # Obtener todas las facturas
    facturas = get_all_facturas(db_session)
    assert len(facturas) == 2
    assert facturas[0].cliente_nit == factura_1.cliente_nit
    assert facturas[1].cliente_nit == factura_2.cliente_nit


def test_get_factura_by_id(db_session):
    # Crear una factura
    factura_data = FacturaCreate(
        cliente_nit="111222333",
        fecha_inicio="2024-03-01",
        fecha_fin="2024-03-31",
        monto_base=300.0,
        monto_adicional=30.0,
        monto_total=330.0,
        estado="pendiente"
    )
    factura = create_factura(db_session, factura_data)

    # Obtener la factura por ID
    factura_obtenida = get_factura_by_id(db_session, factura.id)
    assert factura_obtenida is not None
    assert factura_obtenida.cliente_nit == factura_data.cliente_nit
    assert factura_obtenida.monto_total == factura_data.monto_total

    # Verificar que un ID inexistente retorna None
    factura_inexistente = get_factura_by_id(db_session, factura_id=999)
    assert factura_inexistente is None


