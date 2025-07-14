from utility import parse_data_flexivel
from datetime import datetime


class ComercialQuoteFlow:
    def __init__(self):
        pass
    def handle(self, phone_number, message, session, set_stage, concluir_cotacao):     
           #nome do cliente
        if session.cliente_substage == 'awaiting_name':
            session.cliente_nome = message
            set_stage(session, new_quote_step='awaiting_birthdate')
            return "Obrigado! Agora, qual a sua data de nascimento? (use o formato MM/DD/AAAA)"
        
        #data de nascimento do cliente
        elif session.cliente_substage == "awaiting_birthdate":
            data = parse_data_flexivel(message)
            if data is not None:
                data_formatada = datetime.strftime(data, "%m/%d/%Y")
                session.cliente_birthdate= data_formatada
                set_stage(session, new_quote_step='awaiting_driverlicense')
                return "Obrigado! Agora, qual o numero da sua driver license ou cnh?"
            else:
                return "Ops! parece que voce digitou a data de nascimento errada, tem como voce corrigir?"
            
        #driver do cliente
        elif session.cliente_substage == "awaiting_driverlicense":
            session.cliente_driver = message
            set_stage(session, new_quote_step='awaiting_driverstate')
            return "Perfeito! Poderia me dizer qual o estado da sua driver license? (Se for internacional, diga internacional)"
        
        #numero da driver do cliente
        elif session.cliente_substage == "awaiting_driverstate":
            session.cliente_driver_state = message
            set_stage(session, new_quote_step='awaiting_address')
            return "Obrigado! Poderia me dizer qual o seu endereço? (Inclua o zipcode, por favor!)"
        elif session.cliente_substage == "awaiting_address":
            session.cliente_address = message
            set_stage(session, new_quote_step='awaiting_comercial_address')
            return "Obrigado! Agora, qual é o endereço da empresa? (Se for o mesmo, apenas digite mesmo)"
        
        #endereco do cliente
        elif session.cliente_substage == "awaiting_comercial_address":
            if "mesmo" in message.strip().lower() or "mesmo endereço" in message.strip().lower() or "mesmo endereco" in message.strip().lower():
                session.empresa_endereco = session.cliente_address 
            else:
                session.empresa_endereco = message
            set_stage(session, new_quote_step='awaiting_veiculos')
            return "Okay! Poderia me dizer quantos veiculos voce deseja adicionar?"
        
        #veiculos do cliente
        elif session.cliente_substage == "awaiting_veiculos":
            try:
                qtd = int(message)
                if qtd < 1:
                    return "Por favor, informe um número válido de veículos."
                session.qtd_veiculos = qtd
                session.veiculo_atual = 1
                session.cliente_veiculos = []
                set_stage(session, new_quote_step='awaiting_vin')
                return f"(Veículo 1 de {qtd}) Qual o VIN do veículo?"
            except ValueError:
                return "Por favor, informe um número válido de veículos."

        elif session.cliente_substage == "awaiting_vin":
            vin = message.strip()
            if len(vin) != 17:
                return "O VIN deve ter 17 caracteres. Por favor, verifique e envie novamente."
            veiculos_lista = session.cliente_veiculos or []
            veiculos_lista.append({"vin": vin})
            session.cliente_veiculos = veiculos_lista

            set_stage(session, new_quote_step='awaiting_financiado')
            return f"(Veículo {session.veiculo_atual} de {session.qtd_veiculos}) O veículo é financiado ou quitado?"

        elif session.cliente_substage == "awaiting_financiado":
            financiado = message.strip().lower()
            if financiado not in ["financiado", "quitado"]:
                return "Por favor, responda apenas 'financiado' ou 'quitado'."
            veiculos_lista = session.cliente_veiculos
            veiculos_lista[-1]["financiado"] = financiado
            session.cliente_veiculos = veiculos_lista
            set_stage(session, new_quote_step='awaiting_tempo')

            return f"(Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Há quanto tempo você possui esse veículo?"

        elif session.cliente_substage == "awaiting_tempo":
            tempo = message.strip()
            if not tempo:
                return "Por favor, informe há quanto tempo você possui o veículo."

            veiculos_lista = session.cliente_veiculos
            veiculos_lista[-1]["tempo"] = tempo
            session.cliente_veiculos = veiculos_lista

            if session.veiculo_atual < session.qtd_veiculos:
                session.veiculo_atual += 1
                set_stage(session, new_quote_step='awaiting_vin')
                return f"(Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Qual o VIN do veículo?"
            else:
                set_stage(session, new_quote_step='awaiting_outros_motoristas')
                return "Todos os veículos foram cadastrados! Deseja cadastrar outros motoristas?"
            
        elif session.cliente_substage == "awaiting_outros_motoristas":
            resposta = message.lower()
            if "nao" in resposta or 'não' in resposta or 'n' == resposta:
                set_stage(session, new_quote_step="awaiting_nome_empresa")
                return "Ok, sem motoristas extras. Estamos quase acabando! Qual o nome da empresa?"
            elif "sim" in resposta or 's' == resposta:
                set_stage(session, new_quote_step='awaiting_qtd_motoristas')
                return "Entendido. Quantos motoristas extras você gostaria de adicionar?"
            else:
                return "Não entendi sua resposta. Por favor, responda com 'sim' ou 'não'."
            
        #outros motoristas
        elif session.cliente_substage == "awaiting_qtd_motoristas":
            try:
                qtd = int(message)
                if qtd < 1:
                    return "Por favor, digite um número válido (1 ou mais)."
                session.qtd_motoristas = qtd
                session.motorista_atual = 1
                session.cliente_motoristas = []
                set_stage(session, new_quote_step='awaiting_motorista_birthdate')
                return f"(Motorista extra 1 de {qtd}) Qual a data de nascimento? (use o formato MM/DD/AAAA)"
            except ValueError:
                return "Não entendi. Por favor, digite apenas o número de motoristas extras."

        elif session.cliente_substage == "awaiting_motorista_birthdate":
            data = parse_data_flexivel(message)
            if data is not None:
                if data > datetime.now():
                    return "Data inválida. Por favor, informe uma data de nascimento válida."
                data_formatada = datetime.strftime(data, "%m/%d/%Y")
                motorista_lista = session.cliente_motoristas or []
                motorista_lista.append({"birthdate": data_formatada})
                session.cliente_motoristas = motorista_lista
                set_stage(session, new_quote_step='awaiting_motorista_driver')
                return f"(Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o número da driver license desse motorista?"
            else:
                return "Data inválida. Por favor, informe a data de nascimento no formato MM/DD/AAAA."

        elif session.cliente_substage == "awaiting_motorista_driver":
            driverlicense = message.strip()
            if not driverlicense:
                return "O número da CNH não pode ficar em branco. Por favor, informe corretamente."
            motorista_lista = session.cliente_motoristas
            motorista_lista[-1]["driver_license"] = driverlicense
            session.cliente_motoristas = motorista_lista
            set_stage(session, new_quote_step='awaiting_motorista_state')
            return f"(Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o estado da driver license desse motorista?"

        elif session.cliente_substage == "awaiting_motorista_state":
            driverstate = message.strip()
            if not driverstate:
                return "O estado da CNH não pode ficar em branco. Por favor, informe corretamente."
            motorista_lista = session.cliente_motoristas
            motorista_lista[-1]["driver_license_state"] = driverstate
            session.cliente_motoristas = motorista_lista

            if session.motorista_atual < session.qtd_motoristas:
                session.motorista_atual += 1
                set_stage(session, new_quote_step='awaiting_motorista_birthdate')
                return f"(Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a data de nascimento? (use o formato MM/DD/AAAA)"
            else:
                set_stage(session, new_quote_step='awaiting_nome_empresa')
                return "Todos os motoristas extras foram cadastrados! Qual o nome da empresa?"
            
        elif session.cliente_substage == "awaiting_nome_empresa":
            session.empresa_nome = message
            set_stage(session, new_quote_step='awaiting_tem_usdot')
            return "Obrigado, A sua empresa possui numero usdot?"
        
        elif session.cliente_substage == "awaiting_tem_usdot":
            if "nao" in message.strip().lower() or "n" in message.strip().lower():
                set_stage(session, new_quote_step="awaiting_numero_registro")
                return "Nao tem problema. Qual o numero de registro da empresa?"
            elif "sim" in message.strip().lower() or "s" in message.strip().lower():
                set_stage(session, new_quote_step='awaiting_usdot')
                return "Entao, qual o numero usdot?"
            return "Nao entendi, digite sim ou nao."
        elif session.cliente_substage == "awaiting_usdot":
            session.empresa_usdot = message
            set_stage(session, new_quote_step='awaiting_numero_registro')
            return "Perfeito! Qual o numero de registro da empresa?"
        
        elif session.cliente_substage == "awaiting_numero_registro":
            session.empresa_numero_registro = message
            set_stage(session, new_quote_step="awaiting_estrutura_empresa")
            return "Agora, Qual a estrutura da empresa? (LLC, Sociedade, Corporação)"
        elif session.cliente_substage == "awaiting_estrutura_empresa":
            session.empresa_estrutura = message
            set_stage(session, new_quote_step="awaiting_ramo")
            return "Okay, qual o ramo da empresa? (Ex: Pintura, Tranporte de carga...)"
        elif session.cliente_substage == "awaiting_ramo":
            session.empresa_ramo = message
            set_stage(session, new_quote_step="awaiting_carga")
            return "Esta quase acabando! Qual o tipo de carga que voce carrega?"
        elif session.cliente_substage == "awaiting_carga":
            session.empresa_tipo_carga = message
            set_stage(session, new_quote_step="awaiting_milhas_dia")
            return "Para finalizar, quantas milhas em media você anda por dia?"
        elif session.cliente_substage == "awaiting_milhas_dia":
            try:
                milhas = int(message)
                session.empresa_milhas_trabalho = message
                session.empresa_milhas_ano = milhas * 365
            except ValueError:    
                session.empresa_milhas_trabalho = message
            return concluir_cotacao(phone_number)



        
     
    
            