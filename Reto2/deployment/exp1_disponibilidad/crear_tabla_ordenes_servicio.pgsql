CREATE TABLE orden_servicio (
    id SERIAL PRIMARY KEY,
    fecha_hora_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_productos VARCHAR(100) NOT NULL,
    cantidad_productos INTEGER NOT NULL CHECK (cantidad_productos > 0),
    direccion_entrega TEXT NOT NULL,
    usuario_creador VARCHAR(50) NOT NULL,
    estado VARCHAR(20) DEFAULT 'creada',
    fecha_entrega TIMESTAMP,
    observaciones TEXT
);

-- Añadir índices para mejorar el rendimiento en consultas comunes
CREATE INDEX idx_orden_servicio_fecha ON orden_servicio(fecha_hora_creacion);
CREATE INDEX idx_orden_servicio_usuario ON orden_servicio(usuario_creador);