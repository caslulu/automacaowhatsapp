import pytest
import time
from quotes.auto_quote_flow import AutoQuoteFlow
from quotes.moto_quote_flow import MotoQuoteFlow
from quotes.commercial_quote_flow import ComercialQuoteFlow
class DummySession:
    def __init__(self, substage=None, stage="quote"):
        self.cliente_substage = substage
        self.language = 'pt'
        self.cliente_stage = stage

def dummy_set_stage(session, new_quote_step):
    session.cliente_substage = new_quote_step


## TESTES PARA VOLTAR AO PASSO ANTERIOR.
@pytest.mark.parametrize("flow_cls", [AutoQuoteFlow, MotoQuoteFlow, ComercialQuoteFlow])
@pytest.mark.parametrize("current_step,expected_previous", [
    ("awaiting_birthdate", "awaiting_name"),
    ("awaiting_driverlicense", "awaiting_birthdate"),
    ("awaiting_driverstate", "awaiting_driverlicense"),
    ("awaiting_address", "awaiting_driverstate"),
    ("awaiting_tempo_endereco", "awaiting_address"), ("awaiting_veiculos", "awaiting_tempo_endereco"),
    ("awaiting_vin", "awaiting_veiculos"),
    ("awaiting_financiado", "awaiting_vin"),
    ("awaiting_tempo", "awaiting_financiado"),
    ("awaiting_outros_motoristas", "awaiting_tempo"),
    ("awaiting_qtd_motoristas", "awaiting_outros_motoristas"),
    ("awaiting_motorista_birthdate", "awaiting_qtd_motoristas"),
    ("awaiting_motorista_driver", "awaiting_motorista_birthdate"),
    ("awaiting_motorista_state", "awaiting_motorista_driver"),
    ("awaiting_motorista_relacao", "awaiting_motorista_state"),
    ("awaiting_seguro_anterior", "awaiting_motorista_relacao"),
    ("awaiting_tempo_seguro_anterior", "awaiting_seguro_anterior"),
])
def test_handle_back_steps(flow_cls, current_step, expected_previous):
    flow = flow_cls()
    session = DummySession(current_step)
    flow.handle_back(session, dummy_set_stage)
    assert session.cliente_substage == expected_previous

@pytest.mark.parametrize("current_step,expected_previous", [
    ("awaiting_nome_empresa", "awaiting_outros_motoristas"),
    ("awaiting_tem_usdot", "awaiting_nome_empresa"),
    ("awaiting_usdot", "awaiting_tem_usdot"),
    ("awaiting_numero_registro", "awaiting_usdot"),
    ("awaiting_estrutura_empresa", "awaiting_numero_registro"),
    ("awaiting_ramo", "awaiting_estrutura_empresa"),
    ("awaiting_carga", "awaiting_ramo"),
    ("awaiting_milhas_dia", "awaiting_carga"),
])
def test_handle_back_comercial_steps(current_step, expected_previous):
    flow = ComercialQuoteFlow()
    session = DummySession(current_step)
    flow.handle_back(session, dummy_set_stage)
    assert session.cliente_substage == expected_previous
    
def test_handle_back_limit():
    flow = AutoQuoteFlow()
    session = DummySession("awaiting_name")
    result = flow.handle_back(session, dummy_set_stage)
    assert session.cliente_substage == "awaiting_name"
    assert "Não é possível voltar mais" in result or "can't go back" in result

@pytest.mark.parametrize("flow_cls", [AutoQuoteFlow, MotoQuoteFlow, ComercialQuoteFlow])
def test_handle_nonexistent_step(flow_cls):
    flow = flow_cls()
    session = DummySession("passo_inexistente")
    result = flow.handle_back(session, dummy_set_stage)
    assert session.cliente_substage == "passo_inexistente"
    assert "não é possível voltar mais" in result.lower()

def test_handle_inexistent_step_main_flow():
    flow = AutoQuoteFlow()
    session = DummySession("passo_inexistente")
    result = flow.handle("5511999999999", "qualquer coisa", session, dummy_set_stage, lambda *a, **kw: None)
    assert "Desculpa, Ocorreu um erro!" in result

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

@pytest.fixture
def conversation_flow_mocked():
    # Mocka Cliente e db ANTES de importar o ConversationFlow
    sys.modules['models.model'] = MagicMock()
    sys.modules['models.model'].Cliente = MagicMock()

    sys.modules['utils.extensions'] = MagicMock()
    sys.modules['utils.extensions'].db = MagicMock()

    from services.conversation_service import ConversationFlow
    return ConversationFlow()

def test_handle_support_yes(conversation_flow_mocked):
    # cria uma sessão fake
    fake_session = SimpleNamespace(language='pt', cliente_stage='suporte', last_interaction=time.time())
    conversation_flow_mocked.get_user_session = MagicMock(return_value=fake_session)
    conversation_flow_mocked.set_stage = MagicMock()

    result = conversation_flow_mocked.handle_support("5511999999999", "sim")
    assert "qual problema você está tendo?" in result.lower()

def test_handle_support_no(conversation_flow_mocked):
    # cria uma sessão fake
    fake_session = SimpleNamespace(language='pt', cliente_stage='suporte', last_interaction=time.time())
    conversation_flow_mocked.get_user_session = MagicMock(return_value=fake_session)
    conversation_flow_mocked.set_stage = MagicMock()

    result = conversation_flow_mocked.handle_support("5511999999999", "não")
    assert "agora, volte a fazer o que estava fazendo anteriormente." in result.lower()

def test_handle_support_incorrect(conversation_flow_mocked):
    # cria uma sessão fake
    fake_session = SimpleNamespace(language='pt', cliente_stage='suporte', last_interaction=time.time())
    conversation_flow_mocked.get_user_session = MagicMock(return_value=fake_session)
    conversation_flow_mocked.set_stage = MagicMock()

    result = conversation_flow_mocked.handle_support("5511999999999", "sei la")
    assert "não entendi" in result.lower()

def test_handle_support_timeout(conversation_flow_mocked):
    # cria uma sessão fake
    fake_session = SimpleNamespace(language='pt', cliente_stage='suporte', last_interaction=0)
    conversation_flow_mocked.get_user_session = MagicMock(return_value=fake_session)
    conversation_flow_mocked.set_stage = MagicMock()

    result = conversation_flow_mocked.handle_support("5511999999999", "sei la")
    assert "parece que voce não respondeu a tempo" in result.lower()

def test_handle_support_certeza(conversation_flow_mocked):
    # cria uma sessão fake
    fake_session = SimpleNamespace(language='pt', cliente_stage='suporte', last_interaction=0)
    conversation_flow_mocked.get_user_session = MagicMock(return_value=fake_session)
    conversation_flow_mocked.set_stage = MagicMock()

    result = conversation_flow_mocked.process_message("5511999999999", "suporte")
    assert "você tem certeza que" in result.lower()
