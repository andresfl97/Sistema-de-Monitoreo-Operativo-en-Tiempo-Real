"""
ETL de limpieza y normalización del dataset de encuestas del caso ISP.

Lee el CSV crudo, aplica controles de calidad de datos (nulos,
duplicados, dominios, rangos), normaliza categorías y marca el
sesgo de captura (valoración "excelente" + "No sabe / No usa").

Uso:
    python etl_clean.py [--input data/encuestas_isp.csv] [--output data/encuestas_limpio.csv]
"""

import argparse
import os

import pandas as pd

# Dominios esperados por columna (contrato de datos)
DOMINIOS = {
    "tipo_dia": {"Laboral", "Fin de semana"},
    "horario": {"Diurno", "Nocturno"},
    "contratista": {"A", "B"},
    "sector": {"Alpha", "Beta", "Gamma"},
    "tipo_servicio": {"Instalacion", "Soporte Tecnico", "Atencion"},
    "uso_soporte": {"Si", "No", "No sabe - No usa"},
    "resuelto_primera": {"Si", "No"},
    "puntualidad": {"Si", "No"},
}

RANGOS = {
    "valoracion_atencion": (1, 5),
    "satisfaccion_general": (1, 5),
    "percepcion_servicio": (1, 5),
    "recomendacion": (0, 10),
    "tiempo_espera_min": (0, None),
}


def normalizar_categorias(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in DOMINIOS:
        df[col] = df[col].astype(str).str.strip()
    return df


def calidad_datos(df: pd.DataFrame) -> dict:
    reporte = {
        "filas": len(df),
        "columnas": len(df.columns),
        "duplicados_id": int(df["id"].duplicated().sum()),
        "nulos": int(df.isna().sum().sum()),
        "fuera_de_dominio": {},
        "fuera_de_rango": {},
    }
    for col, valores in DOMINIOS.items():
        malos = int((~df[col].isin(valores)).sum())
        if malos:
            reporte["fuera_de_dominio"][col] = malos
    for col, (min_v, max_v) in RANGOS.items():
        if max_v is None:
            malos = int((df[col] < min_v).sum())
        else:
            malos = int((df[col] < min_v).sum() + (df[col] > max_v).sum())
        if malos:
            reporte["fuera_de_rango"][col] = malos
    return reporte


def marcar_sesgo_captura(df: pd.DataFrame) -> pd.DataFrame:
    """GIGO: usuarios que valoran 'excelente' (5) pero contestan
    'No sabe - No usa' contaminan la lectura de utilización real."""
    df = df.copy()
    df["sesgo_captura"] = (
        (df["satisfaccion_general"] == 5) & (df["uso_soporte"] == "No sabe - No usa")
    )
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=os.path.join("data", "encuestas_isp.csv"))
    parser.add_argument("--output", default=os.path.join("data", "encuestas_limpio.csv"))
    args = parser.parse_args()

    df = pd.read_csv(args.input, encoding="utf-8-sig")
    df = normalizar_categorias(df)
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)
    df = marcar_sesgo_captura(df)

    reporte = calidad_datos(df)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df.to_csv(args.output, index=False, encoding="utf-8-sig")

    print("=== Reporte de calidad de datos ===")
    for k, v in reporte.items():
        print(f"  {k}: {v}")
    print(f"  sesgos_captura: {int(df['sesgo_captura'].sum())}")
    print(f"Dataset limpio escrito en {args.output}")


if __name__ == "__main__":
    main()
