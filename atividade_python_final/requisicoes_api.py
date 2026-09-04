import json
import os
from datetime import date

import requests

API_URL = "https://api.adviceslip.com/advice"
CAMINHO_CACHE = os.path.join(os.path.dirname(__file__), ".frase_cache.json")
FRASE_PADRAO = "Pequenos progressos diarios constroem grandes conquistas."


def _ler_cache():
    try:
        with open(CAMINHO_CACHE, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _salvar_cache(dados):
    with open(CAMINHO_CACHE, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False)


def frase_motivacional():
    """Retorna a frase motivacional do dia.

    A frase e buscada na API publica do Advice Slip e guardada em cache
    para nao ser consumida novamente no mesmo dia (evita limites de uso).
    Se a API falhar, usa uma frase padrao.
    """
    hoje = date.today().isoformat()
    cache = _ler_cache()

    if cache.get("data") == hoje and cache.get("frase"):
        return cache["frase"]

    frase = None
    try:
        resposta = requests.get(API_URL, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        frase = dados.get("slip", {}).get("advice")
    except requests.RequestException:
        frase = None

    frase = frase.strip() if frase else FRASE_PADRAO
    _salvar_cache({"data": hoje, "frase": frase})
    return frase