-- ============================================================
-- Consultas analíticas — Sistema de Monitoreo Operativo (ISP)
--
-- Reproducen en PostgreSQL los KPIs publicados en el README:
--   participación operativa, CSAT, TME, eficiencia, puntualidad,
--   inactividad por horario/segmento y detección del sesgo.
--
-- Supone datos cargados desde el ETL (ver etl/etl_clean.py).
-- ============================================================

-- ------------------------------------------------------------
-- 1. Participación operativa por contratista (% de órdenes)
-- ------------------------------------------------------------
SELECT c.nombre                                                      AS contratista,
       COUNT(o.id)                                                   AS ordenes,
       ROUND(100.0 * COUNT(o.id) / SUM(COUNT(o.id)) OVER (), 1)      AS participacion_pct
FROM ordenes_servicio o
JOIN contratistas c ON c.id = o.contratista_id
GROUP BY c.nombre
ORDER BY participacion_pct DESC;

-- ------------------------------------------------------------
-- 2. Panel de CX: CSAT, valoración, percepción, recomendación, TME
-- ------------------------------------------------------------
SELECT ROUND(100.0 * COUNT(*) FILTER (WHERE e.satisfaccion_general >= 4) / COUNT(*), 1) AS csat_pct,
       ROUND(AVG(e.valoracion_atencion),  2)                                            AS valoracion_atencion,
       ROUND(AVG(e.percepcion_servicio),  2)                                            AS percepcion_servicio,
       ROUND(AVG(e.recomendacion),        1)                                            AS recomendacion,
       ROUND(AVG(o.tiempo_espera_min),    1)                                            AS tiempo_medio_espera_min
FROM encuestas e
JOIN ordenes_servicio o ON o.id = e.orden_id;

-- ------------------------------------------------------------
-- 3. CSAT, eficiencia de resolución y puntualidad por contratista
-- ------------------------------------------------------------
WITH resumen AS (
    SELECT c.nombre,
           COUNT(*)                                            AS total,
           COUNT(*) FILTER (WHERE e.satisfaccion_general >= 4) AS satisfechos,
           COUNT(*) FILTER (WHERE o.resuelto_primera)          AS resueltos,
           COUNT(*) FILTER (WHERE o.puntualidad)               AS puntuales
    FROM encuestas e
    JOIN ordenes_servicio o ON o.id = e.orden_id
    JOIN contratistas c      ON c.id = o.contratista_id
    GROUP BY c.nombre
)
SELECT nombre                                              AS contratista,
       ROUND(100.0 * satisfechos / total, 2)               AS csat_pct,
       ROUND(100.0 * resueltos  / total, 2)               AS eficiencia_resolucion_pct,
       ROUND(100.0 * puntuales / total, 2)                AS puntualidad_pct
FROM resumen
ORDER BY contratista;

-- ------------------------------------------------------------
-- 4. "Inactividad" aparente del soporte por segmento
--    (% de encuestas que NO usan soporte en cada segmento)
--    Hallazgo: nocturno y fin de semana muestran inactividad alta
--    que, tras el análisis del sesgo, era en parte un artefacto
--    de la captura, no un reflejo real del servicio.
-- ------------------------------------------------------------
SELECT horario                                                    AS segmento,
       COUNT(*)                                                   AS total,
       ROUND(100.0 * COUNT(*) FILTER (WHERE e.uso_soporte <> 'Si') / COUNT(*), 2) AS inactividad_pct
FROM encuestas e
JOIN ordenes_servicio o ON o.id = e.orden_id
GROUP BY horario
UNION ALL
SELECT 'Fin de semana',
       COUNT(*),
       ROUND(100.0 * COUNT(*) FILTER (WHERE e.uso_soporte <> 'Si') / COUNT(*), 2)
FROM encuestas e
JOIN ordenes_servicio o ON o.id = e.orden_id
WHERE o.tipo_dia = 'Fin de semana';

-- ------------------------------------------------------------
-- 5. Sesgo de captura (Garbage In, Garbage Out)
--    Encuestas que valoran "excelente" (5) pero afirman no usar
--    el soporte: contamina la lectura de utilización real.
-- ------------------------------------------------------------
SELECT COUNT(*)                                                        AS total_sesgos,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM encuestas), 1)   AS sesgo_pct,
       ROUND(100.0 * COUNT(*) FILTER (WHERE e.satisfaccion_general = 5)
              / NULLIF(COUNT(*) FILTER (WHERE e.satisfaccion_general = 5), 0), 1) AS participacion_en_excelentes
FROM encuestas e
WHERE e.sesgo_captura = TRUE;

-- ------------------------------------------------------------
-- 6. Window function — Ranking de sectores por carga operativa
--    y desviación del contratista respecto al promedio global
--    (análisis de balance operativo).
-- ------------------------------------------------------------
SELECT c.nombre                              AS contratista,
       s.nombre                              AS sector,
       COUNT(o.id)                           AS ordenes,
       ROUND(AVG(o.tiempo_espera_min), 2)    AS tme_promedio,
       ROUND(AVG(o.tiempo_espera_min)
               - AVG(AVG(o.tiempo_espera_min)) OVER (), 2)          AS desviacion_tme_global,
       RANK() OVER (ORDER BY COUNT(o.id) DESC)                      AS ranking_carga
FROM ordenes_servicio o
JOIN contratistas c ON c.id = o.contratista_id
JOIN sectores s      ON s.id = o.sector_id
GROUP BY c.nombre, s.nombre
ORDER BY ranking_carga;
