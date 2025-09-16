# by chatGPT

from pathlib import Path
import pandas as pd
from random import Random

# --- 0) contexto / paths ---
# Rode este arquivo a partir da RAIZ do projeto (onde existem as pastas data/ e src/)
print("CWD:", Path().resolve())

# --- 1) carregar tabelas já salvas (NÃO regenerar) ---
df_o = pd.read_csv(
    "data/samples/oportunidades.csv",
    dtype={"id": "string", "agencia_id": "string", "status": "string"}
)
df_c = pd.read_csv(
    "data/samples/candidatos.csv",
    dtype={"id": "string"}
)

# --- 2) filtrar vagas válidas para candidaturas (publicada/em_selecao) ---
vagas_validas = df_o.loc[
    df_o["status"].isin(["publicada", "em_selecao"]),
    ["id", "status"]
].copy()

print("vagas_validas:", len(vagas_validas), "| candidatos:", len(df_c))

# --- 3) carregar sugestões existentes ---
def load_sugestoes(path="data/outputs/sugestoes.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    req = {"vaga_id", "cand_id", "score"}
    faltando = req - set(df.columns)
    assert not faltando, f"faltam colunas em sugestoes.csv: {faltando}"
    # tipagem coerente
    df["vaga_id"] = df["vaga_id"].astype("string")
    df["cand_id"] = df["cand_id"].astype("string")
    df["score"]   = df["score"].astype(float)
    return df

sug = load_sugestoes()
print("sugestoes shape:", sug.shape)

# --- 4) status para sugestões (origem='sugestao') ---
def marcar_status_sugestoes(rng: Random, df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    categorias = ["novo","em_andamento","entrevistado","aguardando_resposta","aprovado","rejeitado"]
    pesos      = [0.45, 0.25, 0.10, 0.10, 0.07, 0.03]
    df["status"] = rng.choices(categorias, weights=pesos, k=len(df))
    df["origem"] = "sugestao"
    return df

rng = Random(42)
df_sug = marcar_status_sugestoes(rng, sug)
print(df_sug[["vaga_id","cand_id","score","origem","status"]].head(5))

# --- 5) pares já existentes nas sugestões ---
pares_existentes = set(zip(df_sug["vaga_id"], df_sug["cand_id"]))
N_esp = max(1, round(0.30 * len(df_sug)))
print("pares_existentes:", len(pares_existentes), "| N_esp:", N_esp)