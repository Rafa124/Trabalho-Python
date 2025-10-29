"""Funções utilitárias para carregar e salvar dados em JSON."""

import json
from typing import Any, List


def carregar_dados(caminho_arquivo: str) -> List[Any]:
    """Lê um arquivo JSON e retorna uma lista de registros.

    Caso o arquivo não exista ou esteja corrompido, devolve uma lista vazia.
    """

    try:
        # Tenta abrir o arquivo pra leitura
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            # Lê o conteúdo JSON do arquivo
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver com erro, devolve lista vazia
        return []

    # Se os dados forem uma lista, devolve ela
    if isinstance(dados, list):
        return dados

    # Se não for lista, devolve lista vazia
    return []


def salvar_dados(dados: List[Any], caminho_arquivo: str) -> None:
    """Salva uma lista de registros em um arquivo JSON com indentação."""

    # Abre o arquivo pra escrita (cria se não existir, sobrescreve se existir)
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        # Salva os dados em formato JSON bonito (com indentação de 2 espaços)
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)