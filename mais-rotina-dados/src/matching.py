import pandas as pd
from pathlib import Path
import yaml
from gen_dados import load_taxonomias

def main():
    cfg = load_cfg("config/padroes.yml")
    tax = load_taxonomias()
    df_o = pd.read_csv("data/samples/oportunidades.csv")
    df_c = pd.read_csv("data/samples/candidatos.csv")

    for i in range(3):        # 3 vagas
        for j in range(3):    # 3 candidatos
            s = score_pair(df_o.iloc[i], df_c.iloc[j], cfg, tax)
            print(df_o.iloc[i]["id"], df_c.iloc[j]["id"], "=>", s)

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

def to_set(cell) -> set[str]:
    # se entrada vazia retorna um conjunto vazio
    if not cell:
        return set()              
        
    # lista contendo os itens de entrada
    parts = str(cell).split(",")    
    
    # remover os espacos e padronizar os nomes
    trimmed = [p.strip().lower() for p in parts]    
    
    # remove os itens vazios e normaliza os campos
    filtered = [p for p in trimmed if p]

    return set(filtered) # retorna um set      

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
        must_have_w = to_set(cfg["matching"]["must_have"].get("idiomas"))
        print(type(must_have_w), must_have_w)
        must_have = set(cfg["matching"]["must_have"].get("idiomas"))
        print(type(must_have), must_have)
        cand = to_set(cand_row["idiomas"])        
        if not must_have.issubset(cand):
            
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

    print("comp:", s_hab, s_idi, s_reg, s_bon)


    return score

if __name__ == "__main__":
    main()