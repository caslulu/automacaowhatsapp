from datetime import datetime

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