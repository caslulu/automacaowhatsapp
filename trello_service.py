import requests
import os
from dotenv import load_dotenv
from data_funcoes import veiculo_vin

class Trello:

    def __init__(self):
            load_dotenv()
            self.URL_TRELLO = os.getenv("URL_TRELLO")
            self.yourKey = os.getenv("TRELLO_KEY")
            self.yourToken = os.getenv("TRELLO_TOKEN")
            self.idList = os.getenv("TRELLO_ID_LIST")
            
    def criar_carta(self, **kwargs):
        """
        Cria uma carta no Trello. Se houver dados de cônjuge, inclui na descrição.
        """
        veiculos = kwargs.get('veiculos', '')
        pessoas = kwargs.get('pessoas', '')
        email = kwargs.get('email', '')
        if not email:
            email = self.gerar_email(kwargs.get('nome', ''))
        veiculos_lista = []
        pessoas_lista = []
        import json
        if isinstance(veiculos, str):
            try:
                veiculos_lista = json.loads(veiculos)
            except Exception:
                pass
        elif isinstance(veiculos, list):
            veiculos_lista = veiculos
        if isinstance(pessoas, str):
            try:
                pessoas_lista = json.loads(pessoas)
            except Exception:
                pass
        elif isinstance(pessoas, list):
            pessoas_lista = pessoas

        # Monta descrição dos veículos, cada info em uma linha
        veiculos_desc = ''
        if veiculos_lista:
            for idx, v in enumerate(veiculos_lista, 1):
                vin = v.get('vin', '-')
                marca_modelo_ano = '-'
                if vin and vin != '-':
                    try:
                        marca_modelo_ano = veiculo_vin(vin)
                    except Exception:
                        marca_modelo_ano = '-'
                veiculos_desc += (
                    f"\nVeículo {idx}:"
                    f"\n -------------"
                    f"\n  VIN: {vin}"
                    f"\n  {marca_modelo_ano}"
                    f"\n  Estado: {v.get('financiado', '-')}"
                    f"\n  Tempo: {v.get('tempo', '-')}\n"
                )
        else:
            veiculos_desc = str(veiculos)

        # Monta descrição das pessoas extras (drivers)
        pessoas_desc = ''
        if pessoas_lista:
            for idx, p in enumerate(pessoas_lista, 1):
                documento = f"{p.get("driver_license")} - {p.get("driver_license_state")}"
                pessoas_desc += (
                    f"\nDriver extra {idx}:"
                    f"\n --------------"
                    f"\n  Nome: {p.get('nome', '-') }"
                    f"\n  Documento: {documento}"
                    f"\n  Data nascimento: {p.get('birthdate', '-') }"
                    f"\n  Parentesco: {p.get('relation', '-') }"
                    f"\n-------------"
                )

        descricao = (
            f"doc: {kwargs.get('documento', '')}\n"
            f"{kwargs.get('endereco', '')}\n"
            f"{kwargs.get('data_nascimento', '')}\n"
            f"tempo de seguro: {kwargs.get('tempo_de_seguro', '')}\n"
            f"tempo no endereco: {kwargs.get('tempo_no_endereco', '')}\n"
            f"email: {email}\n"
            f"{veiculos_desc}"
            f"{pessoas_desc}\n"
        )

        if kwargs.get("tipo_cotacao") == "comercial":
            descricao += (
                f"\n --- Dados Comerciais ---"
                f"\n Empresa: {kwargs.get('empresa_nome', '-')}"
                f"\n USDOT: {kwargs.get('empresa_usdot', '-')}"
                f"\n Registro: {kwargs.get('empresa_numero_registro', '-')}"
                f"\n Estrutura: {kwargs.get('empresa_estrutura', '-')}"
                f"\n Ramo: {kwargs.get('empresa_ramo', '-')}"
                f"\n Tipo de Carga: {kwargs.get('empresa_tipo_carga', '-')}"
                f"\n Endereço empresa: {kwargs.get('empresa_endereco', '-')}"
                f"\n Milhas até o trabalho: {kwargs.get('empresa_milhas_trabalho', '-')}"
                f"\n Milhas por ano: {kwargs.get('empresa_mihlhas_ano', '-')}"
            )


        params_create = {
            "key": self.yourKey,
            "token": self.yourToken,
            "idList": self.idList,
            "name": kwargs.get('nome', ''),
            "desc": descricao
        }

        response = requests.post(f"{self.URL_TRELLO}", params=params_create)
        if response.ok:
            return response.json().get("id")
        return None
    


    def gerar_email(self, nome_completo):
        if not nome_completo:
            return ''
        return f"{nome_completo.lower().replace(' ', '')}@outlook.com"