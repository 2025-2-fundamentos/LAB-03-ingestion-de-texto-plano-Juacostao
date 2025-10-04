"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
def pregunta_01():
    
    import pandas as pd
    import re

    path = "files/input/clusters_report.txt"
    with open(path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    # conservar líneas no vacías (pero no eliminar indentaciones aún)
    lines = [ln.rstrip("\n") for ln in raw_lines]

    # buscar la línea separadora (línea larga de guiones)
    sep_idx = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if len(s) > 10 and all(ch == "-" for ch in s):
            sep_idx = i
            break
    # si no se encuentra, buscar la primera línea que contenga "Cluster"
    if sep_idx is None:
        for i, ln in enumerate(lines):
            if "Cluster" in ln and "Cantidad" in ln:
                sep_idx = i + 1
                break

    data_lines = lines[sep_idx + 1 :] if sep_idx is not None else lines

    registros = []
    current = None

    # regex para línea que inicia registro: cluster, cantidad, porcentaje, inicio de palabras
    inicio_re = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%?\s*(.*)$")

    for ln in data_lines:
        if ln.strip() == "":
            continue
        m = inicio_re.match(ln)
        if m:
            # guardar anterior
            if current is not None:
                registros.append(current)
            cluster = int(m.group(1))
            cantidad = int(m.group(2))
            porcentaje_txt = m.group(3)
            try:
                porcentaje = float(porcentaje_txt.replace(",", "."))
            except Exception:
                porcentaje = None
            palabras = m.group(4).strip()
            current = {
                "cluster": cluster,
                "cantidad": cantidad,
                "porcentaje": porcentaje,
                "palabras": palabras,
            }
        else:
            # continuación de palabras clave (línea partida)
            if current is not None:
                # añadir con espacio (luego normalizamos espacios/comas)
                current["palabras"] += " " + ln.strip()
            else:
                # líneas previas al primer registro — ignorar
                continue

    # agregar último
    if current is not None:
        registros.append(current)

    # limpiar y normalizar palabras clave
    def limpiar_palabras(s):
        if s is None:
            return ""
        # quitar dobles espacios y normalizar espacios
        s = re.sub(r"\s+", " ", s).strip()
        # asegurar que las comas sean seguidas por una sola espacio
        s = re.sub(r"\s*,\s*", ", ", s)
        # quitar punto final si existe
        s = s.strip()
        s = s.rstrip(".")
        # quitar espacios sobrantes alrededor de paréntesis
        s = re.sub(r"\(\s+", "(", s)
        s = re.sub(r"\s+\)", ")", s)
        # eliminar espacios dobles resultantes
        s = re.sub(r"\s+", " ", s)
        return s

    data = []
    for rec in registros:
        data.append(
            {
                "cluster": rec["cluster"],
                "cantidad_de_palabras_clave": rec["cantidad"],
                "porcentaje_de_palabras_clave": rec["porcentaje"],
                "principales_palabras_clave": limpiar_palabras(rec["palabras"]),
            }
        )

    df = pd.DataFrame(data)
    df = df.sort_values("cluster").reset_index(drop=True)

    # Asegurar tipos correctos
    df["cluster"] = df["cluster"].astype(int)
    df["cantidad_de_palabras_clave"] = df["cantidad_de_palabras_clave"].astype(int)
    df["porcentaje_de_palabras_clave"] = df["porcentaje_de_palabras_clave"].astype(float)

    return df
