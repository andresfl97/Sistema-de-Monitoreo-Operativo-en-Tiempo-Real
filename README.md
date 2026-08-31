## Políticas de Confidencialidad y Gobierno de Datos (Cumplimiento LOPDP Ecuador)

Con el fin de garantizar el secreto profesional, la protección de la propiedad intelectual de la organización y el cumplimiento del marco legal ecuatoriano, toda la información sensible contenida en este repositorio fue sometida a procesos de **anonimización y seudonimización**.

Este tratamiento se sustenta en la **Ley Orgánica de Protección de Datos Personales (LOPDP)** de la República del Ecuador bajo los siguientes lineamientos:

| Principio Aplicado | Implementación |
|---|---|
| **Confidencialidad (Art. 10 - LOPDP)** | Los nombres reales de la empresa y contratistas fueron reemplazados mediante etiquetas neutrales como *Contratista A* y *Contratista B*. |
| **Seguridad y Anonimización (Art. 11 - LOPDP)** | Los datos numéricos, geográficos y volumétricos fueron transformados visualmente para evitar trazabilidad operativa y comercial. Las etiquetas *Alpha*, *Beta* y *Gamma* hacen referencia a los sectores donde operan los contratistas. |
| **Protección de Información** | Se resguarda el ecosistema de **+XXXX clientes activos** y la operación interna del ISP. |

Este repositorio constituye un **caso de estudio con fines académicos y de demostración técnica**, enfocado en exponer la arquitectura del pipeline, la lógica analítica y el modelado de datos sin comprometer activos de información ni acuerdos de confidencialidad.

---

# Sistema de Monitoreo en Tiempo Real: KPI’s Operativos y Customer Experience (CX) — Entorno ISP (+XXXX clientes activos)



### ❓ ¿Puede un proveedor de internet mejorar la experiencia de sus usuarios si no dispone de visibilidad en tiempo real sobre el desempeño de instalación, soporte técnico y atención al cliente?


## 🔍 Problemática

En la operación del ISP no existía un sistema centralizado que permitiera:

- Auditar el rendimiento operativo de contratistas.
- Medir tiempos de atención y resolución.
- Consolidar métricas de soporte técnico y experiencia del cliente.
- Identificar cuellos de botella operativos en tiempo real.

La ausencia de datos estructurados obligaba a mantener una gestión reactiva basada principalmente en reclamos de usuarios, limitando la capacidad de supervisión técnica y toma de decisiones.

---

## 🛠️ Solución

Para resolver este vacío operacional, se diseñó e implementó un pipeline de datos automatizado, integrado de extremo a extremo (*End-to-End*) bajo una arquitectura *Cloud-Native*.

| Componente | Función |
|---|---|
| **Google Forms** | Captura de encuestas post-servicio y satisfacción del cliente |
| **Google Sheets** | Repositorio centralizado y procesamiento ETL/ELT |
| **Looker Studio** | Visualización de KPI’s y reportería ejecutiva en tiempo real |

<p align="center">
  <img width="500" alt="Diagrama de Flujo del Sistema" src="https://github.com/user-attachments/assets/2483cee7-8f79-49d4-b122-58a3b536527f" />
</p>

### 🔄 Flujo Operativo del Sistema

- **Ingesta:** Captura de experiencia del cliente mediante llamadas en frío centralizadas en Google Forms.
- **Procesamiento:** Transformación y normalización del dato en Google Sheets mediante procesos ETL.
- **Visualización:** Publicación de dashboards interactivos en Looker Studio para monitoreo operativo y analítico.

---

#  Módulo 1: Análisis de Desempeño de Contratistas

### ❓ ¿La distribución de carga operativa permite garantizar calidad y satisfacción del cliente?

## 💡 Primeras Percepciones del Módulo Técnico

El análisis de la muestra piloto permitió detectar patrones relevantes sobre distribución operativa y desempeño técnico.

