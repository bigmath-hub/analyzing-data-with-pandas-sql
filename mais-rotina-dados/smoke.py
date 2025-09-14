# teste elaborado pelo chatGPT
# SMOKE TEST — rode a partir da raiz do repo
import pandas as pd

df_o = pd.read_csv("data/samples/oportunidades.csv")
df_a = pd.read_csv("data/samples/agencias.csv")

# 1) Proporção de urgente = 'sim'
is_urgent = df_o["urgente"].astype(str).str.strip().str.lower().eq("sim")
pct_urgent = is_urgent.mean()
print(f"[1] urgente='sim': {is_urgent.sum()} de {len(df_o)} ({pct_urgent*100:.1f}%)")

# 2) min/max de vagas_total
vt_min = int(df_o["vagas_total"].min())
vt_max = int(df_o["vagas_total"].max())
print(f"[2] vagas_total: min={vt_min}, max={vt_max}")

# 3) agencia_id das vagas ⊆ agências ativas
active_agencies = set(
    df_a.loc[
        df_a["status"].astype(str).str.strip().str.lower().eq("ativa"),
        "agencia_id",
    ].astype(str).str.strip()
)
agencies_used = set(df_o["agencia_id"].astype(str).str.strip())
invalid = sorted(agencies_used - active_agencies)
print(f"[3] agencia_id fora das ATIVAS: {len(invalid)}", (invalid[:5] if invalid else ""))

# 4) 3 amostras de descricao_curta (com tamanho)
sample = df_o[["id", "descricao_curta"]].head(3).copy()
sample["len"] = sample["descricao_curta"].astype(str).str.len()
print("[4] amostras de descricao_curta:")
print(sample.to_string(index=False))

# (extra) quantas descrições >120 chars?
over120 = (df_o["descricao_curta"].astype(str).str.len() > 120).sum()
print(f"[extra] descricoes_curta >120 chars: {over120}")