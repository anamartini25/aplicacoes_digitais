from calculadora import *
import pytest 

def test_soma():
    assert soma(2, 4) == 6

def test_subtracao():
    assert subtrair(6, 4) == 2

def test_multiplicacao():
    assert multiplicar(6, 2) == 12

def test_divisao():
    assert divisao(6, 2) == 3

def test_divisao_por_zero():
    with pytest.raises(ValueError):
        divisao(2, 0)
