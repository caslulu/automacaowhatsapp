from datetime import datetime

def parse_data_flexivel(texto_data):
    """
    Tenta analisar uma data em múltiplos formatos comuns.
    Retorna um objeto de data se for bem-sucedido, ou None se falhar em todos.
    """
    # Lista de formatos para tentar, em ordem de prioridade
    formatos_para_tentar = [
        "%d/%m/%Y",  # Formato Brasileiro (DD/MM/AAAA) - ex: 15/07/2024
        "%m/%d/%Y",  # Formato Americano (MM/DD/AAAA) - ex: 07/15/2024
        "%d/%m/%y",  # Formato Brasileiro com ano curto (DD/MM/AA) - ex: 15/07/24
        "%m/%d/%y"   # Formato Americano com ano curto (MM/DD/AA) - ex: 07/15/24
    ]

    for formato in formatos_para_tentar:
        try:
            # Tenta converter o texto com o formato da vez
            return datetime.strptime(texto_data, formato)
        except ValueError:
            # Se falhar, o loop continua para tentar o próximo formato da lista
            pass
    
    # Se o loop terminar e nenhum formato funcionar, retorna None
    return None