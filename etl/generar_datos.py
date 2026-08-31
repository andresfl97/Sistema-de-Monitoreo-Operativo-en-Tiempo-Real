"""
Genera el dataset de ejemplo de encuestas post-servicio del caso ISP.

El dataset es SINTETICO: reproduce, de forma consistente con las metricas
publicadas en el README, la estructura y los patrones del caso real
(anonimizado y seudonimizado en cumplimiento de la LOPDP).

Uso:
    python generar_datos.py            # escribe data/encuestas_isp.csv
    python generar_datos.py --check    # escribe y valida metricas vs README
"""

import argparse
import datetime as dt

import numpy as np
import pandas as pd

SEED = 42
N = 52  # tamano de muestra piloto (README: 45-52 encuestas)

COLUMNS = [
    "id",
    "fecha_hora",
    "tipo_dia",
    "horario",
    "contratista",
    "sector",
    "tipo_servicio",
    "valoracion_atencion",
    "satisfaccion_general",
    "percepcion_servicio",
    "recomendacion",
    "tiempo_espera_min",
    "uso_soporte",
    "motivo_no_uso",
    "resuelto_primera",
    "puntualidad",
]


def generar():
    rng = np.random.default_rng(SEED)

    # --- Distribucion de contratistas (55.9% / 44.1% segun README) ---
    contratistas = np.array(["A"] * 29 + ["B"] * 23)
    rng.shuffle(contratistas)

    # --- Sector: A concentra Alpha/Beta; B opera Beta/Gamma ---
    sectores = []
    for c in contratistas:
        if c == "A":
            sectores.append(rng.choice(["Alpha", "Alpha", "Alpha", "Beta", "Beta"]))
        else:
            sectores.append(rng.choice(["Beta", "Beta", "Gamma", "Gamma"]))
    sectores = np.array(sectores)

    # --- Tipo de servicio ---
    tipo_servicio = rng.choice(
        ["Instalacion", "Soporte Tecnico", "Atencion"], size=N, p=[0.30, 0.45, 0.25]
    )

    # --- Horario y dia ---
    # Objetivo README: inactividad nocturna 90.74% y fin de semana 87.04%
    horario = []
    tipo_dia = []
    uso = []
    motivo = []
    for i in range(N):
        es_fin = rng.random() < 0.20
        es_nocturno = rng.random() < 0.23
        tipo_dia.append("Fin de semana" if es_fin else "Laboral")
        horario.append("Nocturno" if es_nocturno else "Diurno")

        # Uso de soporte: solo Diurno/Laboral lo usa de forma relevante.
        # Nocturno: ~91% no usa; Fin de semana: ~87% no usa.
        if es_nocturno:
            usa = rng.random() < 0.10
        elif es_fin:
            usa = rng.random() < 0.15
        else:
            usa = rng.random() < 0.60
        uso.append("Si" if usa else rng.choice(["No", "No sabe - No usa"], p=[0.4, 0.6]))
        motivo.append("" if usa else rng.choice(["Desconozco el canal", "Servicio estable", "No lo necesito"]))

    # --- Valoraciones ---
    # CSAT 92.2% -> 48 de 52 con satisfaccion >= 4
    satisfaccion = np.array([5] * 34 + [4] * 14 + [3] * 3 + [2] * 1)
    rng.shuffle(satisfaccion)

    # Valoracion de atencion: promedio ~4.6
    valoracion = np.array([5] * 35 + [4] * 14 + [3] * 3)
    rng.shuffle(valoracion)

    # Percepcion general: promedio ~4.1
    percepcion = np.array([5] * 18 + [4] * 24 + [3] * 8 + [2] * 2)
    rng.shuffle(percepcion)

    # Recomendacion (0-10): promedio ~8
    recomendacion = np.array([10] * 10 + [9] * 14 + [8] * 12 + [7] * 8 + [6] * 6 + [5] * 2)
    rng.shuffle(recomendacion)

    # Tiempo de espera: promedio ~1.9 min (lognormal)
    tiempo_espera = rng.lognormal(mean=0.40, sigma=0.65, size=N)

    # --- Sesgo de captura (hallazgo del caso) ---
    # Usuarios que valoran "excelente" (5) pero contestan "No sabe - No usa":
    # contamina la lectura de baja utilizacion del soporte.
    for i in range(N):
        if satisfaccion[i] == 5 and rng.random() < 0.50:
            uso[i] = "No sabe - No usa"
            motivo[i] = "Desconozco el canal"

    # Ajuste de segmentos para reproducir inactividad del README:
    # todo el segmento no usa soporte, salvo exactamente 1 usuario por segmento.
    # (Nocturno: 10/11 o 11/12 ~ 90-92% ~ 90.74% · Fin de semana: ~90% ~ 87.04%)
    # Se evita solapamiento: la fila "activa" de cada segmento no puede pertenecer a ambos.
    for i in range(N):
        if horario[i] == "Nocturno" or tipo_dia[i] == "Fin de semana":
            uso[i] = "No sabe - No usa"
            motivo[i] = "Desconozco el canal"
    noct_solo = [i for i in range(N) if horario[i] == "Nocturno" and tipo_dia[i] != "Fin de semana"]
    fds_solo = [i for i in range(N) if tipo_dia[i] == "Fin de semana" and horario[i] != "Nocturno"]
    if noct_solo:
        uso[rng.choice(noct_solo)] = "Si"
        motivo[rng.choice(noct_solo)] = ""
    if fds_solo:
        uso[rng.choice(fds_solo)] = "Si"
        motivo[rng.choice(fds_solo)] = ""

    # --- Eficiencia de resolucion y puntualidad (determinista por contratista) ---
    # B: 21/23 = 91.3% (README ~92%) · A: 24/29 = 82.8%
    resuelto = ["No"] * N
    puntual = ["No"] * N
    for c, n_si in (("B", 21), ("A", 24)):
        idx = rng.choice(np.where(np.array(contratistas) == c)[0], size=n_si, replace=False)
        for i in idx:
            resuelto[i] = "Si"
            puntual[i] = "Si"

    # --- Fechas: ventana de un mes, evitando que el desorden estropee la segmentacion ---
    base = dt.datetime(2026, 1, 5, 9, 0)
    fechas = []
    for i in range(N):
        d = base + dt.timedelta(days=int(rng.integers(0, 28)), hours=int(rng.integers(0, 10)))
        fechas.append(d)

    df = pd.DataFrame(
        {
            "id": [f"SURV-{i+1:03d}" for i in range(N)],
            "fecha_hora": [f.isoformat(sep=" ") for f in fechas],
            "tipo_dia": tipo_dia,
            "horario": horario,
            "contratista": contratistas,
            "sector": sectores,
            "tipo_servicio": tipo_servicio,
            "valoracion_atencion": valoracion,
            "satisfaccion_general": satisfaccion,
            "percepcion_servicio": percepcion,
            "recomendacion": recomendacion,
            "tiempo_espera_min": np.round(tiempo_espera, 1),
            "uso_soporte": uso,
            "motivo_no_uso": motivo,
            "resuelto_primera": resuelto,
            "puntualidad": puntual,
        }
    )
    return df


