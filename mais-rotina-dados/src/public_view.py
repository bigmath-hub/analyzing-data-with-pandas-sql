import pandas as pd

def public_vagas(path_o="data/samples/oportunidades.csv", path_c="data/outputs/candidaturas.csv") -> pd.DataFrame:
    

    df_o = pd.read_csv(path_o, dtype={"id": "string", "status": "string", "agencia_id": "string"})
    df_c = pd.read_csv(path_c, dtype={"vaga_id": "string", "cand_id": "string", "score": float})        
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
    
    df_candidaturas = pd.read_csv(p_candidaturas, dtype={
        "vaga_id": "string", "cand_id": "string", "score": float, "origem": "string", "status": "string"
    })

    df_candidatos = pd.read_csv(p_candidatos, dtype="string")
    df_oportunidades = pd.read_csv(p_oportunidades, dtype="string")
    
    
    contagem_origem = (
        df_candidaturas.groupby("cand_id")['origem']
        .value_counts()
        .unstack()
        .reindex(columns=['sugestao', 'sorteio'],fill_value=0)
        .fillna(0).astype(int) # limpar na origem dessa vez
    )    
        
    contagem_origem['total_vagas'] = contagem_origem.sum(axis=1) 
    print(contagem_origem)
    
    melhores_linhas = df_candidaturas.iloc[df_candidaturas.groupby('vaga_id')['score'].idxmax()]
    print(melhores_linhas)
    
    df_intermediario = melhores_linhas.drop(['cand_id', 'status', 'origem'], axis=1) 
    
    #df_merge = pd.merge(df_oportunidades, df_intermediario, how='left', left_on='id', right_index=True)
    
    
    
    

    

    

    

    

    


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