from pathlib import Path
import yaml
from random import Random
import pandas as pd



def load_taxonomias(path='config/taxonomias.yml'): # carregar as taxonomias
    p = Path(path)
    tax = yaml.safe_load(p.read_text(encoding='utf-8'))
    #req = {"idiomas","habilidades","regioes","paises","tipos","status","risco_nivel",'redes_sociais'}
    req = {"objetivos","idiomas","habilidades","regioes","paises","tipos","status","risco_nivel","urgente"}
    faltando = req - set(tax)    
    #print(bool(faltando)) # debug
    assert not faltando, f"faltam chaves no YAML: {rng.choice}"
    return tax

def load_agencias(path='data/samples/agencias.csv') -> list: # carregar as agencias
    df = pd.read_csv(path)
    agencia_id = []
    for id in df.itertuples():
        status = str(id.status).strip().lower()
        if status == 'ativa':
            agencia_id.append(str(id.agencia_id).strip())        
    
    return agencia_id    

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


def gerar_oportunidades(rng, tax, n, agencias_id):
    """
    retornar um DF    
    """    
    registros = []

    if not agencias_id:
        raise ValueError("Lista de agencias_id está vazia. Verifique data/samples/agencias.csv.")

    for i in range(1, n+1):
        _, pais = choose_regiao_pais(rng, tax)
        id_ = f'V{i:03d}'
        status = pick_one(rng, tax['status'])
        tipo = pick_one(rng, tax['tipos'])
        habilidades_requeridas = pick_many(rng, tax['habilidades'], 1, 3)
        idiomas_requeridos = pick_many(rng, tax['idiomas'], 1, 2)
        pna = "sim" if rng.random() < 0.30 else "nao"    
        risco_nivel = pick_one(rng, tax['risco_nivel'])
        hab0_slug = habilidades_requeridas.split(",")[0]
        hab0 = hab0_slug.replace("_", " ").title()
        titulo = f"{hab0} em {pais.title()}"
        contato_url = f"https://contato.exemplo/{id_.lower()}"        
        agencia = rng.choice(agencias_id)
        vagas_total = rng.randint(5, 20)
        objetivos_csv = pick_many(rng, tax["objetivos"], 1, 2)
        objetivo0 = objetivos_csv.split(",")[0].replace("_", " ")
        descricao_curta = f"{hab0} em {pais.title()}; foco em {objetivo0}"
        choices = tax['urgente']
        probabilities = [0.20, 0.80]        
        urgente = rng.choices(population=choices, weights=probabilities, k=1)[0]

        linha = {
            "id": id_,
            "titulo": titulo,
            "pais": pais,
            "status": status,
            "tipo": tipo,
            "habilidades_requeridas": habilidades_requeridas,
            "idiomas_requeridos": idiomas_requeridos,
            "pna": pna,
            "risco_nivel": risco_nivel,
            "contato_url": contato_url,
            "agencia_id": agencia,
            "vagas_total": vagas_total,
            "objetivos": objetivos_csv,
            "descricao_curta": descricao_curta,
            "urgente": urgente,
        }
        registros.append(linha)        

    COLS = [
        "id",
        "titulo",
        "pais",
        "status",
        "tipo",
        "habilidades_requeridas",
        "idiomas_requeridos",
        "pna","risco_nivel",
        "contato_url",
        "agencia_id",
        "vagas_total",
        "objetivos",
        "descricao_curta",
        "urgente"
        ]

    return pd.DataFrame(registros)[COLS]


def gerar_candidatos(rng, tax, n):

    candidatos = []

    for i in range(1, n+1):

        id_ = f"C{i:03d}"
        nome = f"Cand_{i:03d}"
        email = f"candid_{i:03d}@exemplo.org"
        telefone = f"+974-7011-{i:04d}"
        habilidades = pick_many(rng, tax["habilidades"], 1, 3)
        idiomas = pick_many(rng, tax["idiomas"], 1, 2)
        regioes_preferidas = pick_many(rng, tax["regioes"], 1, 2)
        tipo = pick_one(rng, tax["tipos"])
        aceita_pna = "sim" if rng.random() < 0.6 else "nao"
        aceita_risco = "sim" if rng.random() < 0.4 else "nao"

        linha = {
            'id': id_,
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'habilidades': habilidades,
            'idiomas': idiomas,
            'regioes_preferidas': regioes_preferidas,
            'tipo': tipo,
            'aceita_pna': aceita_pna,
            'aceita_risco': aceita_risco
        }

        candidatos.append(linha)

    COLS = [
        'id',
        'nome',
        'email',
        'telefone',
        'habilidades',
        'idiomas',
        'regioes_preferidas',
        'tipo',
        'aceita_pna',
        'aceita_risco'
    ]

    return pd.DataFrame(candidatos)[COLS]
    
        
'''
rng.choice(items)
rng.sample(items, 2)
rng.randint(1, 3)
'''

if __name__ == "__main__":
    rng = Random(42)

    tax = load_taxonomias()
    agencias = load_agencias()

    df_o = gerar_oportunidades(rng, tax, n=20, agencias_id=agencias)
    df_c = gerar_candidatos(rng, tax, n=60)

    df_o.to_csv("data/samples/oportunidades.csv", index=False)
    df_c.to_csv("data/samples/candidatos.csv", index=False)

    # feedback rápido no console
    print(f"Oportunidades: {len(df_o)}  |  Candidatos: {len(df_c)}")
    print("Status das vagas:")
    print(df_o["status"].value_counts())
