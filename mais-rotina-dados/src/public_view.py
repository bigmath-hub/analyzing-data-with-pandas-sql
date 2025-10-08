import pandas as pd

from pathlib import Path

def export_json(df: pd.DataFrame, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    # orient="records" -> lista de objetos; indent para ficar legível
    df.to_json(path, orient="records", force_ascii=False, indent=2)


def public_vagas(
        path_o="data/samples/oportunidades.csv", 
        path_c="data/outputs/candidaturas.csv"
) -> pd.DataFrame:
    
    # carregar as bases
    df_o = pd.read_csv(
        path_o, 
        dtype={"id": "string", "status": "string", "agencia_id": "string"}
    )
    df_c = pd.read_csv(
        path_c,
        dtype={"vaga_id": "string", "cand_id": "string", "score": float}
    )

    if df_c.empty:
        cont_cand = pd.DataFrame(
            0,
            index=df_o['id'],
            columns=['sugestao', 'sorteio']
        )
        top1 = pd.DataFrame(
            {'cand_id': "", 'score': 0.0},
            index=df_o['id']
        )
    else:
        # contagem por origem
        cont_cand = (
            df_c.groupby('vaga_id')['origem']
            .value_counts()
            .unstack()
            .reindex(columns=['sugestao', 'sorteio'], fill_value=0)
            .astype("Int64")
        )

        # melhor candidato por vaga
        idx = df_c.groupby('vaga_id')['score'].idxmax()
        top1 = (
            df_c.loc[idx, ['vaga_id', 'cand_id', 'score']]
            .set_index('vaga_id')
        )
        top1 = top1.reindex(df_o['id']).fillna({'cand_id': "", 'score': 0.0})

    # merges
    base = (
        df_o
        .merge(cont_cand, how='left', left_on='id', right_index=True)
        .merge(top1, how='left', left_on='id', right_index=True)
    )

    # limpeza
    for col in ['sugestao', 'sorteio']:
        base[col] = base[col].fillna(0).astype(int)

    base['score'] = base['score'].fillna(0.0).astype(float)
    base['cand_id'] = base['cand_id'].fillna("").astype("string")
    
    base['cands_total'] = base['sugestao'] + base['sorteio']

    # renomear
    ren = {
        'id': 'vaga_id',
        'sugestao': 'cands_sugestao',
        'sorteio': 'cands_sorteio',
        'cand_id': 'top1_cand_id',
        'score': 'top1_score'
    }

    if "status_x" in base.columns and "status" not in base.columns:
        ren["status_x"] = "status"

    base = base.rename(columns=ren)

    cols_finais = [
        "vaga_id", "titulo", "pais", "agencia_id", "status", "urgente", "vagas_total",
        "cands_sugestao", "cands_sorteio", "cands_total",
        "top1_cand_id", "top1_score",
    ]

    df_final = base[cols_finais].copy()

    return df_final

def public_candidatos(
        p_candidatos="data/samples/candidatos.csv", 
        p_candidaturas="data/outputs/candidaturas.csv", 
        p_oportunidades="data/samples/oportunidades.csv"
) -> pd.DataFrame:
    
    df_candidaturas = pd.read_csv( 
        p_candidaturas,
        dtype={"vaga_id": "string", "cand_id": "string", "score": float, "origem": "string", "status": "string"}        
    )
    df_candidatos = pd.read_csv(p_candidatos, dtype="string") 
    df_oportunidades = pd.read_csv(p_oportunidades, dtype="string")  
    
    
    if df_candidaturas.empty:
        contagem_origem = pd.DataFrame(0, index=df_candidatos['id'], colunms=['sugestao', 'sorteio'])
        top_vaga_info = pd.DataFrame(colunms=['cand_id', 'vaga_id', 'titlulo', 'score'])    
    else:       
        # contagem por origem e totais
        contagem_origem = (df_candidaturas.groupby("cand_id")['origem']            
            .value_counts()
            .unstack()            
            .reindex(columns=['sugestao', 'sorteio'],fill_value=0)
            .fillna(0)
            .astype(int) # limpar na origem dessa vez
        )        
        idx = df_candidaturas.groupby('cand_id')['score'].idxmax()
        melhores_linhas = df_candidaturas.loc[idx, ["cand_id", "vaga_id", "score"]]
        
        top_vaga_info = melhores_linhas.merge(
            df_oportunidades[["id", "titulo"]],
            left_on="vaga_id",
            right_on="id",
            how="left",
        ).drop(columns=["id"])

        contagem_origem = contagem_origem.reindex(df_candidatos["id"], fill_value=0)
        contagem_origem["inscricoes_total"] = contagem_origem.sum(axis=1)

        df_final = (
            df_candidatos
            .merge(contagem_origem, how="left", left_on="id", right_index=True)
            .merge(top_vaga_info, how="left", left_on="id", right_on="cand_id")
            .drop(columns=["cand_id"])  # veio do merge do top_vaga_info
        )

        for col in ["sugestao", "sorteio", "inscricoes_total"]:
            df_final[col] = df_final[col].fillna(0).astype(int)

        df_final["score"] = df_final["score"].fillna(0.0).astype(float)
        for col in ["vaga_id", "titulo"]:
            df_final[col] = df_final[col].fillna("").astype("string")

        df_final = df_final.rename(columns={
            "id": "cand_id",
            "sugestao": "total_sugestao",
            "sorteio": "total_sorteio",
            "vaga_id": "top_vaga_id",
            "titulo": "top_vaga_titulo",
            "score": "top_score",
        })

        colunas_finais = [
            "cand_id", "nome", "idiomas", "regioes_preferidas", "tipo",
            "total_sugestao", "total_sorteio", "inscricoes_total",
            "top_vaga_id", "top_vaga_titulo", "top_score",
        ]

        return df_final[colunas_finais]

def main():
    
    df_vagas = public_vagas()
    df_candidatos = public_candidatos()    
    
    # objetivo: encontrar os 5 candidatos com > inscricoes_total
    candidatos = public_candidatos()
    maiores_cand = candidatos.nlargest(5, columns='inscricoes_total') # aqui eu tenho todo o df
    print(maiores_cand[['cand_id', 'inscricoes_total', 'top_vaga_titulo', 'top_score']]) # eu selecionei apenas essas tres colunas contendo algumas informacoes relevantes
    print(f"Total de inscricoes: {len(candidatos[candidatos['inscricoes_total'] > 0])}")
    print()
    # imprimir as 5 vagas com o maior valor na coluna 'cands_total'
    vagas = public_vagas()
    maiores_vagas = vagas.nlargest(5, columns='cands_total')
    print(maiores_vagas[['vaga_id', 'cands_total']])    
    print(f"Total de candidatos: {len(vagas[vagas['cands_total'] > 0])}") # a saida mostra 4. significa que sao 4 vagas que possuem candidatura?

    # --- SMOKE CHECKS FINAIS ---
    print("\nIniciando smoke checks...")

    # Carregando as fontes de verdade para comparação
    df_candidatos_orig = pd.read_csv("data/samples/candidatos.csv")
    df_candidaturas_orig = pd.read_csv("data/outputs/candidaturas.csv")
    df_oportunidades_orig = pd.read_csv("data/samples/oportunidades.csv")

    # testes df candidatos    
    assert len(df_candidatos) == len(df_candidatos_orig)    
    assert int(df_candidatos['inscricoes_total'].sum()) == len(df_candidaturas_orig)
    print("candidatos: OK")

    # teste df vagas    
    assert len(df_vagas) == len(df_oportunidades_orig)    
    assert int(df_vagas["cands_total"].sum()) == len(df_candidaturas_orig)    
    scores_validos = df_vagas[df_vagas["top1_score"] > 0]
    assert scores_validos["top1_score"].between(0, 100).all()
    print("vagas: OK")

    # exportar JSONs -> chatGPT
    export_json(df_vagas, "data/outputs/public_vagas.json")
    export_json(df_candidatos, "data/outputs/public_candidatos.json")
    print("JSONs salvos em data/outputs/public_vagas.json e data/outputs/public_candidatos.json")

    def build_resumo(df_vagas: pd.DataFrame, df_cands: pd.DataFrame) -> str:
        total_vagas = len(df_vagas)
        vagas_com_cands = int((df_vagas["cands_total"] > 0).sum())

        total_cands = len(df_cands)
        cands_com_insc = int((df_cands["inscricoes_total"] > 0).sum())

        # faixa de scores válidos (>0)
        sc = df_vagas.loc[df_vagas["top1_score"] > 0, "top1_score"]
        score_min = float(sc.min()) if not sc.empty else 0.0
        score_max = float(sc.max()) if not sc.empty else 0.0

        urgentes = int((df_vagas["urgente"] == "sim").sum())
        status_counts = (
            df_vagas["status"].value_counts(dropna=False)
            .sort_index()
            .to_dict()
        )

        # Top 3 vagas por volume
        top_vagas = (
            df_vagas.nlargest(3, "cands_total")[["vaga_id", "titulo", "cands_total"]]
            .to_dict("records")
        )

        # Top 3 candidatos por inscrições
        top_cands = (
            df_cands.nlargest(3, "inscricoes_total")[["cand_id", "nome", "inscricoes_total", "top_vaga_titulo", "top_score"]]
            .to_dict("records")
        )

        linhas = []
        linhas.append("RESUMO — visões públicas\n--------------------------")
        linhas.append(f"Vagas: {total_vagas} (cobertas: {vagas_com_cands}) | Urgentes: {urgentes}")
        linhas.append(f"Candidatos: {total_cands} (com inscrições: {cands_com_insc})")
        linhas.append(f"Faixa de top scores: {score_min:.1f} – {score_max:.1f}")
        linhas.append(f"Status de vagas: {status_counts}")
        linhas.append("")
        linhas.append("Top 3 vagas por candidatos:")
        for r in top_vagas:
            linhas.append(f"- {r['vaga_id']} • {r['titulo']} — {int(r['cands_total'])} inscrições")
        linhas.append("")
        linhas.append("Top 3 candidatos por inscrições:")
        for r in top_cands:
            linhas.append(f"- {r['cand_id']} • {r['nome']} — {int(r['inscricoes_total'])} inscrições | melhor vaga: “{r['top_vaga_titulo']}” (score {r['top_score']:.1f})")
        linhas.append("")

        return "\n".join(linhas)

        
    # 3) Mini-resumo (txt legível)
    resumo_txt = build_resumo(df_vagas, df_candidatos)
    Path("data/outputs/public_resumo.txt").write_text(resumo_txt, encoding="utf-8")
    print("Resumo salvo em data/outputs/public_resumo.txt")

    

    
if __name__ == "__main__":
    main()