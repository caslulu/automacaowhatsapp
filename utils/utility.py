from datetime import datetime
import requests

def veiculo_vin(vin):
    """Pega o(s) VINs e retorna marca, modelo e ano do veículo."""
    get_info = requests.get(f'https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json').json()['Results']
    marca = get_info[7]["Value"]
    modelo = get_info[9]["Value"]
    ano = get_info[10]["Value"]
    if not marca or not modelo or not ano:
        raise ValueError("Não foi possível decodificar o VIN.")
    else:
        carro = f"{marca}, {modelo}, {ano}"
    return carro
    
def parse_data_flexivel(texto_data):
    """
    Tenta analisar uma data em múltiplos formatos comuns.
    Retorna um objeto de data se for bem-sucedido, ou None se falhar em todos.
    """
    formatos_para_tentar = [
        "%d/%m/%Y",  
        "%m/%d/%Y",
        "%d/%m/%y", 
        "%m/%d/%y"   
    ]

    for formato in formatos_para_tentar:
        try:
            return datetime.strptime(texto_data, formato)
        except ValueError:
            pass
    
    return None