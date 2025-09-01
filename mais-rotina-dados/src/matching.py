import yaml
from pathlib import Path

def main():
    cfg = load_cfg('config/padroes.yml')
    print(validate_cfg(cfg))
    print(f"pesos: {cfg['matching']['pesos']}")
    print(f"SOMA_PESOS {sum(cfg['matching']['pesos'].values())}")


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
        


if __name__ == "__main__":
    main()