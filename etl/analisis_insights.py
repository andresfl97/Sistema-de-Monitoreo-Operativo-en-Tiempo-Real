"""
Reproduce los KPIs publicados en el README a partir del dataset limpio,
convirtiendo el caso en un análisis reproducible (no solo capturas).

Uso:
    python analisis_insights.py [--input data/encuestas_limpio.csv]
"""

import argparse
import os

import pandas as pd

# Valores de referencia publicados en el README (muestra piloto 45-52)
REFERENCIA = {
    "Participación Contratista A": 55.9,
    "Participación Contratista B": 44.1,
    "CSAT": 92.2,
    "Tiempo Medio de Espera (min)": 1.9,
    "Valoración de Atención (1-5)": 4.6,
    "Percepción del Servicio (1-5)": 4.1,
    "Recomendación (0-10)": 8.0,
    "Eficiencia de Resolución B (%)": 92.38,
    "Puntualidad B (%)": 93.33,
    "Inactividad Nocturna (%)": 90.74,
    "Inactividad Fin de Semana (%)": 87.04,
}


def metricas(df: pd.DataFrame) -> dict:
    pct = lambda s: 100.0 * s.mean()
    b = df["contratista"] == "B"
    nocturno = df[df["horario"] == "Nocturno"]
    fin_semana = df[df["tipo_dia"] == "Fin de semana"]

    return {
        "Participación Contratista A": pct(df["contratista"] == "A"),
        "Participación Contratista B": pct(df["contratista"] == "B"),
        "CSAT": pct(df["satisfaccion_general"] >= 4),
        "Tiempo Medio de Espera (min)": df["tiempo_espera_min"].mean(),
        "Valoración de Atención (1-5)": df["valoracion_atencion"].mean(),
        "Percepción del Servicio (1-5)": df["percepcion_servicio"].mean(),
        "Recomendación (0-10)": df["recomendacion"].mean(),
        "Eficiencia de Resolución B (%)": pct(df.loc[b, "resuelto_primera"] == "Si"),
        "Puntualidad B (%)": pct(df.loc[b, "puntualidad"] == "Si"),
        "Inactividad Nocturna (%)": pct(nocturno["uso_soporte"] != "Si"),
        "Inactividad Fin de Semana (%)": pct(fin_semana["uso_soporte"] != "Si"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=os.path.join("data", "encuestas_limpio.csv"))
    args = parser.parse_args()

    df = pd.read_csv(args.input, encoding="utf-8-sig")
    m = metricas(df)

    print("=== KPIs reproducidos vs README ===")
    print(f"{'Métrica':<34}{'Obtenido':>10}{'README':>10}{'Dif':>8}")
    for k, ref in REFERENCIA.items():
        valor = m[k]
        es_pct = k.endswith("(%)")
        suf = "%" if es_pct else ""
        print(f"{k:<34}{valor:>9.2f}{suf}{ref:>9.2f}{suf}{valor - ref:>+7.2f}{suf}")

    print("\n=== Hallazgo: sesgo de captura (GIGO) ===")
    sesgos = df["sesgo_captura"]
    print(f"Encuestas con valoración 'excelente' + 'No sabe/No usa': {sesgos.sum()} de {len(df)}")
    print(
        "Interpretación: la baja interacción NO implica baja calidad del soporte; "
        "el diseño de la captura distorsiona la utilización real."
    )


if __name__ == "__main__":
    main()
