from abc import ABC, abstractmethod
import pytest

# ==============================================================================
# DECORATOR
# ==============================================================================
def registrar_envio(funcao_original):
    def wrapper(*args, **kwargs):
        print("Iniciando envio da notificação")
        resultado = funcao_original(*args, **kwargs)
        print("Envio finalizado")
        return resultado
    return wrapper

# ==============================================================================
# CLASSES (Abstrata e Concretas)
# ==============================================================================
class Notificacao(ABC):
    def __init__(self, destinatario, mensagem):
        self.destinatario = destinatario
        self.mensagem = mensagem

    def exibir_dados(self):
        return f"Destinatário: {self.destinatario} | Mensagem: {self.mensagem}"

    @abstractmethod
    def enviar(self):
        pass

class NotificacaoEmail(Notificacao):
    @registrar_envio
    def enviar(self):
        return f"E-mail enviado para {self.destinatario}"

class NotificacaoSMS(Notificacao):
    @registrar_envio
    def enviar(self):
        return f"SMS enviado para {self.destinatario}"

# ==============================================================================
# TESTES UNITÁRIOS (Pytest)
# ==============================================================================

def test_notificacao_email_retorno(capsys):
    """Verifica se a notificação por e-mail retorna o texto correto e executa o decorator."""
    notif = NotificacaoEmail("usuario@email.com", "Bem-vindo!")
    
    resultado = notif.enviar()
    
    # Valida o retorno do método
    assert resultado == "E-mail enviado para usuario@email.com"
    
    # Valida se o decorator imprimiu as mensagens no console
    capturado = capsys.readouterr()
    assert "Iniciando envio da notificação\n" in capturado.out
    assert "Envio finalizado\n" in capturado.out

def test_notificacao_sms_retorno(capsys):
    """Verifica se a notificação por SMS retorna o texto correto e executa o decorator."""
    notif = NotificacaoSMS("11999999999", "Seu código é 1234")
    
    resultado = notif.enviar()
    
    # Valida o retorno do método
    assert resultado == "SMS enviado para 11999999999"
    
    # Valida se o decorator imprimiu as mensagens no console
    capturado = capsys.readouterr()
    assert "Iniciando envio da notificação\n" in capturado.out
    assert "Envio finalizado\n" in capturado.out

def test_exibir_dados_retorno():
    """Verifica se exibir_dados() retorna corretamente os dados cadastrados."""
    notif = NotificacaoEmail("teste@email.com", "Minha mensagem")
    esperado = "Destinatário: teste@email.com | Mensagem: Minha mensagem"
    
    assert notif.exibir_dados() == esperado

def test_instanciar_classe_abstrata_gera_erro():
    """Verifica se não é possível instanciar a classe abstrata Notificacao diretamente."""
    with pytest.raises(TypeError):
        # Tentar instanciar uma classe com método abstrato gera um TypeError no Python
        Notificacao("qualquer@email.com", "Olá")
