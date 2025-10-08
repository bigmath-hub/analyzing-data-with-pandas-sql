import pandas as pd

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
            index='df_o['id'],
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
            .astype(int)
        )

        # melhor candidato por vaga
        idx = df_c.groupby('vaga_id')['score'].idxmax()
        top1 = (
            df_c.loc[idx, ['vaga_id', 'cand_id', 'score']]
            .set_index['vaga_id']
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
    base['cand'] = base['cand'].fillna("").astype("string")
    
    base['cands_total'] = base['sugestao'] + base['sorteio']

    # renomear
    ren = {
        'id': 'vaga_id',
        'sugestao': 'cands_sugestao'
    }


    cont_cand = df_c.groupby('vaga_id')['origem'].value_counts().unstack().reindex(columns=["sugestao","sorteio"], fill_value=0)    
    melhores_linhas = df_c.loc[df_c.groupby('vaga_id')['score'].idxmax()]
    top1_cand = melhores_linhas.set_index('vaga_id')[['cand_id', 'score']]        
    
    print(df_o) # id
    print(df_o.dtypes) # id
    print()
    print(cont_cand) # vaga_id
    print(cont_cand.dtypes) # vaga_id
    

    df_merge1 = pd.merge(df_o, cont_cand, how='left', left_on='id', right_index=True)
    df_merge1[['sugestao', 'sorteio']] = df_merge1[['sugestao', 'sorteio']].fillna(0).astype(int)
    df = pd.merge(df_merge1, top1_cand, how='left', left_on='id', right_index=True)
    df['cands_total'] = df['sugestao'] + df['sorteio']

    colunas_renomear = {
        'id': 'vaga_id',
        'sugestao': 'cands_sugestao',
        'sorteio': 'cands_sorteio',
        'cand_id': 'top1_cand_id',
        'score': 'top1_score',
        'status_x': 'status'
    }
    df = df.rename(columns=colunas_renomear)

    colunas_finais = [
        'vaga_id', 'titulo', 'pais', 'agencia_id', 'status', 'urgente', 'vagas_total',
        'cands_sugestao', 'cands_sorteio', 'cands_total',
        'top1_cand_id', 'top1_score'
    ]

    df_final = df[colunas_finais]

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
    # objetivo: encontrar os 5 candidatos com > inscricoes_total
    candidatos = public_candidatos()
    maiores_cand = candidatos.nlargest(5, columns='inscricoes_total') # aqui eu tenho todo o df
    print(maiores_cand[['cand_id', 'top_vaga_id', 'top_score']]) # eu selecionei apenas essas tres colunas contendo algumas informacoes relevantes
    

if __name__ == "__main__":
    main()