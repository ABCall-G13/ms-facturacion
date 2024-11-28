CREATE DATABASE IF NOT EXISTS facturacion;

USE facturacion;

CREATE TABLE IF NOT EXISTS facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_nit VARCHAR(60) NOT NULL, 
    fecha_inicio DATE NOT NULL,      
    fecha_fin DATE NOT NULL,       
    monto_base DECIMAL(10, 2) NOT NULL, 
    monto_adicional DECIMAL(10, 2) DEFAULT 0.00, 
    monto_total DECIMAL(10, 2) NOT NULL,
    estado VARCHAR(50) DEFAULT 'pendiente',
    pdf_url VARCHAR(255) DEFAULT NULL,
    cliente_id INT NOT NULL,
    INDEX (fecha_inicio),
    INDEX (fecha_fin),
    INDEX (cliente_nit) 
);

CREATE TABLE IF NOT EXISTS incidentes_facturados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT NOT NULL,
    costo DECIMAL(10, 2) NOT NULL,
    fecha_incidente DATE NOT NULL,
    radicado_incidente VARCHAR(60) NOT NULL,
    cliente_id INT NOT NULL, 
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE,
    INDEX (fecha_incidente)
);
