"""Operações relacionadas aos usuários do sistema."""

from typing import Dict, List, Optional


def cadastrar_usuario() -> Optional[Dict[str, str]]:
    """Solicita dados pelo console e devolve um novo usuário válido."""

    # Pede pro usuário digitar o nome completo
    nome = input("Digite seu nome completo: ").strip()
    # Pede pro usuário digitar o CPF (só números)
    cpf = input("Digite seu CPF (somente números): ").strip()

    # Verifica se o CPF tem exatamente 11 números
    if not cpf.isdigit() or len(cpf) != 11:
        print(" CPF inválido! Deve conter exatamente 11 números.")
        return None

    # Verifica se o nome tem apenas letras (sem números ou símbolos)
    if not all(parte.isalpha() for parte in nome.split()):
        print(" Nome inválido! Digite apenas letras (sem números ou símbolos).")
        return None

    # Deixa o nome bonito com primeira letra maiúscula (ex: "maria silva" -> "Maria Silva")
    nome_formatado = " ".join(parte.capitalize() for parte in nome.split())

    # Cria um dicionário com os dados do usuário
    novo_usuario = {"nome": nome_formatado, "cpf": cpf}
    print(f" Usuário {nome_formatado} cadastrado com sucesso!\n")
    return novo_usuario


def listar_usuarios(lista_usuarios: List[Dict[str, str]]) -> None:
    """Mostra todos os usuários cadastrados no console."""

    # Se a lista estiver vazia, mostra mensagem e sai
    if not lista_usuarios:
        print(" Nenhum usuário cadastrado ainda.\n")
        return

    # Mostra o cabeçalho da listagem
    print("\n=== Lista de Usuários Cadastrados ===")
    # Percorre a lista de usuários e mostra cada um com seu número
    for indice, usuario in enumerate(lista_usuarios, start=1):
        print(f"{indice}. Nome: {usuario['nome']} | CPF: {usuario['cpf']}")
    print("=====================================\n")


def encontrar_usuario_por_cpf(
    lista_usuarios: List[Dict[str, str]], cpf: str
) -> Optional[Dict[str, str]]:
    """Procura um usuário pelo CPF e devolve o registro, se existir."""

    # Percorre todos os usuários da lista
    for usuario in lista_usuarios:
        # Se achar um com CPF igual, devolve ele
        if usuario["cpf"] == cpf:
            return usuario
    # Se não achar nenhum, devolve None (nada)
    return None