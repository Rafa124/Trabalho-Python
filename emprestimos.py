"""Operações de empréstimo e devolução de livros."""

from datetime import datetime
from typing import Dict, List

from livros import (
    decrementar_exemplares_livro,
    encontrar_livro_por_titulo,
    incrementar_exemplares_livro,
)
from usuarios import encontrar_usuario_por_cpf


def listar_emprestimos(lista_emprestimos: List[Dict[str, str]]) -> None:
    """Mostra os empréstimos correntes no console."""

    # Se não tem empréstimos, mostra mensagem e para
    if not lista_emprestimos:
        print(" Nenhum empréstimo registrado no momento.\n")
        return

    # Mostra o cabeçalho
    print("\n=== Empréstimos Atuais ===")
    # Percorre e mostra cada empréstimo
    for indice, emprestimo in enumerate(lista_emprestimos, start=1):
        print(
            f"{indice}. CPF: {emprestimo['cpf_usuario']} | Livro: {emprestimo['titulo_livro']} | "
            f"Data: {emprestimo['data_emprestimo']}"
        )
    print("==========================\n")


def emprestar_livro(
    lista_usuarios: List[Dict[str, str]],
    lista_livros: List[Dict[str, int | str]],
    lista_emprestimos: List[Dict[str, str]],
) -> bool:
    """Registra o empréstimo de um livro se dados válidos forem informados."""

    # Pede o CPF do usuário que quer pegar o livro
    cpf = input("Digite o CPF do usuário: ").strip()
    # Pede o título do livro que vai ser emprestado
    titulo = input("Digite o título do livro: ").strip().title()

    # Procura se o usuário existe na lista
    usuario = encontrar_usuario_por_cpf(lista_usuarios, cpf)
    if usuario is None:
        print(" Usuário não encontrado! Cadastre o usuário primeiro.\n")
        return False

    # Procura se o livro existe na lista
    livro = encontrar_livro_por_titulo(lista_livros, titulo)
    if livro is None:
        print(" Livro não encontrado! Cadastre o livro primeiro.\n")
        return False

    # Verifica se tem exemplares disponíveis
    if livro["exemplares"] <= 0:
        print(" Não há exemplares disponíveis para empréstimo!\n")
        return False

    # Diminui 1 exemplar do livro
    decrementar_exemplares_livro(titulo, lista_livros)

    # Cria um novo registro de empréstimo com data e hora atual
    emprestimo = {
        "cpf_usuario": cpf,
        "titulo_livro": titulo,
        "data_emprestimo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Adiciona o empréstimo na lista
    lista_emprestimos.append(emprestimo)
    print(f" Empréstimo realizado com sucesso para {usuario['nome']}!\n")
    return True


def devolver_livro(
    lista_livros: List[Dict[str, int | str]],
    lista_emprestimos: List[Dict[str, str]],
) -> bool:
    """Remove o empréstimo e devolve o exemplar ao acervo."""

    # Pede o CPF do usuário que está devolvendo
    cpf = input("Digite o CPF do usuário: ").strip()
    # Pede o título do livro que está sendo devolvido
    titulo = input("Digite o título do livro devolvido: ").strip().title()

    # Procura o empréstimo na lista
    for indice, emprestimo in enumerate(lista_emprestimos):
        # Verifica se é o mesmo CPF
        mesmo_usuario = emprestimo["cpf_usuario"] == cpf
        # Verifica se é o mesmo livro (comparando sem diferenciar maiúsculas/minúsculas)
        mesmo_livro = emprestimo["titulo_livro"].lower() == titulo.lower()

        # Se encontrou o empréstimo correto
        if mesmo_usuario and mesmo_livro:
            # Devolve o exemplar pro acervo (aumenta 1)
            incrementar_exemplares_livro(emprestimo["titulo_livro"], lista_livros)
            # Remove o empréstimo da lista
            lista_emprestimos.pop(indice)
            print(" Livro devolvido com sucesso!\n")
            return True

    # Se não encontrou o empréstimo
    print(" Não encontramos esse empréstimo. Confira os dados digitados.\n")
    return False


def emprestimos_por_usuario(
    lista_emprestimos: List[Dict[str, str]], cpf: str
) -> List[Dict[str, str]]:
    """Retorna todos os empréstimos ativos de um determinado usuário."""

    # Arruma o CPF (remove espaços)
    cpf_normalizado = cpf.strip()
    # Se o CPF estiver vazio, não procura nada
    if not cpf_normalizado:
        return []

    # Cria uma lista só com os empréstimos desse CPF
    return [
        emprestimo
        for emprestimo in lista_emprestimos
        if emprestimo["cpf_usuario"] == cpf_normalizado
    ]