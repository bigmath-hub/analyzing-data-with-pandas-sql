import yaml
from pathlib import Path
from random import Random


def load_taxonomias(path='config/taxonomias.yml'): # carregar as taxonomias
    p = Path(path)
    tax = yaml.safe_load(p.read_text(encoding='utf-8'))
    #req = {"idiomas","habilidades","regioes","paises","tipos","status","risco_nivel",'redes_sociais'}
    req = {"idiomas","habilidades","regioes","paises","tipos","status","risco_nivel"}
    faltando = req - set(tax)    
    print(bool(faltando)) # debug
    assert not faltando, f"faltam chaves no YAML: {faltando}"
    return tax     

def pick_one(rng, items): 
    return rng.choice(items)

def pick_many(rng, items, k_min=1, k_max=2):    
    k_max = min(k_max, len(items))
    k = rng.randint(k_min, k_max)    
    chosen = rng.sample(items, k)    
    chosen.sort()
    return ",".join(chosen)

def choose_regiao_pais(rng, tax):
    reg = pick_one(rng, tax['regioes'])
    pais = pick_one(rng, tax['paises'][reg])    
    return reg, pais

def gerar_oportunidades(rng, tax, n):
    """
    retornar um DF    
    """
    reg, pais = choose_regiao_pais(rng, tax)
    id = 'V{i:03d}'
    status = pick_one(rng, tax['status'])
    tipo = pick_one(rng, tax['tipos'])
    habilidades_requeridas = pick_many(rng, tax['habilidades'], 1, 3)
    idiomas_requeridos = pick_many(rng, tax['idiomas'], 1, 2)
    # pna = "sim" se rng.random() < p else "nao" (escolha um p; por exemplo, 0.3) nao entendi essa linha
    pna = 'sim'
    risco_nivel = pick_one(rng, tax['risco_nivel'])
    





'''
rng.choice(items)
rng.sample(items, 2)
rng.randint(1, 3)
'''

if __name__ == "__main__":  
    rng = Random(42)
    tax = load_taxonomias()    

    '''
    print("idiomas", len(tax['idiomas']))
    print('habilidades', len(tax['habilidades']))
    print('regioes', len(tax['regioes']))
    for reg, paises in tax['paises'].items():
        print(f"{reg}: {len(paises)} paises")
'''    
    items = ["a", "b", "c", "d"]
    print(pick_one(rng, items))
    print(pick_many(rng, items)) 

    for _ in range(5):
        reg, pais = choose_regiao_pais(rng, tax)
        print(f"{reg} --> {pais}")


