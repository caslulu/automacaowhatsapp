
import sys
import types
mock_flag_modified = lambda instance, key: None
sys.modules['sqlalchemy.orm.attributes'] = types.ModuleType('sqlalchemy.orm.attributes')
sys.modules['sqlalchemy.orm.attributes'].flag_modified = mock_flag_modified


import pytest
from quotes.commercial_quote_flow import ComercialQuoteFlow

class DummySession:
    def __init__(self):
        self.language = 'pt'
        self.cliente_substage = 'awaiting_birthdate'
        self.cliente_birthdate = None

def dummy_set_stage(session, new_quote_step):
    session.cliente_substage = new_quote_step

def dummy_concluir_cotacao(*args, **kwargs): pass

## TESTES DE NASCIMENTO

## GARANTE QUE O FORMATO DA DATA DE NASCIMENTO FUNCIONA TANTO EM BR QUANTO EM AMERICANO E DEIXA SALVO EM AMERICANO.
def test_handle_birthdate_usvalid():
    flow = ComercialQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '01/20/1990', dummy_set_stage)
    assert session.cliente_birthdate == "01/20/1990"
    assert session.cliente_substage == "awaiting_driverlicense"
    assert "(Passo 3 de 10)" in result

def test_handle_birthdate_brvalid():
    flow = ComercialQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '20/01/1990', dummy_set_stage)
    assert session.cliente_birthdate == "01/20/1990"
    assert session.cliente_substage == "awaiting_driverlicense"
    assert "(Passo 3 de 10)" in result

#GARANTE QUE FORMATOS INVALIDOS DE DATA DE NASCIMENTO NAO PASSA E PEDE PRA DIGITAR NOVAMENTE.
def test_handle_birthdate_invalid():
    flow = ComercialQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '30/30/1990', dummy_set_stage)
    assert session.cliente_birthdate == None
    assert session.cliente_substage == 'awaiting_birthdate'
    assert "Ops! parece que você" in result 

def test_handle_birthdate_invalid_bigger():
    flow = ComercialQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '07/30/2025', dummy_set_stage)
    assert session.cliente_birthdate == None
    assert session.cliente_substage == 'awaiting_birthdate'
    assert "Ops! parece que você" in result 

# TESTES DA ADIÇÃO DE VEICULOS/TRANSIÇÃO
def test_handle_multiple_vehicles():
    flow = ComercialQuoteFlow()
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
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.tipo_cotacao = "comercial"
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

### QUANTIDADE DE VEICULOS

def test_handle_qtd_veiculos_invalid():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.tipo_cotacao = "comercial"
    session.cliente_substage = 'awaiting_veiculos'
    result = flow.handle_qtd_veiculos(session, 'zero', dummy_set_stage)
    assert "número válido" in result
    assert session.cliente_substage == 'awaiting_veiculos'

def test_handl_qtd_veiculos_menor():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.tipo_cotacao = "comercial"
    session.cliente_substage = 'awaiting_veiculos'
    result = flow.handle_qtd_veiculos(session, '0', dummy_set_stage)
    assert "número válido" in result
    assert session.cliente_substage == 'awaiting_veiculos'

def test_handle_qtd_veiculos_valid():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_veiculos'
    result = flow.handle_qtd_veiculos(session, '1', dummy_set_stage)
    assert result == True 
    assert session.cliente_substage == 'awaiting_vin'

### FINANCIADO / QUITADO

def test_handle_financiado_invalid():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_financiado'
    result = flow.handle_financiado(session, 'nao sei', dummy_set_stage)
    assert "responda apenas 'financiado' ou 'quitado'." in result
    assert session.cliente_substage == "awaiting_financiado"

def test_handle_financiado_valid():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_financiado'
    session.cliente_veiculos = [{"vin": "12345678901234567"}]
    result = flow.handle_financiado(session, 'financiado', dummy_set_stage)
    assert result == True
    assert session.cliente_veiculos[-1]["financiado"] == "financiado"
    assert session.cliente_substage == "awaiting_tempo"



### TAMANHO DO VIN
def test_handle_vin_size_invalid():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_vin'
    result = flow.handle_vin(session, '01234567', dummy_set_stage)
    assert "O VIN deve ter 17 caracteres." in result
    assert session.cliente_substage == 'awaiting_vin'

def test_handle_vin_size_valid():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_vin'
    session.cliente_veiculos = []
    result = flow.handle_vin(session, '4T1B11HK9KU850127', dummy_set_stage)
    assert "o veiculo que você está tentando adicionar é um" in result.lower().strip()
    assert session.cliente_substage == 'awaiting_vehicle_confirmation'

def test_handle_vehicle_confirmation_yes():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.vin_temp = "4T1B11HK9KU850127"
    session.cliente_substage = 'awaiting_vehicle_confirmation'
    session.cliente_veiculos = []
    result = flow.handle_vehicle_confirmation(session, 'sim', dummy_set_stage)
    assert result == True
    assert session.cliente_substage == 'awaiting_financiado'

