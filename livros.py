"""Operações relacionadas aos livros cadastrados."""

from typing import Dict, List, Optional


def cadastrar_livro() -> Optional[Dict[str, int | str]]:
    """Solicita dados de um livro e devolve o registro formatado."""

    # Pede os dados do livro pro usuário
    titulo = input("Digite o título do livro: ").strip()
    autor = input("Digite o primeiro autor do livro: ").strip()
    ano = input("Digite o ano de publicação: ").strip()
    exemplares = input("Digite o número de exemplares: ").strip()

    # Verifica se o ano é um número válido
    if not ano.isdigit():
        print(" Ano inválido! Digite apenas números.")
        return None

    # Verifica se o número de exemplares é válido
    if not exemplares.isdigit():
        print(" Número de exemplares inválido! Digite apenas números.")
        return None

    # Formata o título com primeiras letras maiúsculas
    titulo_formatado = titulo.title()
    # Formata o nome do autor
    autor_formatado = " ".join(parte.capitalize() for parte in autor.split())

    # Cria um dicionário com as informações do livro
    livro = {
        "título": titulo_formatado,
        "autor": autor_formatado,
        "ano": int(ano),
        "exemplares": int(exemplares),
    }

    print(f" Livro '{titulo_formatado}' cadastrado com sucesso!\n")
    return livro


def listar_livros(lista_livros: List[Dict[str, int | str]]) -> None:
    """Mostra a listagem atual de livros cadastrados."""

    # Se não tem nenhum livro, mostra mensagem e para
    if not lista_livros:
        print(" Nenhum livro cadastrado ainda.\n")
        return

    # Mostra o cabeçalho
    print("\n=== Lista de Livros Cadastrados ===")
    # Percorre todos os livros e mostra as informações
    for indice, livro in enumerate(lista_livros, start=1):
        print(
            f"{indice}. Título: {livro['título']} | Autor: {livro['autor']} | "
            f"Ano: {livro['ano']} | Exemplares: {livro['exemplares']}"
        )
    print("===================================\n")


def encontrar_livro_por_titulo(
    lista_livros: List[Dict[str, int | str]], titulo: str
) -> Optional[Dict[str, int | str]]:
    """Procura um livro pelo título (case-insensitive)."""

    # Percorre todos os livros
    for livro in lista_livros:
        # Compara os títulos sem diferenciar maiúsculas/minúsculas
        if livro["título"].lower() == titulo.lower():
            return livro
    # Se não encontrar, retorna None
    return None


def buscar_livros_por_titulo(
    lista_livros: List[Dict[str, int | str]], termo: str
) -> List[Dict[str, int | str]]:
    """Retorna livros cujo título contém o termo informado."""

    # Arruma o termo de busca (remove espaços e deixa minúsculo)
    termo_normalizado = termo.strip().lower()
    # Se o termo estiver vazio, não procura nada
    if not termo_normalizado:
        return []

    # Cria uma lista com os livros que contêm o termo no título
    return [
        livro
        for livro in lista_livros
        if termo_normalizado in livro["título"].lower()
    ]


def buscar_livros_por_autor(
    lista_livros: List[Dict[str, int | str]], termo: str
) -> List[Dict[str, int | str]]:
    """Retorna livros cujo autor contém o termo informado."""

    # Arruma o termo de busca (remove espaços e deixa minúsculo)
    termo_normalizado = termo.strip().lower()
    # Se o termo estiver vazio, não procura nada
    if not termo_normalizado:
        return []

    # Cria uma lista com os livros que contêm o termo no nome do autor
    return [
        livro
        for livro in lista_livros
        if termo_normalizado in livro["autor"].lower()
    ]


def decrementar_exemplares_livro(
    titulo: str, lista_livros: List[Dict[str, int | str]]
) -> None:
    """Reduz em uma unidade o número de exemplares, se disponível."""

    # Procura o livro pelo título
    livro = encontrar_livro_por_titulo(lista_livros, titulo)
    # Se encontrou o livro E ele tem exemplares disponíveis
    if livro and livro["exemplares"] > 0:
        # Diminui 1 exemplar
        livro["exemplares"] -= 1


def incrementar_exemplares_livro(
    titulo: str, lista_livros: List[Dict[str, int | str]]
) -> None:
    """Aumenta em uma unidade o número de exemplares de um livro."""

    # Procura o livro pelo título
    livro = encontrar_livro_por_titulo(lista_livros, titulo)
    # Se encontrou o livro
    if livro:
        # Aumenta 1 exemplar
        livro["exemplares"] += 1