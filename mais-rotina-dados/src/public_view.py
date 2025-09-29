import pandas as pd

def public_vagas(path_o="data/samples/oportunidades.csv", path_c="data/outputs/candidaturas.csv") -> pd.DataFrame:
    

    df_o = pd.read_csv(path_o, dtype={"id": "string", "status": "string", "agencia_id": "string"})
    df_c = pd.read_csv(path_c, dtype={"vaga_id": "string", "cand_id": "string", "score": float})        
    cont_cand = df_c.groupby('vaga_id')['origem'].value_counts().unstack().reindex(columns=["sugestao","sorteio"], fill_value=0)
    print(cont_cand)  
    melhores_linhas = df_c.loc[df_c.groupby('vaga_id')['score'].idxmax()]
    top1_cand = melhores_linhas.set_index('vaga_id')[['cand_id', 'score']]        

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
        p_opotunidades="data/samples/oportunidades.csv"
) -> pd.DataFrame:
    
    df_candidatos = pd.read_csv(p_candidaturas, dtype={
        "vaga_id": "string", "cand_id": "string", "score": float, "origem": "string", "status": "string"
    })
       
    contagem_origem = (
        df_candidatos.groupby("cand_id")['origem']
        .value_counts()
        .unstack()
        .reindex(columns=['sugestao', 'sorteio'],fill_value=0)
        .fillna(0).astype(int) # limpar na origem dessa vez
    )
    

    

    

    


def main():

    public_candidatos()   
    




    """df = public_vagas()
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

    outp = "data/outputs/public_vagas.csv"
    df.to_csv(outp, index=False)
    print("salvo em:", outp)      
"""
if __name__ == "__main__":
    main()