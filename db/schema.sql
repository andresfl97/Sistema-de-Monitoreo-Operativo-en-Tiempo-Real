-- ============================================================
-- Esquema relacional (PostgreSQL) — Sistema de Monitoreo Operativo
-- Caso ISP: desempeño de contratistas, soporte técnico y CX.
--
-- Nota: corresponde al paso de "Migración a PostgreSQL" del roadmap
-- del proyecto (sustitución de Google Sheets por base relacional).
-- Los datos reales fueron seudonimizados en cumplimiento de la LOPDP.
-- ============================================================

BEGIN;

-- ------------------------------------------------------------
-- Tablas de dimensión
-- ------------------------------------------------------------

-- Contratistas de campo (nombres neutralizados según política LOPDP)
CREATE TABLE IF NOT EXISTS contratistas (
    id            SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre        VARCHAR(30)  NOT NULL UNIQUE,     -- 'Contratista A', 'Contratista B'
    estado        VARCHAR(20)  NOT NULL DEFAULT 'Activo'
                  CHECK (estado IN ('Activo', 'Inactivo'))
);

-- Sectores geográficos de operación (etiquetas neutralizadas)
CREATE TABLE IF NOT EXISTS sectores (
    id            SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre        VARCHAR(30)  NOT NULL UNIQUE,     -- 'Alpha', 'Beta', 'Gamma'
    zona          VARCHAR(30)
);

-- Tipos de servicio atendidos
CREATE TABLE IF NOT EXISTS tipos_servicio (
    id            SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre        VARCHAR(30) NOT NULL UNIQUE       -- 'Instalacion', 'Soporte Tecnico', 'Atencion'
);

-- ------------------------------------------------------------
-- Tablas de hechos
-- ------------------------------------------------------------

-- Órdenes de servicio / tickets asignados a contratistas
CREATE TABLE IF NOT EXISTS ordenes_servicio (
    id                  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    contratista_id      SMALLINT NOT NULL REFERENCES contratistas (id),
    sector_id           SMALLINT NOT NULL REFERENCES sectores (id),
    tipo_servicio_id    SMALLINT NOT NULL REFERENCES tipos_servicio (id),
    fecha_creacion      TIMESTAMP NOT NULL,
    fecha_atencion      TIMESTAMP,
    horario             VARCHAR(10) NOT NULL CHECK (horario IN ('Diurno', 'Nocturno')),
    tipo_dia            VARCHAR(15) NOT NULL CHECK (tipo_dia IN ('Laboral', 'Fin de semana')),
    tiempo_espera_min   NUMERIC(6, 2) CHECK (tiempo_espera_min >= 0),
    resuelto_primera    BOOLEAN,                    -- eficiencia de resolución
    puntualidad         BOOLEAN,
    CONSTRAINT chk_orden_fechas CHECK (fecha_atencion IS NULL OR fecha_atencion >= fecha_creacion)
);

-- Encuestas post-servicio (Customer Experience)
CREATE TABLE IF NOT EXISTS encuestas (
    id                      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    orden_id                INTEGER NOT NULL REFERENCES ordenes_servicio (id),
    fecha_encuesta          TIMESTAMP NOT NULL,
    valoracion_atencion     SMALLINT CHECK (valoracion_atencion BETWEEN 1 AND 5),
    satisfaccion_general    SMALLINT CHECK (satisfaccion_general BETWEEN 1 AND 5),
    percepcion_servicio     SMALLINT CHECK (percepcion_servicio BETWEEN 1 AND 5),
    recomendacion           SMALLINT CHECK (recomendacion BETWEEN 0 AND 10),
    uso_soporte             VARCHAR(15) NOT NULL
                            CHECK (uso_soporte IN ('Si', 'No', 'No sabe - No usa')),
    motivo_no_uso           VARCHAR(40),
    sesgo_captura           BOOLEAN NOT NULL DEFAULT FALSE
                            -- TRUE si valoró "excelente"(5) y contestó "No sabe - No usa":
                            -- hallazgo de contaminación del formulario (GIGO).
);

-- ------------------------------------------------------------
-- Índices para rendimiento analítico
-- ------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_ordenes_contratista ON ordenes_servicio (contratista_id);
CREATE INDEX IF NOT EXISTS idx_ordenes_sector       ON ordenes_servicio (sector_id);
CREATE INDEX IF NOT EXISTS idx_ordenes_fecha        ON ordenes_servicio (fecha_creacion);
CREATE INDEX IF NOT EXISTS idx_encuestas_orden      ON encuestas (orden_id);
CREATE INDEX IF NOT EXISTS idx_encuestas_satisf     ON encuestas (satisfaccion_general);

COMMIT;
