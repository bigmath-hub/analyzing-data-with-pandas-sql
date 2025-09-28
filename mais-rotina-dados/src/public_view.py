import pandas as pd

def public_vagas(path_o="data/samples/oportunidades.csv", path_c="data/outputs/candidaturas.csv") -> pd.DataFrame:
    

    df_o = pd.read_csv(path_o, dtype={"id": "string", "status": "string", "agencia_id": "string"})
    df_c = pd.read_csv(path_c, dtype={"vaga_id": "string", "cand_id": "string", "score": float})    
    cont_cand = df_c.groupby('vaga_id')['origem'].value_counts().unstack().fillna(0).astype(int)
    cont_cand = cont_cand.reindex(columns=["sugestao","sorteio"], fill_value=0) # edge case - by chatGPT
    melhores_linhas = df_c.loc[df_c.groupby('vaga_id')['score'].idxmax()]
    top1_cand = melhores_linhas.set_index('vaga_id')[['cand_id', 'score']]    
    #df_merged = pd.merge(top1_cand, df_o, how='left', left_on='vaga_id', right_on='id')
    df_merge1 = pd.merge(df_o, cont_cand, how='left', left_on='id', right_index=True)
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
    


def main():
    df = public_vagas()
    print(f"Number of rows df: {len(df)}")    
    df_o = pd.read_csv("data/samples/oportunidades.csv")
    print(f"Number of rows oportunidades.csv: {len(df_o)}")    
    check_sum = (df['cands_total'] == (df['cands_sugestao'] + df['cands_sorteio'])).all()
    print(f"A soma de cands_total está correta em todas as linhas? {check_sum}")
    len_cands_total = len(df[df['cands_total'] > 0])
    top1_score_max = df[df['top1_score'] > 0]['top1_score'].max()
    top1_score_min = df[df['top1_score'] > 0]['top1_score'].min()
    
    print("cands_total:", len_cands_total)

    print("top1_score_max:", top1_score_max)    
    print("top1_score_min:", top1_score_min)
    
    
    

if __name__ == "__main__":
    main()