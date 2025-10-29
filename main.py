"""Ponto de entrada do sistema de biblioteca usando módulos dedicados."""

from typing import Dict, List

from emprestimos import (
    devolver_livro,
    emprestar_livro,
    emprestimos_por_usuario,
    listar_emprestimos,
)
from livros import (
    buscar_livros_por_autor,
    buscar_livros_por_titulo,
    cadastrar_livro,
    listar_livros,
)
from persistencia import carregar_dados, salvar_dados
from usuarios import cadastrar_usuario, listar_usuarios

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_LIVROS = "livros.json"
ARQUIVO_EMPRESTIMOS = "emprestimos.json"


def exibir_menu() -> str:
    """Mostra o menu principal e devolve a opção escolhida."""

    # Mostra todas as opções do menu
    print("=== MENU ===")
    print("1. Cadastrar usuário")
    print("2. Listar usuários")
    print("3. Cadastrar livro")
    print("4. Listar livros")
    print("5. Emprestar livro")
    print("6. Consultar livros")
    print("7. Listar empréstimos")
    print("8. Listar empréstimos por usuário")
    print("9. Devolver livro")
    print("10. Sair")
    # Pede pro usuário escolher uma opção
    return input("Escolha uma opção: ").strip()


def consultar_livros(lista_livros: List[Dict[str, int | str]]) -> None:
    """Permite buscar livros por título ou autor e exibe os resultados."""

    # Se não tem livros cadastrados, mostra mensagem e para
    if not lista_livros:
        print(" Nenhum livro cadastrado ainda.\n")
        return

    # Mostra as opções de busca
    print("\n=== Consulta de Livros ===")
    print("1. Buscar por título")
    print("2. Buscar por autor")
    escolha = input("Escolha uma opção de busca: ").strip()

    # Pede o termo que vai ser procurado
    termo_busca = input("Digite o termo de busca: ").strip()

    # Se escolheu buscar por título
    if escolha == "1":
        resultados = buscar_livros_por_titulo(lista_livros, termo_busca)
    # Se escolheu buscar por autor
    elif escolha == "2":
        resultados = buscar_livros_por_autor(lista_livros, termo_busca)
    # Se digitou opção inválida
    else:
        print(" Opção de busca inválida.\n")
        return

    # Se não encontrou nenhum livro
    if not resultados:
        print(" Nenhum livro encontrado para o termo informado.\n")
        return

    # Mostra os livros encontrados
    listar_livros(resultados)


def listar_emprestimos_de_usuario(
    lista_emprestimos: List[Dict[str, str]]
) -> None:
    """Exibe os empréstimos ativos de um CPF específico."""

    # Pede o CPF do usuário
    cpf = input("Digite o CPF do usuário: ").strip()
    # Busca todos os empréstimos desse CPF
    resultados = emprestimos_por_usuario(lista_emprestimos, cpf)

    # Se não achou nenhum empréstimo
    if not resultados:
        print(" Nenhum empréstimo encontrado para esse CPF.\n")
        return

    # Mostra os empréstimos encontrados
    listar_emprestimos(resultados)


def main() -> None:
    """Executa o loop principal do sistema de biblioteca."""

    # Carrega os dados salvos nos arquivos JSON
    usuarios: List[Dict[str, str]] = carregar_dados(ARQUIVO_USUARIOS)
    livros: List[Dict[str, int | str]] = carregar_dados(ARQUIVO_LIVROS)
    emprestimos: List[Dict[str, str]] = carregar_dados(ARQUIVO_EMPRESTIMOS)

    # Loop infinito do menu
    while True:
        # Mostra o menu e pega a opção escolhida
        opcao = exibir_menu()

        # Opção 1: Cadastrar novo usuário
        if opcao == "1":
            novo_usuario = cadastrar_usuario()
            if novo_usuario:
                usuarios.append(novo_usuario)
                salvar_dados(usuarios, ARQUIVO_USUARIOS)
        # Opção 2: Mostrar todos os usuários
        elif opcao == "2":
            listar_usuarios(usuarios)
        # Opção 3: Cadastrar novo livro
        elif opcao == "3":
            novo_livro = cadastrar_livro()
            if novo_livro:
                livros.append(novo_livro)
                salvar_dados(livros, ARQUIVO_LIVROS)
        # Opção 4: Mostrar todos os livros
        elif opcao == "4":
            listar_livros(livros)
        # Opção 5: Fazer empréstimo
        elif opcao == "5":
            if emprestar_livro(usuarios, livros, emprestimos):
                salvar_dados(livros, ARQUIVO_LIVROS)
                salvar_dados(emprestimos, ARQUIVO_EMPRESTIMOS)
        # Opção 6: Consultar/buscar livros
        elif opcao == "6":
            consultar_livros(livros)
        # Opção 7: Mostrar todos os empréstimos
        elif opcao == "7":
            listar_emprestimos(emprestimos)
        # Opção 8: Mostrar empréstimos de um usuário específico
        elif opcao == "8":
            listar_emprestimos_de_usuario(emprestimos)
        # Opção 9: Devolver livro
        elif opcao == "9":
            if devolver_livro(livros, emprestimos):
                salvar_dados(livros, ARQUIVO_LIVROS)
                salvar_dados(emprestimos, ARQUIVO_EMPRESTIMOS)
        # Opção 10: Sair do programa
        elif opcao == "10":
            print(" Encerrando o programa...")
            # Salva tudo antes de sair
            salvar_dados(usuarios, ARQUIVO_USUARIOS)
            salvar_dados(livros, ARQUIVO_LIVROS)
            salvar_dados(emprestimos, ARQUIVO_EMPRESTIMOS)
            break
        # Se digitou opção inválida
        else:
            print(" Opção inválida! Tente novamente.\n")


if __name__ == "__main__":
    main()
