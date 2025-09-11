import pandas as pd
from pathlib import Path
import yaml
from gen_dados import load_taxonomias

def main():
    cfg = load_cfg("config/padroes.yml")
    tax = load_taxonomias()
    df_o = pd.read_csv("data/samples/oportunidades.csv")
    df_c = pd.read_csv("data/samples/candidatos.csv")
    
    cand = match_all(df_o, df_c, cfg, tax)    

    cand.to_csv("data/outputs/sugestoes.csv", index=False)    
    print("Arquivo salvo em: data/outputs/sugestoes.csv\n")    
    print(tax)

def load_cfg(path: str) -> dict:
    texto = read_yaml_text(path)
    cfg = parse_yaml(texto)    
    cfg_ok = validate_cfg(cfg)

    return cfg

def read_yaml_text(path: str) -> str:
    config_file_path = Path(path)
    try:    
        file_string = config_file_path.read_text(encoding='utf-8')    
    except:
        raise FileNotFoundError(f"Error: o arquivo '{config_file_path}' nao encontrado.")
            
    return file_string

def parse_yaml(file_string: str) -> dict:
    config_data = yaml.safe_load(file_string)
    return config_data


def validate_cfg(cfg: dict) -> str:
    try:
        matching = cfg['matching']
    except KeyError:
        raise ValueError("Deve conter 'matching' key")
        
    try:
        pesos = matching['pesos']
        threshold_padrao = matching['threshold_padrao']
    except KeyError as e:
        raise ValueError(f"Chave requerida nao encontrada em 'matching {e}")             
        
    required = {"habilidades", "idiomas", "regiao", "bonus"}        
    check_required = set(pesos.keys())

    if check_required != required:
        raise ValueError("Erro nas chaves requeridas em 'matching['pesos']")            
        
    soma = 0
    for value in cfg['matching']['pesos'].values():
        soma += value
    if not abs(soma - 1.0) < 1e-9:
        raise ValueError(f"Soma dos pesos deve ser ~1.0 e foi {soma}")
        
    if 'must_have' not in matching:
        matching['must_have'] = {}

    return f"CFG_OK"

def to_set(var) -> set[str]:

    if var is None:
        return set()

    if isinstance(var, (set, list, tuple)):
        return {str(x).strip().lower() for x in var if str(x).strip()}    

    s = str(var).strip()
    if not s:
        return set()
    return {x.strip().lower() for x in s.split(",") if x.strip()} 

def pais_para_regiao(tax: dict, pais: str) -> str | None:
    for raw in tax['paises'].items():
        if pais in raw[1]:
            return raw[0]

def overlap_requeridos(req_csv: str, have_csv: str) -> float:    
    required = to_set(req_csv)
    have = to_set(have_csv)

    inter = required & have

    if len(required) == 0:
        return 1.0

    fator = len(inter) / len(required)
    return fator

def regiao_hit(vaga_pais, cand_regioes_csv, tax) -> float:    
    vaga_regioes = pais_para_regiao(tax, vaga_pais) # regiao disponivel para a vaga -> str
    cand_regioes = to_set(cand_regioes_csv) # disponibilidade do candidato -> set()

    if vaga_regioes in cand_regioes:
        return 1.0

    return 0.0

def bonus_val(o_pna, o_risco, c_aceita_pna, c_aceita_risco) -> float:    
    b1 = 1.0 if o_pna=='sim' and c_aceita_pna=='sim' else 0.0
    b2 = 1.0 if o_risco in {'medio', 'alto'} and c_aceita_risco=='sim' else 0.0

    return (b1 + b2) / 2

def score_pair(vaga_row, cand_row, cfg, tax):
    # ler os pesos
    w = cfg['matching']['pesos']
    # se existir must have
    if cfg["matching"]["must_have"].get("idiomas"):
        mh_list = cfg["matching"]["must_have"].get("idiomas")
        must_have = to_set(mh_list)       
        cand = to_set(cand_row["idiomas"])        
        if must_have and not must_have.issubset(cand):
            return 0.0

    # componentes do score
    s_hab = overlap_requeridos(
        vaga_row['habilidades_requeridas'], cand_row['habilidades']
    )    
    s_idi = overlap_requeridos(
        vaga_row['idiomas_requeridos'], cand_row['idiomas']
    )
    s_reg = regiao_hit(vaga_row['pais'], cand_row['regioes_preferidas'], tax)
    s_bon = bonus_val(
        vaga_row['pna'], vaga_row['risco_nivel'],
        cand_row['aceita_pna'], cand_row['aceita_risco']
    )
    raw = w["habilidades"]*s_hab + w["idiomas"]*s_idi + w['regiao']*s_reg + w['bonus']*s_bon
    score = round(100*raw, 1)

    return score

def match_all(df_o, df_c, cfg, tax) -> pd.DataFrame:
    TH = cfg["matching"]["threshold_padrao"]
    vagas_validas = df_o[df_o["status"].isin(["publicada","em_selecao"])] 
    valid = vagas_validas.reset_index(drop=True)
    regs = []

    for v in range(len(valid)):
        for c in range(len(df_c)):
            s = score_pair(valid.iloc[v], df_c.iloc[c], cfg, tax)
            if s >= TH:
                regs.append({"vaga_id": valid.iloc[v]['id'], "cand_id": df_c.iloc[c]["id"], "score": s})
    
    out = pd.DataFrame(regs).sort_values(["vaga_id","score"], ascending=[True,False])

    TOTAL_PARES = len(valid) * len(df_c)
    APROVADOS = len(out)
    VAGAS_COBERTAS = out['vaga_id'].nunique()
    

    print()
    print("Resumo:")
    print("-------")
    print(out.head(5))
    print()
    print("Total de pares:", TOTAL_PARES)
    print("Aprovados:", APROVADOS)
    print("Vagas Cobertas:", VAGAS_COBERTAS)
    print()
    
    return out

if __name__ == "__main__":
    main()