def check(df):
    n = len(df)
    pct = lambda s: f"{100 * s.mean():.2f}%"
    print(f"Registros: {n}")
    print(f"Participacion Contratista A: {pct(df['contratista'] == 'A')}  (README 55.9%)")
    print(f"Participacion Contratista B: {pct(df['contratista'] == 'B')}  (README 44.1%)")
    print(f"CSAT (sat. >= 4): {pct(df['satisfaccion_general'] >= 4)}  (README 92.2%)")
    print(f"Tiempo Medio de Espera: {df['tiempo_espera_min'].mean():.1f} min  (README 1.9)")
    print(f"Valoracion de atencion: {df['valoracion_atencion'].mean():.2f}  (README 4.6)")
    print(f"Percepcion del servicio: {df['percepcion_servicio'].mean():.2f}  (README 4.1)")
    print(f"Recomendacion: {df['recomendacion'].mean():.1f}  (README 8)")
    print(f"Eficiencia resolucion B: {pct(df.loc[df['contratista'] == 'B', 'resuelto_primera'] == 'Si')}  (README 92.38%)")
    print(f"Puntualidad B: {pct(df.loc[df['contratista'] == 'B', 'puntualidad'] == 'Si')}  (README 93.33%)")
    noct = df[df["horario"] == "Nocturno"]
    fds = df[df["tipo_dia"] == "Fin de semana"]
    print(f"Inactividad nocturna: {pct(noct['uso_soporte'] != 'Si')}  (README 90.74%)")
    print(f"Inactividad fin de semana: {pct(fds['uso_soporte'] != 'Si')}  (README 87.04%)")
    cont = df[(df["satisfaccion_general"] == 5) & (df["uso_soporte"] == "No sabe - No usa")]
    print(f"Registros 'excelente' + 'No sabe/No usa' (sesgo): {len(cont)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validar metricas vs README")
    parser.add_argument("--out", default="data/encuestas_isp.csv")
    args = parser.parse_args()

    df = generar()
    out = args.out
    import os

    os.makedirs(os.path.dirname(out), exist_ok=True)
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"Dataset escrito en {out}")
    if args.check:
        check(df)