| Indicador | Resultado |
|---|---|
| Participación Operativa Contratista A | 55.9% |
| Participación Operativa Contratista B | 44.1% |
| Sectores con mayor despliegue | Sector Alpha y Sector Beta |
| Eficiencia de Resolución — Contratista B | 92.38% |
| Puntualidad — Contratista B | 93.33% |

---

<img width="1103" height="868" alt="contratistas_anonimizado" src="https://github.com/user-attachments/assets/e53f70d2-e614-4866-affe-1e83d61536a6" />

---

### 🔎 Observaciones Detectadas

- El **Contratista A** concentraba la mayor carga operativa.
- El **Contratista B** presentó diferencias en puntualidad y eficiencia respecto al estándar esperado.
- La distribución geográfica evidenció oportunidades de optimización logística.


---

## 🚀 Oportunidades de Mejora — Módulo Técnico

- **Homologación de SLA’s:** Auditoría técnica y mesas de trabajo para estandarizar niveles de servicio entre contratistas.
- **Optimización Logística:** Redistribución geográfica de órdenes de trabajo para reducir tiempos de traslado.
- **Balance Operativo:** Mejor distribución de carga entre contratistas.
- **Monitoreo Continuo:** Seguimiento de KPI’s operativos en tiempo real, lanzar alerta en puntuaciones menores a 8.

---

#  Módulo 2: Customer Experience (CX)

### ❓ ¿La satisfacción del cliente refleja realmente la utilización y efectividad del soporte técnico?

## 💡 Auditoría de Calidad del Dato y Percepción del Servicio

El análisis integró indicadores operativos del equipo *Helpdesk* con métricas de experiencia del cliente para contrastar desempeño técnico y percepción del servicio.

### 📈 Indicadores Operativos

| KPI | Resultado |
|---|---|
| CSAT | 92.2% |
| Tiempo Medio de Espera (TME) | 1.9 minutos |
| Valoración de Atención | 4.6 / 5 |
| Percepción General del Servicio | 4.1 / 5 |
| Nivel de Recomendación | 8 / 10 |

A pesar de los indicadores positivos, el análisis detectó niveles elevados de aparente inactividad en horarios especiales:

- **Horario nocturno:** 90.74%
- **Fines de semana:** 87.04%

---

<img width="1411" height="1071" alt="informe_general" src="https://github.com/user-attachments/assets/6b19ab06-0afa-4da9-a6a3-de5c453572ed" />

---

## ⚠️ Hallazgo Analítico: Sesgo en la Captura

La auditoría del dato crudo permitió detectar contaminación de variables dentro del formulario de captura.

Muchos usuarios que calificaban el servicio como “excelente” seleccionaban simultáneamente la opción:

> *“No sabe / No usa”*

Esto generaba una interpretación errónea sobre baja utilización del soporte técnico.

### 🔍 Interpretación Estratégica

El análisis permitió identificar que:

- La baja interacción no implicaba necesariamente baja calidad del soporte.
- Existía desconocimiento de los canales de atención 24/7, son invisibles para los usuarios del servicio.
- Un diseño ambiguo en la captura distorsionaba indicadores operativos y gerenciales.

---

## 💡 Aprendizaje Técnico

La detección temprana de este sesgo permitió validar el impacto práctico de la regla:

> *Garbage In, Garbage Out*

Datos ambiguos producen análisis imprecisos y pueden afectar decisiones operativas, presupuestarias y estratégicas.

---



# 🚀 Oportunidades de Mejora — Módulo CX

## 📐 Reingeniería de Captura de Datos

Se rediseñó el flujo de captura mediante lógica de exclusión condicional (*Skip Logic*) para separar correctamente:

- Usuarios que desconocen la existencia del soporte.
- Usuarios que no utilizan soporte debido a estabilidad del servicio.

### Resultado obtenido

- Reducción de ambigüedad en formularios.
- Mayor trazabilidad analítica.
- Mejor interpretación de indicadores operativos.

---

## 🧠 Análisis de Sentimientos y Contexto Operativo

