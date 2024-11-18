import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from sqlalchemy.orm import Session
from app.models.factura import Factura
from app.models.incidente_factura import IncidenteFacturado


def generar_pdf_factura(factura_id: int, db: Session, ruta: str):
    
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise ValueError(f"No se encontró ninguna factura con el ID {factura_id}")
    
    incidentes = db.query(IncidenteFacturado).filter(IncidenteFacturado.factura_id == factura_id).all()
    total_incidentes = len(incidentes)


    doc = SimpleDocTemplate(ruta, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Factura ID: {factura.id}", styles["Title"]))
    elements.append(Spacer(1, 20))

    info_factura = [
        ["Cliente NIT:", factura.cliente_nit],
        ["Periodo Facturado:", f"{factura.fecha_inicio} a {factura.fecha_fin}"],
        ["Monto Base:", f"${factura.monto_base:.2f}"],
        ["Monto Adicional:", f"${factura.monto_adicional:.2f}"],
        ["Monto Total:", f"${factura.monto_total:.2f}"],
        ["Total de Incidentes:", str(total_incidentes)],
    ]

    tabla_info = Table(info_factura, colWidths=[150, 300])
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
        elements.append(Paragraph("Detalles de los Incidentes", styles["Heading2"]))
        data_incidentes = [["Radicado", "Costo", "Fecha"]]
        for incidente in incidentes:
            data_incidentes.append([
                incidente.radicado_incidente,
                f"${incidente.costo:.2f}",
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


