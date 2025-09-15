from random import Random
"""
oportunidades = {
    'id': 'name0',
    'titulo': 'name1',
    'pais': 'name2',
    'status': 'publicada', # rascunho | publicada | em_selecao | preenchida | expirada
    'tipo': 'local', # local (s/ viagem) | curto (<=2sem) | medio (2<8sem) | longo (>8sem) 
    'habilidades_requeridas': ['logistica','ensino_biblico'], 
    'idiomas_requeridos': ['ingles','arabe_basico'],
    'pna': 'nao', # sim | nao
    'risco_nivel': 'baixo', # baixo | medio | alto
    'contato_url': 'name8'
}

candidatos = {
    'id': 'name0',
    'nome': 'name1',
    'email': 'name2',
    'telefone': 'name3',
    'habilidades': ['lista','csv'],
    'idiomas': ['lista','csv'],
    'regioes_preferidas': ['lista','csv'],
    'tipo': ['enum','local','curto','medio','longo'],
    'aceita_pna': ['sim','nao'],
    'aceita_risco':['sim','nao']
}

id (str)
nome (str)
email (str)
telefone (str)
habilidades (lista csv, ex.: logistica,ensino_biblico)
idiomas (lista csv, ex.: ingles,arabe_basico)
regioes_preferidas (lista csv, ex.: mena,africa_norte)
tipo (enum string: local|curto|medio|longo)
aceita_pna (enum string: sim|nao)
aceita_risco (enum string: sim|nao)

C1,jesus_cristo,jc@heaven.com,+333-333-3333,"unisciente,unipresente,unipotente","ingles,arabe_basico","america_sul,asia_sul",longo,sim,sim

from random import Random

def pick_one(rng, items): 
    return rng.choice(items)

def pick_many(rng, items, k_min=1, k_max=2):    
    k_max = min(k_max, len(items))
    k = rng.randint(k_min, k_max)    
    chosen = rng.sample(items, k)
    chosen.sort()
    return ",".join(chosen)

#def choose_regiao_pais()



rng.choice(items)
rng.sample(items, 2)
rng.randint(1, 3)


if __name__ == '__main__':
    rng = Random(42)
    items = ["a", "b", "c", "d"]
    print(pick_one(rng, items))
    print(pick_many(rng, items)) 
"""




"""
name = 'assange'
file = open('names.txt', "a")
file.write(f"{name}\n")
file.close()

with open('names.txt', 'a') as file:
    file.write(f"{name}\n")

"""
"""
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

print(to_set("ingles,arabe_basico"))
print(to_set("  ingles ,  arabe_basico ,,  "))
print(to_set(""))

"""
"""
name = 'orange, banana, apple'

word_list = name.split(",")
print(word_list)

clear_words = [word.strip() for word in word_list]

print(set(clear_words))"""


"""from src.gen_dados import load_taxonomias

def pais_para_regiao(tax: dict, pais: str) -> str | None:
    for raw in tax['paises'].items():
        if pais in raw[1]:
            return raw[0]


tax = load_taxonomias()
print(pais_para_regiao(tax, "jordania"))
print(pais_para_regiao(tax, "egito"))
print(pais_para_regiao(tax, "brasil"))
print(pais_para_regiao(tax, "canada"))   # fora da taxonomia → None


mena
africa_norte
america_sul
None
"""

"""set1 = {'logistica', 'ensino_biblico'}
set2 = {'logistica'}

sub_set = set1 - set2

print(sub_set)

# preciso aplicar a formula para obter o fator
factor = len(sub_set) / len(set1)
print(factor)"""


"""def to_set(cell) -> set[str]:
    if cell is None:
        return set()

    if isinstance(cell, (list, tuple, set)):
        return [for x in cell if ]

    

print(to_set(['mat  ,    d, s']))
print(to_set(['mat'  ,    'd', 's']))
print(to_set(('mat', 'silva', 'dd')))
print(to_set({'mat', 'silva', 'dd'}))
print(to_set('matt silva dilly'))"""


"""fruits = ['apple  ', '   banana', '   apple   ', ' orange', 'banana', 'apple']

f = {str(x).strip().lower() for x in fruits if str(x).strip()}

fruit_set = set()
for fruit in fruits:
    if str(fruit).strip():
        fruit_set.add(str(fruit).strip().lower())
print(fruit_set)
    


print(f)"""
"""
def to_set(var) -> set[str]:
        
    if var is None:
        return set()

    if isinstance(var, (set, list, tuple)):
        return {str(x).strip().lower() for x in var if str(x).strip()}    
    
    s = str(var).strip()
    if not s:
        return set()
    return {x.strip().lower() for x in s.split(",") if x.strip()}


print(to_set(["ingles"]))                # {'ingles'}
print(to_set("ingles,frances"))          # {'ingles', 'frances'}
print(to_set("  ingles ,  arabe_basico ,,  "))  # {'ingles', 'arabe_basico'}
print(to_set(None))                      # set()
"""

rng = Random(42)

choices = ['head', 'tail']
probabilidades = [0.50, 0.50]

design = {
        'novo': 0.45, 
        'em_andamento': 0.25, 
        'entrevistado': 0.10,
        'aguardando_resposta': 0.10,
        'aprovado': 0.07,
        'rejeitado': 0.03
    }

#print(list(design.keys()))


for _ in range(10):
    print(rng.choices(population=list(design.keys()), weights=design.values(), k=1)[0])
        
            
            