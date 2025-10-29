"""Testes automatizados para o sistema de biblioteca."""

from typing import Dict, List

import pytest

from emprestimos import devolver_livro, emprestar_livro, emprestimos_por_usuario
from livros import (
    buscar_livros_por_autor,
    buscar_livros_por_titulo,
    cadastrar_livro,
)
from usuarios import cadastrar_usuario


def criar_iterador_entradas(valores: List[str]):
    """Cria um gerador simples para simular a função input."""

    def _fornecer(_prompt: str) -> str:
        return valores.pop(0)

    return _fornecer


def test_cadastrar_usuario_valido(monkeypatch: pytest.MonkeyPatch) -> None:
    entradas = ["ana maria", "12345678901"]
    monkeypatch.setattr("builtins.input", criar_iterador_entradas(entradas))

    usuario = cadastrar_usuario()

    assert usuario == {"nome": "Ana Maria", "cpf": "12345678901"}


def test_cadastrar_usuario_com_dados_invalidos(monkeypatch: pytest.MonkeyPatch) -> None:
    entradas = ["Joao123", "111"]
    monkeypatch.setattr("builtins.input", criar_iterador_entradas(entradas))

    usuario = cadastrar_usuario()

    assert usuario is None


def test_cadastrar_livro_invalido(monkeypatch: pytest.MonkeyPatch) -> None:
    entradas = ["livro teste", "autor teste", "ano ruim", "2"]
    monkeypatch.setattr("builtins.input", criar_iterador_entradas(entradas))

    livro = cadastrar_livro()

    assert livro is None


def test_cadastrar_livro_valido(monkeypatch: pytest.MonkeyPatch) -> None:
    entradas = ["livro teste", "autor teste", "2020", "3"]
    monkeypatch.setattr("builtins.input", criar_iterador_entradas(entradas))

    livro = cadastrar_livro()

    assert livro == {
        "título": "Livro Teste",
        "autor": "Autor Teste",
        "ano": 2020,
        "exemplares": 3,
    }


def test_emprestar_livro_sucesso(monkeypatch: pytest.MonkeyPatch) -> None:
    usuarios: List[Dict[str, str]] = [{"nome": "Ana Maria", "cpf": "12345678901"}]
    livros: List[Dict[str, int | str]] = [
        {"título": "Livro Teste", "autor": "Autor", "ano": 2020, "exemplares": 2}
    ]
    emprestimos: List[Dict[str, str]] = []

    entradas = ["12345678901", "Livro Teste"]
    monkeypatch.setattr("builtins.input", criar_iterador_entradas(entradas))

    sucesso = emprestar_livro(usuarios, livros, emprestimos)

    assert sucesso is True
    assert len(emprestimos) == 1
    assert emprestimos[0]["cpf_usuario"] == "12345678901"


def test_emprestar_livro_sem_usuario(monkeypatch: pytest.MonkeyPatch) -> None:
    usuarios: List[Dict[str, str]] = []
    livros: List[Dict[str, int | str]] = [
        {"título": "Livro Teste", "autor": "Autor", "ano": 2020, "exemplares": 1}
    ]
    emprestimos: List[Dict[str, str]] = []

    entradas = ["00000000000", "Livro Teste"]
    monkeypatch.setattr("builtins.input", criar_iterador_entradas(entradas))

    sucesso = emprestar_livro(usuarios, livros, emprestimos)

    assert sucesso is False
    assert livros[0]["exemplares"] == 1
    assert emprestimos == []


def test_devolver_livro_sucesso(monkeypatch: pytest.MonkeyPatch) -> None:
    livros: List[Dict[str, int | str]] = [
        {"título": "Livro Teste", "autor": "Autor", "ano": 2020, "exemplares": 0}
    ]
    emprestimos: List[Dict[str, str]] = [
        {
            "cpf_usuario": "12345678901",
            "titulo_livro": "Livro Teste",
            "data_emprestimo": "2025-10-29 10:00:00",
        }
    ]

    entradas = ["12345678901", "Livro Teste"]
    monkeypatch.setattr("builtins.input", criar_iterador_entradas(entradas))

    sucesso = devolver_livro(livros, emprestimos)

    assert sucesso is True
    assert livros[0]["exemplares"] == 1
    assert emprestimos == []


def test_devolver_livro_inexistente(monkeypatch: pytest.MonkeyPatch) -> None:
    livros: List[Dict[str, int | str]] = [
        {"título": "Livro Teste", "autor": "Autor", "ano": 2020, "exemplares": 1}
    ]
    emprestimos: List[Dict[str, str]] = []

    entradas = ["12345678901", "Livro Teste"]
    monkeypatch.setattr("builtins.input", criar_iterador_entradas(entradas))

    sucesso = devolver_livro(livros, emprestimos)

    assert sucesso is False
    assert livros[0]["exemplares"] == 1


def test_buscar_livros_por_titulo() -> None:
    livros: List[Dict[str, int | str]] = [
        {"título": "Python Básico", "autor": "Autor 1", "ano": 2020, "exemplares": 1},
        {"título": "Python Avançado", "autor": "Autor 2", "ano": 2021, "exemplares": 2},
        {"título": "Algoritmos", "autor": "Autor 3", "ano": 2019, "exemplares": 1},
    ]

    resultados = buscar_livros_por_titulo(livros, "python")

    assert len(resultados) == 2
    assert all("python" in livro["título"].lower() for livro in resultados)


def test_buscar_livros_por_autor_sem_resultado() -> None:
    livros: List[Dict[str, int | str]] = [
        {"título": "Livro Um", "autor": "Maria Silva", "ano": 2022, "exemplares": 1}
    ]

    resultados = buscar_livros_por_autor(livros, "José")

    assert resultados == []


def test_emprestimos_por_usuario() -> None:
    emprestimos: List[Dict[str, str]] = [
        {"cpf_usuario": "111", "titulo_livro": "A", "data_emprestimo": "2025-10-01"},
        {"cpf_usuario": "222", "titulo_livro": "B", "data_emprestimo": "2025-10-02"},
        {"cpf_usuario": "111", "titulo_livro": "C", "data_emprestimo": "2025-10-03"},
    ]

    resultados = emprestimos_por_usuario(emprestimos, "111")

    assert len(resultados) == 2
    assert all(emprestimo["cpf_usuario"] == "111" for emprestimo in resultados)