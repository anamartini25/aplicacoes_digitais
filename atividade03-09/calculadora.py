
def soma (a, b):
    return a + b

def subtrair(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def divisao(a, b):
    if b == 0:
        raise ValueError('Não existe divisão por zero.')
    else:
        return a / b 
