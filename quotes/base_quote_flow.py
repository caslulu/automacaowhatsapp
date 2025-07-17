from utility import parse_data_flexivel
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified

class BaseQuoteFlow:

    previous_steps = {
        "awaiting_birthdate": "awaiting_name",
        "awaiting_driverlicense": "awaiting_birthdate",
        "awaiting_driverstate": "awaiting_driverlicense",
        "awaiting_address": "awaiting_driverstate",
        "awaiting_tempo_endereco": "awaiting_address",
        "awaiting_veiculos": "awaiting_tempo_endereco",
        "awaiting_vin": "awaiting_veiculos",
        "awaiting_financiado": "awaiting_vin",
        "awaiting_tempo": "awaiting_financiado",
        "awaiting_outros_motoristas": "awaiting_tempo",
        "awaiting_qtd_motoristas": "awaiting_outros_motoristas",
        "awaiting_motorista_birthdate": "awaiting_qtd_motoristas",
        "awaiting_motorista_driver": "awaiting_motorista_birthdate",
        "awaiting_motorista_state": "awaiting_motorista_driver",
        "awaiting_motorista_relacao": "awaiting_motorista_state",
        "awaiting_seguro_anterior": "awaiting_motorista_relacao",
        "awaiting_tempo_seguro_anterior": "awaiting_seguro_anterior"  
    }
    
    def handle_back(self, session, set_stage):
        lang = getattr(session, 'language', 'pt')
        atual = session.cliente_substage
        if atual in self.previous_steps:
            set_stage(session, new_quote_step=self.previous_steps[atual])
            return self.texts['back'][lang] if 'back' in self.texts else {
                'pt': "Você voltou para o passo anterior. Por favor, informe novamente:",
                'en': "You have returned to the previous step. Please provide the information again:",
                'es': "Has vuelto al paso anterior. Por favor, proporciona la información nuevamente:"
            }[lang]
        else:
            return self.texts['back_limit'][lang] if 'back_limit' in self.texts else {
                'pt': "Não é possível voltar mais",
                'en': "You can't go back any further",
                'es': "No es posible retroceder más"
            }[lang]

    def handle_nome(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        session.cliente_nome = message
        set_stage(session, new_quote_step="awaiting_birthdate")
        return self.texts['birthdate'][lang]

    def handle_birthdate(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        data = parse_data_flexivel(message)
        if data is not None:
            session.cliente_birthdate = datetime.strftime(data, '%m/%d/%Y')
            set_stage(session, new_quote_step='awaiting_driverlicense')
            return self.texts['driverlicense'][lang]
        return self.texts['birthdate_error'][lang] if 'birthdate_error' in self.texts else self.texts['birthdate'][lang]

    def handle_driverlicense(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        session.cliente_driver = message
        set_stage(session, new_quote_step="awaiting_driverstate")
        return self.texts['driver_state'][lang]

    def handle_driverstate(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        session.cliente_driver_state = message
        set_stage(session, new_quote_step='awaiting_address')
        return self.texts["address"][lang]

    def handle_address(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        session.cliente_address = message
        set_stage(session, new_quote_step="awaiting_tempo_endereco")
        return self.texts["tempo_endereco"][lang]

    def handle_tempo_address(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        session.cliente_tempo_endereco = message
        set_stage(session, new_quote_step="awaiting_veiculos")
        return self.texts["qtd_veiculos"][lang]

    def handle_qtd_veiculos(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        try:
            qtd = int(message)
            if qtd < 1:
                return self.texts["qtd_veiculos_erro"][lang]
            session.qtd_veiculos = qtd
            session.veiculo_atual = 1
            session.cliente_veiculos = [] 
            set_stage(session, new_quote_step='awaiting_vin')
            return True
        except ValueError:
            return self.texts['qtd_veiculos_erro'][lang]
    
    def handle_vin(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        vin = message.strip()
        if len(vin) != 17:
            return self.texts["vin_erro"][lang]
        session.cliente_veiculos.append({"vin": vin})
        flag_modified(session, "cliente_veiculos")
        set_stage(session, new_quote_step='awaiting_financiado')
        return True
    def handle_financiado(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        financiado = message.strip().lower()
        if financiado not in ["financiado", "quitado"]:
            return self.texts.get('financiado_erro', self.texts.get('financiad_erro', {})).get(lang, '')
        session.cliente_veiculos[-1]["financiado"] = financiado
        flag_modified(session, "cliente_veiculos")
        set_stage(session, new_quote_step='awaiting_tempo')
        return True
    def handle_tempo(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        tempo = message.strip()
        if not tempo:
            return self.texts["tempo_erro"][lang]
        session.cliente_veiculos[-1]["tempo"] = tempo
        flag_modified(session, "cliente_veiculos")
        if session.veiculo_atual < session.qtd_veiculos:
            session.veiculo_atual += 1
            set_stage(session, new_quote_step='awaiting_vin')
            return True
        else:
            set_stage(session, new_quote_step='awaiting_outros_motoristas')
            return self.texts["cadastrar_outros_motoristas"][lang]
    def handle_outros_motoristas(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        resposta = message.lower()
        if "nao" in resposta or 'não' in resposta or 'n' == resposta:
            set_stage(session, new_quote_step="awaiting_seguro_anterior")
            return self.texts["sem_outros_motoristas"][lang]
        elif "sim" in resposta or 's' == resposta:
            set_stage(session, new_quote_step='awaiting_qtd_motoristas')
            return self.texts["quantos_motoristas"][lang]
        else:
            return self.texts.get("cadastrar_outros_motoristas_erro", {}).get(lang, self.texts["cadastrar_outros_motoristas"][lang])
    def handle_qtd_motoristas(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        try:
            qtd = int(message)
            if qtd < 1:
                return self.texts["qtd_motorista_menor_erro"][lang]
            session.qtd_motoristas = qtd
            session.motorista_atual = 1
            session.cliente_motoristas = []
            set_stage(session, new_quote_step='awaiting_motorista_nome')
            return True
        except ValueError:
            return self.texts["qtd_motorista_erro"][lang]
    def handle_nome_motoristas(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        nome = message.strip()
        if not nome:
            return self.texts["nome_erro"][lang]
        session.cliente_motoristas.append({"nome": nome})
        flag_modified(session, "cliente_motoristas")
        set_stage(session, new_quote_step = 'awaiting_motorista_birthdate')
        return True
    
    def handle_birthdate_motoristas(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        data = parse_data_flexivel(message)
        if data is not None:
            if data > datetime.now():
                return self.texts["data_maior_erro"][lang]
            data_formatada = datetime.strftime(data, "%m/%d/%Y")
            session.cliente_motoristas[-1]["birthdate"] = data_formatada
            flag_modified(session, "cliente_motoristas")
            set_stage(session, new_quote_step='awaiting_motorista_driver')
            return True 
        else:
            return self.texts["birthdate_invalido"][lang]

    def handle_driver_motoristas(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        driverlicense = message.strip()
        if not driverlicense:
            return self.texts["motorista_driver_erro"][lang]
        session.cliente_motoristas[-1]["driver_license"] = driverlicense
        flag_modified(session, "cliente_motoristas")
        set_stage(session, new_quote_step='awaiting_motorista_state')
        return True

    def handle_driver_motoristas_state(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        driverstate = message.strip()
        if not driverstate:
            return self.texts["motorista_driver_state_erro"][lang]
        session.cliente_motoristas[-1]["driver_license_state"] = driverstate
        flag_modified(session, "cliente_motoristas")
        set_stage(session, new_quote_step='awaiting_motorista_relacao')
        return True

    def handle_motoristas_relacao(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        relacao = message.strip()
        if not relacao:
            return self.texts["relacao_vazia_erro"][lang]
        session.cliente_motoristas[-1]["relation"] = relacao
        flag_modified(session, "cliente_motoristas")
        if session.motorista_atual < session.qtd_motoristas:
            session.motorista_atual += 1
            set_stage(session, new_quote_step='awaiting_motorista_nome')
            return True
        else:
            set_stage(session, new_quote_step='awaiting_seguro_anterior')
            return self.texts["tem_seguro_anterior"][lang]
    
    def handle_tem_seguro_anterior(self, session, message, set_stage, concluir_cotacao, phone_number):
        lang = getattr(session, 'language', 'pt')
        if "nao" in message.lower() or 'não' in message.lower() or 'n' in message.lower() or "0" in message.lower():
            return concluir_cotacao(phone_number)
        elif "sim" in message.lower() or 's' in message.lower() or "si" in message.lower():
            set_stage(session, new_quote_step='awaiting_tempo_seguro_anterior')
            return self.texts["tempo_seguro_anterior"][lang]
        else:
            return self.texts["tem_seguro_anterior_erro"][lang]