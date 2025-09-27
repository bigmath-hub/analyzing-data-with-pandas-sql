import pandas as pd

def public_vagas(path_o="data/samples/oportunidades.csv", path_c="data/outputs/candidaturas.csv") -> pd.DataFrame:

    # Leia as duas tabelas, garanta tipos (vaga_id/cand_id como string; score como float)

    df_o = pd.read_csv(path_o, dtype={"id": "string", "status": "string", "agencia_id": "string"})
    df_c = pd.read_csv(path_c, dtype={"vaga_id": "string", "cand_id": "string", "score": float})
    
    df_c.groupby('origem')

    return df_c

    
    
    
    
    # cands_sugestao: num. de linhas da candidatura com origem == "sugestao"

    # cands_sorteio: num. de linhas da candidatura com origem == "sorteio"

    # cands_total: soma

    # top1_cand_id: cand_id do maior score daquela vaga

    # top1_score: score do candidato

    
    


def main():
    print(public_vagas())


if __name__ == "__main__":
    main()