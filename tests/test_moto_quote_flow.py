import sys
import types
mock_flag_modified = lambda instance, key: None
sys.modules['sqlalchemy.orm.attributes'] = types.ModuleType('sqlalchemy.orm.attributes')
sys.modules['sqlalchemy.orm.attributes'].flag_modified = mock_flag_modified


import pytest
from quotes.moto_quote_flow import MotoQuoteFlow

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
    flow = MotoQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '01/20/1990', dummy_set_stage)
    assert session.cliente_birthdate == "01/20/1990"
    assert session.cliente_substage == "awaiting_driverlicense"
    assert "(Passo 3 de 10)" in result

def test_handle_birthdate_brvalid():
    flow = MotoQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '20/01/1990', dummy_set_stage)
    assert session.cliente_birthdate == "01/20/1990"
    assert session.cliente_substage == "awaiting_driverlicense"
    assert "(Passo 3 de 10)" in result

#GARANTE QUE FORMATOS INVALIDOS DE DATA DE NASCIMENTO NAO PASSA E PEDE PRA DIGITAR NOVAMENTE.
def test_handle_birthdate_invalid():
    flow = MotoQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '30/30/1990', dummy_set_stage)
    assert session.cliente_birthdate == None
    assert session.cliente_substage == 'awaiting_birthdate'
    assert "Ops! parece que você" in result 

def test_handle_birthdate_invalid_bigger():
    flow = MotoQuoteFlow()
    session = DummySession()
    result = flow.handle_birthdate(session, '07/30/2045', dummy_set_stage)
    assert session.cliente_birthdate == None
    assert session.cliente_substage == 'awaiting_birthdate'
    assert "Ops! parece que você" in result 

# TESTES DA ADIÇÃO DE VEICULOS/TRANSIÇÃO
def test_handle_multiple_vehicles():
    flow = MotoQuoteFlow()
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
    flow = MotoQuoteFlow()
    session = DummySession()
    session.tipo_cotacao = "moto"
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
    flow = MotoQuoteFlow()
    session = DummySession()
    session.tipo_cotacao = "moto"
    session.cliente_substage = 'awaiting_veiculos'
    result = flow.handle_qtd_veiculos(session, 'zero', dummy_set_stage)
    assert "número válido" in result
    assert session.cliente_substage == 'awaiting_veiculos'

def test_handl_qtd_veiculos_menor():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.tipo_cotacao = "moto"
    session.cliente_substage = 'awaiting_veiculos'
    result = flow.handle_qtd_veiculos(session, '0', dummy_set_stage)
    assert "número válido" in result
    assert session.cliente_substage == 'awaiting_veiculos'

def test_handle_qtd_veiculos_valid():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_veiculos'
    result = flow.handle_qtd_veiculos(session, '1', dummy_set_stage)
    assert result == True 
    assert session.cliente_substage == 'awaiting_vin'

### FINANCIADO / QUITADO

def test_handle_financiado_invalid():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_financiado'
    result = flow.handle_financiado(session, 'nao sei', dummy_set_stage)
    assert "responda apenas 'financiado' ou 'quitado'." in result
    assert session.cliente_substage == "awaiting_financiado"

def test_handle_financiado_valid():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_financiado'
    session.cliente_veiculos = [{"vin": "12345678901234567"}]
    result = flow.handle_financiado(session, 'financiado', dummy_set_stage)
    assert result == True
    assert session.cliente_veiculos[-1]["financiado"] == "financiado"
    assert session.cliente_substage == "awaiting_tempo"



### TAMANHO DO VIN
def test_handle_vin_size_invalid():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_vin'
    result = flow.handle_vin(session, '01234567', dummy_set_stage)
    assert "O VIN deve ter 17 caracteres." in result
    assert session.cliente_substage == 'awaiting_vin'

def test_handle_vin_size_valid():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.cliente_substage = 'awaiting_vin'
    session.cliente_veiculos = []
    result = flow.handle_vin(session, '4T1B11HK9KU850127', dummy_set_stage)
    assert "o veiculo que você está tentando adicionar é um" in result.lower().strip()
    assert session.cliente_substage == 'awaiting_vehicle_confirmation'

def test_handle_vehicle_confirmation_yes():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.vin_temp = "4T1B11HK9KU850127"
    session.cliente_substage = 'awaiting_vehicle_confirmation'
    session.cliente_veiculos = []
    result = flow.handle_vehicle_confirmation(session, 'sim', dummy_set_stage)
    assert result == True
    assert session.cliente_substage == 'awaiting_financiado'

def test_handle_vehicle_confirmation_no():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.vin_temp = "4T1B11HK9KU850127"
    session.tipo_cotacao = "moto"
    session.cliente_substage = 'awaiting_vehicle_confirmation'
    session.cliente_veiculos = []
    result = flow.handle_vehicle_confirmation(session, 'no', dummy_set_stage)
    assert "vamos tentar novamente. por favor, digite o vin da moto" in result.lower().strip()
 
    assert session.cliente_substage == 'awaiting_vin'
    
