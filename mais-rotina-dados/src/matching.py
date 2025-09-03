from pathlib import Path
import yaml
from gen_dados import load_taxonomias

def main():
    print(overlap_requeridos("logistica,ensino_biblico", "logistica"))        # 0.5
    print(overlap_requeridos("ingles,arabe_basico", "frances,ingles"))        # 0.5
    print(overlap_requeridos("", "qualquer,coisa"))                            # 1.0

    tax = load_taxonomias()
    print(regiao_hit("jordania", "mena,asia_sul", tax))   # 1.0
    print(regiao_hit("egito", "america_sul", tax))        # 0.0

    print(bonus_val("sim","alto","sim","nao"))   # 0.5
    print(bonus_val("nao","baixo","sim","sim"))  # 0.0
    print(bonus_val("sim","medio","sim","sim"))  # 1.0


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

def to_set(cell: str) -> set[str]:
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

if __name__ == "__main__":
    main()