def test_handle_vehicle_confirmation_no():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.tipo_cotacao = "comercial"
    session.vin_temp = "4T1B11HK9KU850127"
    session.cliente_substage = 'awaiting_vehicle_confirmation'
    session.cliente_veiculos = []
    result = flow.handle_vehicle_confirmation(session, 'no', dummy_set_stage)
    assert "vamos tentar novamente. por favor, digite o vin do" in result.lower().strip()
 
    assert session.cliente_substage == 'awaiting_vin'
    
def test_handle_vehicle_confirmation_incorrect():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.vin_temp = "4T1B11HK9KU850127"
    session.cliente_substage = 'awaiting_vehicle_confirmation'
    session.cliente_veiculos = []
    result = flow.handle_vehicle_confirmation(session, 'idk', dummy_set_stage)
    assert "não entendi a sua resposta! pode" in result.lower().strip()
    assert session.cliente_substage == 'awaiting_vehicle_confirmation'



## TESTE ADIÇÃO MOTORISTA/TRANSIÇÃO
def test_handle_multiple_motorists():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.qtd_motoristas = 2
    session.motorista_atual = 1
    session.cliente_motoristas = [{"nome": "Jose", "birthdate": "02/02/2000", "driver_license": "SA4371431", "driver_license_state": "Massa"}]
    session.cliente_substage = 'awaiting_relation'

    result = flow.handle_motoristas_relacao(session, "amigo", dummy_set_stage)
    assert result == True
    assert session.motorista_atual == 2
    assert session.cliente_substage == "awaiting_motorista_nome"

def test_handle_last_motorist():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.qtd_motoristas = 1
    session.motorista_atual = 1
    session.cliente_motoristas = [{"nome": "Jose", "birthdate": "02/02/2000", "driver_license": "SA4371431", "driver_license_state": "Massa"}]
    session.cliente_substage = 'awaiting_relation'

    result = flow.handle_motoristas_relacao(session, "amigo", dummy_set_stage)
    assert session.cliente_substage == "awaiting_nome_empresa"
    assert "qual o nome da empresa?" in result.lower().strip()

# ENDERECO DA EMPRESA
def test_endereco_empresa():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_address'
    result = flow.handle_address(session, "rua tal", dummy_set_stage)
    assert session.cliente_substage == "awaiting_comercial_address"
    assert "Qual o endereço comercial?" in result


def test_endereco_empresa_mesmo():
    flow = ComercialQuoteFlow()
    phone_number = "11111111111111"
    session = DummySession()
    session.cliente_address = "rua blabla"
    session.cliente_substage = "awaiting_comercial_address"
    result = flow.handle(phone_number, "mesmo", session, dummy_set_stage, dummy_concluir_cotacao)
    assert session.empresa_endereco == 'rua blabla'
    assert session.cliente_substage == "awaiting_veiculos"
    assert "Quantos veículos comerciais você" in result


def test_endereco_empresa_diferente():
    flow = ComercialQuoteFlow()
    phone_number = "11111111111111"
    session = DummySession()
    session.cliente_address = "rua blabla"
    session.cliente_substage = "awaiting_comercial_address"
    result = flow.handle(phone_number, "rua teste", session, dummy_set_stage, dummy_concluir_cotacao)
    assert session.empresa_endereco == "rua teste"
    assert session.cliente_substage == "awaiting_veiculos"
    assert session.cliente_address == "rua blabla"
    assert "Quantos veículos comerciais você" in result

# Testes em inglês
def test_handle_vin_size_invalid_en():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.language = 'en'
    session.cliente_substage = 'awaiting_vin'
    result = flow.handle_vin(session, '01234567', dummy_set_stage)
    assert "The VIN must be 17 characters" in result
    assert session.cliente_substage == 'awaiting_vin'

def test_handle_last_motorist_en():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.language = 'en'
    session.qtd_motoristas = 1
    session.motorista_atual = 1
    session.cliente_motoristas = [{"nome": "Jose", "birthdate": "02/02/2000", "driver_license": "SA4371431", "driver_license_state": "Massa"}]
    session.cliente_substage = 'awaiting_relation'
    result = flow.handle_motoristas_relacao(session, "employee", dummy_set_stage)
    assert session.cliente_substage == "awaiting_nome_empresa"
    assert "What is the company name?" in result

# Testes em espanhol
def test_handle_vin_size_invalid_es():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.language = 'es'
    session.cliente_substage = 'awaiting_vin'
    result = flow.handle_vin(session, '01234567', dummy_set_stage)
    assert "El VIN debe tener 17 caracteres" in result
    assert session.cliente_substage == 'awaiting_vin'

def test_handle_last_motorist_es():
    flow = ComercialQuoteFlow()
    session = DummySession()
    session.language = 'es'
    session.qtd_motoristas = 1
    session.motorista_atual = 1
    session.cliente_motoristas = [{"nome": "Jose", "birthdate": "02/02/2000", "driver_license": "SA4371431", "driver_license_state": "Massa"}]
    session.cliente_substage = 'awaiting_relation'
    result = flow.handle_motoristas_relacao(session, "empleado", dummy_set_stage)
    assert session.cliente_substage == "awaiting_nome_empresa"
    assert "¿Cuál es el nombre de la empresa?" in result
