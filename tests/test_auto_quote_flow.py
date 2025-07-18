import sys
import types
mock_flag_modified = lambda instance, key: None
sys.modules['sqlalchemy.orm.attributes'] = types.ModuleType('sqlalchemy.orm.attributes')
sys.modules['sqlalchemy.orm.attributes'].flag_modified = mock_flag_modified


import pytest
from quotes.auto_quote_flow import AutoQuoteFlow

class DummySession:
    def __init__(self):
        self.language = 'pt'
        self.cliente_substage = 'awaiting_birthdate'
        self.cliente_birthdate = None

def dummy_set_stage(session, new_quote_step):
    session.cliente_substage = new_quote_step


## TESTES DE NASCIMENTO

## GARANTE QUE O FORMATO DA DATA DE NASCIMENTO FUNCIONA TANTO EM BR QUANTO EM AMERICANO E DEIXA SALVO EM AMERICANO.
def test_handle_birthdate_usvalid():
    flow = AutoQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '01/20/1990', dummy_set_stage)
    assert session.cliente_birthdate == "01/20/1990"
    assert session.cliente_substage == "awaiting_driverlicense"
    assert "(Passo 3 de 10)" in result

def test_handle_birthdate_brvalid():
    flow = AutoQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '20/01/1990', dummy_set_stage)
    assert session.cliente_birthdate == "01/20/1990"
    assert session.cliente_substage == "awaiting_driverlicense"
    assert "(Passo 3 de 10)" in result

#GARANTE QUE FORMATOS INVALIDOS DE DATA DE NASCIMENTO NAO PASSA E PEDE PRA DIGITAR NOVAMENTE.
def test_handle_birthdate_invalid():
    flow = AutoQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '30/30/1990', dummy_set_stage)
    assert session.cliente_birthdate == None
    assert session.cliente_substage == 'awaiting_birthdate'
    assert "Ops! parece que você" in result 

def test_handle_birthdate_invalid_bigger():
    flow = AutoQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '07/30/2025', dummy_set_stage)
    assert session.cliente_birthdate == None
    assert session.cliente_substage == 'awaiting_birthdate'
    assert "Ops! parece que você" in result 

# TESTES DA ADIÇÃO DE VEICULOS/TRANSIÇÃO
def test_handle_multiple_vehicles():
    flow = AutoQuoteFlow()
    session = DummySession()
    session.qtd_veiculos = 2
    session.veiculo_atual = 1
    session.cliente_veiculos = [{"vin": "12345678901234567", "financiado": "quitado"}]
    session.cliente_substage = 'awaiting_tempo'

    result = flow.handle_tempo(session, "2 anos", dummy_set_stage)

    assert session.veiculo_atual == 2
    assert session.cliente_substage == "awaiting_vin"
    assert result == True


def test_handle_tempo_last_vehicle():
    flow = AutoQuoteFlow()
    session = DummySession()
    session.qtd_veiculos = 2
    session.veiculo_atual = 2
    session.cliente_veiculos = [
        {"vin": "12345678901234567", "financiado": "quitado"},
        {"vin": "12345678901234568", "financiado": "financiado"}
    ]
    session.cliente_substage = "awaiting_tempo"

    result = flow.handle_tempo(session, "3 anos", dummy_set_stage)
    assert session.cliente_substage == "awaiting_outros_motoristas"
    assert "Deseja cadastrar outros motoristas?" in result or "seguro" in result.lower()
    