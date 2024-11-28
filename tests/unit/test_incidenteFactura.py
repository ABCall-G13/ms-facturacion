import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.schemas.factura import FacturaCreate
from app.schemas.incidente_factura import incidente_facturadoCreate
from app.crud.factura import create_factura
from app.crud.incidente_factura import create_incidente_facturado, get_incidente_by_id, get_incidentes_by_factura


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


def test_create_incidente_facturado(db_session):
    # Crear una factura
    factura_data = FacturaCreate(
        cliente_nit="123456789",
        fecha_inicio="2024-01-01",
        fecha_fin="2024-01-31",
        monto_base=100.0,
        monto_adicional=20.0,
        monto_total=120.0,
        estado="pendiente",
        cliente_id=1
    )
    factura = create_factura(db_session, factura_data)

    # Crear un incidente relacionado (sin especificar factura_id)
    incidente_data = incidente_facturadoCreate(
        radicado_incidente="RAD-001",
        costo=50.0,
        fecha_incidente="2024-01-15",
        nit="123456789",
        cliente_id=1
    )
    # Se espera que el create_incidente_facturado calcule el factura_id automáticamente
    incidente = create_incidente_facturado(db_session, {
        "radicado_incidente": incidente_data.radicado_incidente,
        "factura_id": factura.id,  # Simulamos el cálculo dinámico
        "costo": incidente_data.costo,
        "fecha_incidente": incidente_data.fecha_incidente,
        "cliente_id": 1
    })

    assert incidente.factura_id == factura.id
    assert incidente.radicado_incidente == incidente_data.radicado_incidente
    assert incidente.costo == incidente_data.costo
    assert incidente.fecha_incidente.isoformat() == incidente_data.fecha_incidente.isoformat()


def test_get_incidente_by_id(db_session):
    # Crear una factura
    factura_data = FacturaCreate(
        cliente_nit="111222333",
        fecha_inicio="2024-03-01",
        fecha_fin="2024-03-31",
        monto_base=300.0,
        monto_adicional=30.0,
        monto_total=330.0,
        estado="pendiente",
        cliente_id=1
    )
    factura = create_factura(db_session, factura_data)

    # Crear un incidente relacionado
    incidente_data = incidente_facturadoCreate(
        radicado_incidente="RAD-002",
        costo=60.0,
        fecha_incidente="2024-03-20",
        nit="123456789",
        cliente_id=1
    )
    incidente = create_incidente_facturado(db_session, {
        "radicado_incidente": incidente_data.radicado_incidente,
        "factura_id": factura.id,  # Simulamos el cálculo dinámico
        "costo": incidente_data.costo,
        "fecha_incidente": incidente_data.fecha_incidente,
        "cliente_id": incidente_data.cliente_id
    })

    # Obtener el incidente por ID
    incidente_obtenido = get_incidente_by_id(db_session, incidente_id=incidente.id)
    assert incidente_obtenido is not None
    assert incidente_obtenido.radicado_incidente == incidente_data.radicado_incidente
    assert incidente_obtenido.factura_id == factura.id

    # Verificar que un ID inexistente retorna None
    incidente_inexistente = get_incidente_by_id(db_session, incidente_id=999)
    assert incidente_inexistente is None


def test_get_incidentes_by_factura(db_session):
    # Crear una factura
    factura_data = FacturaCreate(
        cliente_nit="987654321",
        fecha_inicio="2024-02-01",
        fecha_fin="2024-02-28",
        monto_base=200.0,
        monto_adicional=50.0,
        monto_total=250.0,
        estado="pagada",
        cliente_id=1
    )
    factura = create_factura(db_session, factura_data)

    # Crear incidentes relacionados
    incidente_1 = incidente_facturadoCreate(
        radicado_incidente="RAD-003",
        costo=30.0,
        fecha_incidente="2024-02-10",
        nit="123456789",
        cliente_id=1
    )
    incidente_2 = incidente_facturadoCreate(
        radicado_incidente="RAD-004",
        costo=40.0,
        fecha_incidente="2024-02-15",
        nit="123456789",
        cliente_id=1
    )
    create_incidente_facturado(db_session, {
        "radicado_incidente": incidente_1.radicado_incidente,
        "factura_id": factura.id,  # Simulamos el cálculo dinámico
        "costo": incidente_1.costo,
        "fecha_incidente": incidente_1.fecha_incidente,
        "cliente_id": incidente_1.cliente_id
    })
    create_incidente_facturado(db_session, {
        "radicado_incidente": incidente_2.radicado_incidente,
        "factura_id": factura.id,  # Simulamos el cálculo dinámico
        "costo": incidente_2.costo,
        "fecha_incidente": incidente_2.fecha_incidente,
        "cliente_id": incidente_2.cliente_id
    })

    # Obtener los incidentes de la factura
    incidentes = get_incidentes_by_factura(db_session, factura_id=factura.id)
    assert len(incidentes) == 2
    assert incidentes[0].radicado_incidente == "RAD-003"
    assert incidentes[1].radicado_incidente == "RAD-004"
