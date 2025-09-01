import yaml
from pathlib import Path

def main():
    text = read_yaml_text('config/padroes.yml')
    cfg_dict = parse_yaml(text)
    cfg = load_cfg(cfg_dict)
    print(cfg["matching"]["pesos"])    
    print(sum(cfg["matching"]["pesos"].values()))
    
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

def load_cfg(file_dict: dict) -> dict:
    try:
        matching = file_dict['matching']
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
        
    count = 0
    for value in file_dict['matching']['pesos'].values():
        count += value
    if not abs(count - 1.0) < 1e-9:
        raise ValueError(f"Soma dos pesos deve ser ~1.0 e foi {count}")
        
    if 'must_have' not in matching:
        matching['must_have'] = {}

    return file_dict   


if __name__ == "__main__":
    main()