def test_handle_vehicle_confirmation_incorrect():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.vin_temp = "4T1B11HK9KU850127"
    session.cliente_substage = 'awaiting_vehicle_confirmation'
    session.cliente_veiculos = []
    result = flow.handle_vehicle_confirmation(session, 'idk', dummy_set_stage)
    assert "não entendi a sua resposta! pode" in result.lower().strip()
    assert session.cliente_substage == 'awaiting_vehicle_confirmation'

## TESTE ADIÇÃO MOTORISTA/TRANSIÇÃO
def test_handle_multiple_motorists():
    flow = MotoQuoteFlow()
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
    flow = MotoQuoteFlow()
    session = DummySession()
    session.qtd_motoristas = 1
    session.motorista_atual = 1
    session.cliente_motoristas = [{"nome": "Jose", "birthdate": "02/02/2000", "driver_license": "SA4371431", "driver_license_state": "Massa"}]
    session.cliente_substage = 'awaiting_relation'

    result = flow.handle_motoristas_relacao(session, "amigo", dummy_set_stage)
    assert session.cliente_substage == "awaiting_seguro_anterior"
    assert "Agora, você possui seguro atualmente ou teve seguro nos últimos 30 dias?" in result


## TEM SEGURO ANTERIOR
def test_handle_tem_seguro_anterior_invalid():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.cliente_substage = "awaiting_seguro_anterior"
    def mock_concluir_cotacao(*args, **kwargs): pass
    phone_number = '1199999999999999'
    result = flow.handle_tem_seguro_anterior(session, "nao sei dizer", dummy_set_stage, mock_concluir_cotacao, phone_number)

    assert session.cliente_substage == 'awaiting_seguro_anterior'
    assert "não entendi a sua resposta! pode dizer sim ou não?" in result

def test_handle_tem_seguro_anterior_valid_teve():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.cliente_substage = "awaiting_seguro_anterior"
    def mock_concluir_cotacao(*args, **kwargs): pass
    phone_number = '1199999999999999'
    result = flow.handle_tem_seguro_anterior(session, "sim", dummy_set_stage, mock_concluir_cotacao, phone_number)

    assert session.cliente_substage == 'awaiting_tempo_seguro_anterior'
    assert "Para finalizar, quanto tempo de seguro você tem/teve?" in result

def test_handle_tem_seguro_anterior_valid_nteve():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.cliente_substage = "awaiting_seguro_anterior"
    def mock_concluir_cotacao(*args, **kwargs): pass
    phone_number = '1199999999999999'
    result = flow.handle_tem_seguro_anterior(session, "nao", dummy_set_stage, mock_concluir_cotacao, phone_number)

    assert session.cliente_substage == 'awaiting_seguro_anterior'

# TESTANDO OUTRAS LINGUAGENS
def test_handle_birthdate_en():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.language = 'en'
    result = flow.handle_birthdate(session, '01/20/1990', dummy_set_stage)
    assert session.cliente_birthdate == "01/20/1990"
    assert session.cliente_substage == "awaiting_driverlicense"
    assert "Thank you! Now, what is your driver license" in result

def test_handle_birthdate_es():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.language = 'es'
    result = flow.handle_birthdate(session, '20/01/1990', dummy_set_stage)
    assert session.cliente_birthdate == "01/20/1990"
    assert session.cliente_substage == "awaiting_driverlicense"
    assert "¡Gracias! Ahora, ¿cuál es su número de licencia" in result

def test_handle_vin_size_invalid_en():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.language = 'en'
    session.cliente_substage = 'awaiting_vin'
    result = flow.handle_vin(session, '01234567', dummy_set_stage)
    assert "The VIN must be 17 characters" in result
    assert session.cliente_substage == 'awaiting_vin'

def test_handle_vin_size_invalid_es():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.language = 'es'
    session.cliente_substage = 'awaiting_vin'
    result = flow.handle_vin(session, '01234567', dummy_set_stage)
    assert "El VIN debe tener 17 caracteres" in result
    assert session.cliente_substage == 'awaiting_vin'


def test_handle_tem_seguro_anterior_invalid_en():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.language = 'en'
    session.cliente_substage = "awaiting_seguro_anterior"
    def mock_concluir_cotacao(*args, **kwargs): pass
    phone_number = '1199999999999999'
    result = flow.handle_tem_seguro_anterior(session, "I don't know", dummy_set_stage, mock_concluir_cotacao, phone_number)
    assert session.cliente_substage == 'awaiting_seguro_anterior'
    assert "didn't understand your answer" in result

def test_handle_tem_seguro_anterior_invalid_es():
    flow = MotoQuoteFlow()
    session = DummySession()
    session.language = 'es'
    session.cliente_substage = "awaiting_seguro_anterior"
    def mock_concluir_cotacao(*args, **kwargs): pass
    phone_number = '1199999999999999'
    result = flow.handle_tem_seguro_anterior(session, "no sé", dummy_set_stage, mock_concluir_cotacao, phone_number)
    assert session.cliente_substage == 'awaiting_seguro_anterior'
    assert "no entendí su respuesta" in result