Durante las llamadas telefónicas se identificó que las encuestas estructuradas no reflejaban completamente la percepción del cliente.

Aunque muchos usuarios calificaban positivamente el servicio, las conversaciones permitían detectar:

- Frustraciones operativas.
- Molestias no registradas en formularios.
- Observaciones técnicas adicionales.
- Falta de comunicación.

---

### ❓ ¿Es apropiado tomar decisiones presupuestarias basadas en una muestra piloto reducida?

## 🎯 Estado Actual del Proyecto

| Elemento | Estado |
|---|---|
| Tipo de Proyecto | Producto Mínimo Viable |
| Tamaño de Muestra | 45 a 52 (encuestas/panel de control) |
| Técnica de Muestreo | Muestreo Aleatorio Simple (MAS) |
| Nivel de Inferencia | Exploratorio |
| Objetivo Actual | Descubrimiento de patrones y sesgos |

## 📋 Consideraciones Estadísticas

- La muestra permitió detectar inconsistencias en la captura y comportamiento operativo.
- El volumen actual todavía no representa completamente el universo de **+XXXX clientes activos**.
- Los resultados deben interpretarse como tendencias preliminares y no como métricas definitivas para decisiones de alto presupuesto.

---

# 🔄 Recomendaciones y Escalabilidad del Proyecto

Para evolucionar hacia una arquitectura de datos empresarial, se plantea el siguiente roadmap:

- [ ] **Migración a PostgreSQL:** Sustitución de Google Sheets por una base de datos relacional para mejorar integridad y escalabilidad.
- [ ] **Series Temporales y Clustering:** Identificación de patrones de estacionalidad y segmentación de clientes con riesgo de *churn*.
- [ ] **Dashboards Avanzados:** Implementación de filtros dinámicos y segmentación temporal en Looker Studio.
- [ ] **Automatización ETL:** Programación de procesos automáticos de limpieza y transformación del dato.
- [ ] **Gobierno del Dato:** Fortalecimiento de trazabilidad, calidad y consistencia analítica.

---

## 🧰 Reproducibilidad (código)

Los resultados publicados en este documento pueden reproducirse localmente con los scripts del repositorio:

```
# 1. (Opcional) Regenerar el dataset de ejemplo
python etl/generar_datos.py --check

# 2. ETL: limpieza, calidad de datos y marca de sesgo de captura
python etl/etl_clean.py

# 3. Análisis: reproduce los KPIs del README y compara contra ellos
python etl/analisis_insights.py
```

| Artefacto | Descripción |
|---|---|
| `data/encuestas_isp.csv` | Dataset de ejemplo (sintético, consistente con las métricas publicadas) |
| `etl/generar_datos.py` | Generación reproducible del dataset (semilla fija) |
| `etl/etl_clean.py` | Normalización, control de calidad y detección del sesgo de captura (GIGO) |
| `etl/analisis_insights.py` | Reproducción de los KPIs del README |
| `db/schema.sql` | Esquema PostgreSQL propuesto (paso de migración del roadmap) |
| `db/analytics_queries.sql` | Consultas analíticas con CTEs y window functions |

> **Nota sobre el dataset:** `encuestas_isp.csv` es sintético y se publica únicamente con fines de demostración y reproducibilidad. Mantiene la estructura y los patrones del caso real (anonimizado y seudonimizado según LOPDP), de modo que los KPIs del README se reproducen con diferencias menores de redondeo.

---

## 🧭 Contexto y origen del proyecto

Este caso nació de la experiencia directa en la operación FTTH/GPON de un ISP. La operación carecía de visibilidad sobre el desempeño de contratistas, los tiempos de atención y la experiencia del cliente; ante esa brecha se diseñó e implementó este sistema de monitoreo.

El proyecto se construyó de forma autónoma durante un periodo de trabajo en oficina y, tras demostrar su valor operativo, marcó la orientación profesional del autor hacia el análisis de datos y la automatización.
