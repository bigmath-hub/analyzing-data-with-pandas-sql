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


name = 'orange, banana, apple'

word_list = name.split(",")
print(word_list)

clear_words = [word.strip() for word in word_list]

print(set(clear_words))