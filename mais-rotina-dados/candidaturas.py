from src.matching import load_cfg, score_pair
from src.gen_dados import load_taxonomias

from pathlib import Path
import pandas as pd
from random import Random     

                            

def sortear_par_unico(rng, vagas_validas_df, candidatos_df, pares_existentes) -> tuple[str,str]:   
    
    choices_o = vagas_validas_df["id"].astype(str).str.strip().tolist()
    choices_c = candidatos_df["id"].astype(str).str.strip().tolist()
    max_tentativas = 50
    tentativas = 0

    
    while tentativas < max_tentativas:   
        
        vaga_id = rng.choice(choices_o) # 1 vaga id em vagas_validas_df
        cand_id = rng.choice(choices_c) # 1 candidato em candidatos_df

        if (vaga_id, cand_id) not in pares_existentes: # se (vaga_id, cand_id) em pares existentes, repetir.
            return (vaga_id, cand_id)                      
        
        tentativas += 1

    raise RuntimeError("limite de tentativas atingido ao sortear par único")

def sortear_pares_novos(rng, vagas_validas_df, candidatos_df, pares_existentes, n) -> set[tuple[str,str]]:
    usados = set(pares_existentes)   
    resultado = set()
    n = int(n)
    
    while len(resultado) < n:
            par = sortear_par_unico(rng, vagas_validas_df, candidatos_df, usados)
            resultado.add(par)
            usados.add(par)    
    
    return resultado

def load_oportunidades(path="data/samples/oportunidades.csv") -> pd.DataFrame:
    return pd.read_csv(path, dtype={"id": "string", "status": "string", "agencia_id": "string"})

def load_candidatos(path="data/samples/candidatos.csv") -> pd.DataFrame:
    return pd.read_csv(path, dtype={"id": "string"})

def load_sugestoes(path="data/outputs/sugestoes.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    req = {"vaga_id", "cand_id", "score"}
    faltando = req - set(df.columns)
    assert not faltando, f"faltam colunas em sugestoes.csv: {faltando}"
    df["vaga_id"] = df["vaga_id"].astype("string")
    df["cand_id"] = df["cand_id"].astype("string")
    df["score"] = df["score"].astype(float)
    return df

def filtrar_vagas_validas(df_o: pd.DataFrame) -> pd.DataFrame:
    return df_o.loc[df_o["status"].isin(["publicada", "em_selecao"]), ["id", "status"]].copy()

def marcar_status_sugestoes(rng: Random, df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    categorias = ["novo", "em_andamento", "entrevistado", "aguardando_resposta", "aprovado", "rejeitado"]
    pesos = [0.45, 0.25, 0.10, 0.10, 0.07, 0.03]
    df["status"] = rng.choices(categorias, weights=pesos, k=len(df))
    df["origem"] = "sugestao"
    return df

def preparar_base(rng: Random):
    print("CWD:", Path().resolve())

    df_o = load_oportunidades()
    df_c = load_candidatos()
    vagas_validas = filtrar_vagas_validas(df_o)

    print("vagas_validas:", len(vagas_validas), "| candidatos:", len(df_c))

    sug = load_sugestoes()
    print("sugestoes shape:", sug.shape)

    df_sug = marcar_status_sugestoes(rng, sug)
    print(df_sug[["vaga_id", "cand_id", "score", "origem", "status"]].head(5))

    pares_existentes = set(zip(df_sug["vaga_id"], df_sug["cand_id"]))
    N_esp = max(1, round(0.30 * len(df_sug)))
    print("pares_existentes:", len(pares_existentes), "| N_esp:", N_esp)

    return df_o, df_c, vagas_validas, df_sug, pares_existentes, N_esp

def carregar_ctx_matching():
    cfg = load_cfg("config/padroes.yml")
    tax = load_taxonomias()
    
    return (cfg, tax)

def get_row_by_id(df: pd.DataFrame, id_col: str, id_val: str) -> pd.Series:
    return df.loc[df[id_col] == id_val].iloc[0]

def pontuar_pares(pares, df_o, df_c, cfg, tax) -> pd.DataFrame:
    regs = []
    
    for vaga_id, cand_id in pares:
        vaga_row = get_row_by_id(df_o, "id", vaga_id)
        cand_row = get_row_by_id(df_c, "id", cand_id)
        s = score_pair(vaga_row, cand_row, cfg, tax)
        regs.append({"vaga_id": vaga_id, "cand_id": cand_id, "score": s})
    
    return pd.DataFrame(regs)

def consolidar_candidaturas(df_sug: pd.DataFrame, df_novos: pd.DataFrame) -> pd.DataFrame:
    cols = ["vaga_id", "cand_id", "score", "origem", "status"]
    base = pd.concat([df_sug[cols].copy(), df_novos[cols].copy()], ignore_index=True)

    base["vaga_id"] = base["vaga_id"].astype("string")
    base["cand_id"] = base["cand_id"].astype("string")
    base["score"] = base["score"].astype(float)

    base = base.sort_values(["vaga_id", "cand_id", "score"], ascending=[True, True, False])
    base = base.drop_duplicates(subset=["vaga_id", "cand_id"], keep="first")

    return base



def main():
    rng = Random(42)
    df_o, df_c, vagas_validas, df_sug, pares_existentes, N_esp = preparar_base(rng)
    cfg, tax = carregar_ctx_matching()

    print("CFG_PESOS:", cfg['matching']['pesos'])
    print("TAX_KEYS:", sorted(tax.keys())[:5], "...")

    # Micro-passo já feito: sortear 30% de pares novos
    pares_novos = sortear_pares_novos(rng, vagas_validas, df_c, pares_existentes, N_esp)
    print("pares_novos:", pares_novos)
    conflitos = sum(1 for p in pares_novos if p in pares_existentes)
    print("conflitos_com_existentes:", conflitos)   # deve ser 0
    print("qtd_novos:", len(pares_novos), "esperado:", N_esp)

    df_pontuados = pontuar_pares(pares_novos, df_o, df_c, cfg, tax)
    print("amostra - pontuados:")
    print(df_pontuados.head())

    TH_SCORE = 20
    df_pontuados = df_pontuados[df_pontuados["score"] >= TH_SCORE].copy()
    df_pontuados["origem"] = "sorteio"
    df_pontuados["status"] = "novo"

    print("apos filtro >= 20")
    print(df_pontuados)  

    df_final = consolidar_candidaturas(df_sug, df_pontuados)
    print("\namostra - consolidado")
    print(df_final.head())

    out_path = "data/outputs/candidaturas.csv"
    df_final.to_csv(out_path, index=False)
    print(f"\narquivo salvo em {out_path}")

    print("\nResumo:")
    print("-------")
    print("linhas totais:", len(df_final))
    print("por origem:\n", df_final["origem"].value_counts())
    print("\nTop 5 por score:")
    print(df_final.sort_values("score", ascending=False).head(5))

    vagas_cobertas = df_final["vaga_id"].nunique()
    total_vagas_validas = vagas_validas["id"].nunique()
    print(f"\nVagas cobertas: {vagas_cobertas} de {total_vagas_validas}")


if __name__ == "__main__":
    main()
