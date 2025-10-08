from pathlib import Path
import json
import pandas as pd
import numpy as np

# importa as visões já prontas
from .public_view import public_vagas, public_candidatos



API_DIR = Path("public/api")


def _df_to_records(df: pd.DataFrame):
    # Substitui NaN/NaT por None (JSON válido)
    clean = df.replace({np.nan: None})
    return clean.to_dict(orient="records")


def _save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _build_index(vagas: pd.DataFrame, candidatos: pd.DataFrame) -> dict:
    # Totais
    vagas_total = int(len(vagas))
    vagas_cobertas = int((vagas["cands_total"] > 0).sum())
    urgentes = int((vagas["urgente"].astype(str).str.lower() == "sim").sum())

    candidatos_total = int(len(candidatos))
    cand_com_insc = int((candidatos["inscricoes_total"] > 0).sum())

    # Faixa de scores > 0
    scores = vagas.loc[vagas["top1_score"] > 0, "top1_score"]
    if len(scores) == 0:
        s_min = None
        s_max = None
    else:
        s_min = float(scores.min())
        s_max = float(scores.max())

    return {
        "totals": {
            "vagas": vagas_total,
            "vagas_cobertas": vagas_cobertas,
            "urgentes": urgentes,
            "candidatos": candidatos_total,
            "candidatos_com_inscricoes": cand_com_insc,
        },
        "top_scores": {
            "min": s_min,
            "max": s_max,
        },
    }


def main():
    # gera dataframes das visões
    df_vagas = public_vagas()
    df_cands = public_candidatos()

    # salva JSONs principais
    _save_json(API_DIR / "public_vagas.json", _df_to_records(df_vagas))
    _save_json(API_DIR / "public_candidatos.json", _df_to_records(df_cands))

    # salva índice/resumo
    index_payload = _build_index(df_vagas, df_cands)
    _save_json(API_DIR / "public_index.json", index_payload)

    print("OK -> public/api/public_vagas.json")
    print("OK -> public/api/public_candidatos.json")
    print("OK -> public/api/public_index.json")


if __name__ == "__main__":
    main()
