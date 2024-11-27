import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from sqlalchemy.orm import Session
from app.models.factura import Factura
from app.models.incidente_factura import IncidenteFacturado


def generar_pdf_factura(factura_id: int, db: Session, ruta: str, currency: str = "COP", lenguage: str = "es"):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise ValueError(f"No se encontró ninguna factura con el ID {factura_id}")
    
    incidentes = db.query(IncidenteFacturado).filter(IncidenteFacturado.factura_id == factura_id).all()
    total_incidentes = len(incidentes)
    
    # Conversión de moneda
    tasa_conversion = 4000
    conversion = 1 if currency == "COP" else 1 / tasa_conversion
    simbolo_moneda = "$" if currency == "COP" else "USD$"

    # Traducción de etiquetas
    etiquetas = {
        "es": {
            "factura_id": "Factura ID",
            "cliente_nit": "Cliente NIT",
            "periodo_facturado": "Periodo Facturado",
            "monto_base": "Monto Base",
            "monto_adicional": "Monto Adicional",
            "monto_total": "Monto Total",
            "total_incidentes": "Total de Incidentes",
            "detalles_incidentes": "Detalles de los Incidentes",
            "radicado": "Radicado",
            "costo": "Costo",
            "fecha": "Fecha"
        },
        "en": {
            "factura_id": "Invoice ID",
            "cliente_nit": "Customer NIT",
            "periodo_facturado": "Billed Period",
            "monto_base": "Base Amount",
            "monto_adicional": "Additional Amount",
            "monto_total": "Total Amount",
            "total_incidentes": "Total Incidents",
            "detalles_incidentes": "Incident Details",
            "radicado": "Filed Number",
            "costo": "Cost",
            "fecha": "Date"
        }
    }

    etiquetas = etiquetas[lenguage]

    # Crear documento PDF
    doc = SimpleDocTemplate(ruta, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"{etiquetas['factura_id']}: {factura.id}", styles["Title"]))
    elements.append(Spacer(1, 20))

    info_factura = [
        [etiquetas["cliente_nit"], factura.cliente_nit],
        [etiquetas["periodo_facturado"], f"{factura.fecha_inicio} a {factura.fecha_fin}"],
        [etiquetas["monto_base"], f"{simbolo_moneda} {factura.monto_base * conversion:.2f}"],
        [etiquetas["monto_adicional"], f"{simbolo_moneda} {factura.monto_adicional * conversion:.2f}"],
        [etiquetas["monto_total"], f"{simbolo_moneda} {factura.monto_total * conversion:.2f}"],
        [etiquetas["total_incidentes"], str(total_incidentes)],
    ]

    tabla_info = Table(info_factura, colWidths=[200, 300])
    tabla_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(tabla_info)
    elements.append(Spacer(1, 20))

    if total_incidentes > 0:
        elements.append(Paragraph(etiquetas["detalles_incidentes"], styles["Heading2"]))
        data_incidentes = [[etiquetas["radicado"], etiquetas["costo"], etiquetas["fecha"]]]
        for incidente in incidentes:
            data_incidentes.append([
                incidente.radicado_incidente,
                f"{simbolo_moneda} {incidente.costo * conversion:.2f}",
                str(incidente.fecha_incidente),
            ])

        tabla_incidentes = Table(data_incidentes, colWidths=[150, 150, 150])
        tabla_incidentes.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(tabla_incidentes)

    doc.build(elements)

    # Verificar si el archivo se ha guardado correctamente
    if os.path.exists(ruta):
        print(f"PDF guardado en: {ruta}")
    else:
        print(f"Error: No se pudo guardar el PDF en: {ruta}")
