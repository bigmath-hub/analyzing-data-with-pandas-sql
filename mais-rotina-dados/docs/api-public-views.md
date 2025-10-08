# Visões públicas — contrato (estático)

Este documento descreve os arquivos JSON estáticos que o front-end pode consumir.  
Eles são gerados no repositório de dados e **copiados para** `public/api/` deste projeto.

## Arquivos publicados

- `public/api/public_vagas.json` — lista de vagas com contadores de candidaturas e melhor candidato (top1).
- `public/api/public_candidatos.json` — lista de candidatos com total de inscrições e melhor vaga (top1).
- `public/api/public_index.json` — mini-resumo com contagens gerais e faixa de scores.

Formato: JSON UTF-8, números sem aspas, strings em minúsculas quando forem “flags” (ex.: `urgente`).

---

## `public_vagas.json` (array de objetos)

**Campos e tipos**

| campo             | tipo            | descrição                                                                 |
|-------------------|-----------------|---------------------------------------------------------------------------|
| `vaga_id`         | string          | ID da vaga (ex.: `"V010"`).                                              |
| `titulo`          | string          | Título formatado (ex.: `"Evangelismo em Quenia"`).                        |
| `pais`            | string          | País em minúsculas (ex.: `"quenia"`).                                     |
| `agencia_id`      | string          | ID da agência (ex.: `"A004"`).                                            |
| `status`          | string          | Um de: `rascunho`, `publicada`, `em_selecao`, `preenchida`, `expirada`.   |
| `urgente`         | string          | `"sim"` ou `"nao"`.                                                       |
| `vagas_total`     | number          | Número total de posições abertas na vaga.                                 |
| `cands_sugestao`  | number          | Qtde de candidaturas vindas de **sugestão**.                              |
| `cands_sorteio`   | number          | Qtde de candidaturas vindas de **sorteio**.                               |
| `cands_total`     | number          | Soma: `cands_sugestao + cands_sorteio`.                                   |
| `top1_cand_id`    | string \| ""    | ID do melhor candidato (maior score) ou string vazia se não houver.       |
| `top1_score`      | number \| 0.0   | Score do melhor candidato (0.0 quando não houver).                        |

**Exemplo (um item):**
```json
{
  "vaga_id": "V010",
  "titulo": "Evangelismo em Quenia",
  "pais": "quenia",
  "agencia_id": "A004",
  "status": "em_selecao",
  "urgente": "nao",
  "vagas_total": 9,
  "cands_sugestao": 2,
  "cands_sorteio": 1,
  "cands_total": 3,
  "top1_cand_id": "C057",
  "top1_score": 97.5
}
