from utility import parse_data_flexivel
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified



from quotes.base_quote_flow import BaseQuoteFlow

class ComercialQuoteFlow(BaseQuoteFlow):
    texts = {
        'birthdate': "(Passo 2 de 10) Obrigado! Agora, qual a sua data de nascimento? (use o formato MM/DD/AAAA)",
        'birthdate_error': "Ops! parece que você digitou a data de nascimento errada, tem como corrigir?",
        'birthdate_invalido':  "Data inválida. Por favor, informe a data de nascimento no formato MM/DD/AAAA.",
        'data_maior_erro':  "Data inválida. Por favor, informe uma data de nascimento válida.",
        'nome_erro': "O nome não pode ficar em branco.",
        'driverlicense':  "(Passo 3 de 10) Obrigado! Agora, qual o número da sua driver license ou cnh?",
        'driver_state':  "(Passo 4 de 10) Perfeito! Poderia me dizer qual o estado da sua driver license? (Se for internacional, diga internacional)",
        'motorista_driver_erro':  "O número da CNH não pode ficar em branco. Por favor, informe corretamente.",
        'motorista_driver_state_erro':  "O estado da CNH não pode ficar em branco. Por favor, informe corretamente.",
        'relacao_vazia_erro':  "A relação não pode ficar em branco. Por favor, informe corretamente (Ex: funcionário, sócio, etc).",
        'address': "(Passo 5 de 10) Obrigado! Poderia me dizer qual o seu endereço? (Inclua o zipcode, por favor!)",
        'comercial_address': "(Passo 6 de 10) Qual o endereço comercial? (Se for o mesmo, digite 'mesmo')",
        'qtd_veiculos':"(Passo 7 de 10) Quantos veículos você deseja adicionar?",
        'qtd_veiculos_erro': "Por favor, informe um número válido de veículos.",
        'vin_erro':  "O VIN deve ter 17 caracteres. Por favor, verifique e envie novamente.",
        'financiado_erro':  "Por favor, responda apenas 'financiado' ou 'quitado'.",
        'tempo_erro': "Por favor, informe há quanto tempo você possui o veículo.",
        'cadastrar_outros_motoristas': "Todos os veículos foram cadastrados! Deseja cadastrar outros motoristas?",
        'sem_outros_motoristas': "Ok, sem motoristas extras. Estamos quase acabando! Qual o nome da empresa?",
        'quantos_motoristas':  "Entendido. Quantos motoristas extras você gostaria de adicionar?",
        'qtd_motorista_menor_erro':  "Por favor, digite um número válido (1 ou mais).",
        'qtd_motorista_erro':  "Não entendi. Por favor, digite apenas o número de motoristas extras.",
    }

    def handle(self, phone_number, message, session, set_stage, concluir_cotacao):
        # Etapas comuns delegadas ao BaseQuoteFlow
        if session.cliente_substage == 'awaiting_name':
            return self.handle_nome(session, message, set_stage)

        elif session.cliente_substage == 'awaiting_birthdate':
            return self.handle_birthdate(session, message, set_stage)

        elif session.cliente_substage == 'awaiting_driverlicense':
            return self.handle_driverlicense(session, message, set_stage)

        elif session.cliente_substage == 'awaiting_driverstate':
            return self.handle_driverstate(session, message, set_stage)

        elif session.cliente_substage == 'awaiting_address':
            return self.handle_address(session, message, set_stage)

        # Etapa específica do comercial
        elif session.cliente_substage == "awaiting_comercial_address":
            if "mesmo" in message.strip().lower() or "mesmo endereço" in message.strip().lower() or "mesmo endereco" in message.strip().lower():
                session.empresa_endereco = session.cliente_address 
            else:
                session.empresa_endereco = message
            set_stage(session, new_quote_step='awaiting_veiculos')
            return self.texts['qtd_veiculos']

        # Delegar etapas de veículos e motoristas para métodos herdados
        elif session.cliente_substage == "awaiting_veiculos":
            return self.handle_qtd_veiculos(session, message, set_stage)

        elif session.cliente_substage == "awaiting_vin":
            return self.handle_vin(session, message, set_stage)

        elif session.cliente_substage == "awaiting_financiado":
            return self.handle_financiado(session, message, set_stage)

        elif session.cliente_substage == "awaiting_tempo":
            return self.handle_tempo(session, message, set_stage)

        elif session.cliente_substage == "awaiting_outros_motoristas":
            return self.handle_outros_motoristas(session, message, set_stage)

        elif session.cliente_substage == "awaiting_qtd_motoristas":
            return self.handle_qtd_motoristas(session, message, set_stage)

        elif session.cliente_substage == "awaiting_motorista_nome":
            return self.handle_nome_motoristas(session, message, set_stage)

        elif session.cliente_substage == "awaiting_motorista_birthdate":
            return self.handle_birthdate_motoristas(session, message, set_stage)

        elif session.cliente_substage == "awaiting_motorista_driver":
            return self.handle_driver_motoristas(session, message, set_stage)

        elif session.cliente_substage == "awaiting_motorista_state":
            return self.handle_driver_motoristas_state(session, message, set_stage)

        elif session.cliente_substage == "awaiting_motorista_relacao":
            return self.handle_motoristas_relacao(session, message, set_stage)

        # Etapas finais específicas do comercial
        elif session.cliente_substage == "awaiting_nome_empresa":
            session.empresa_nome = message
            set_stage(session, new_quote_step='awaiting_tem_usdot')
            return "Obrigado, a sua empresa possui número usdot?"

        elif session.cliente_substage == "awaiting_tem_usdot":
            if "nao" in message.strip().lower() or "n" in message.strip().lower():
                set_stage(session, new_quote_step="awaiting_numero_registro")
                return "Não tem problema. Qual o número de registro da empresa?"
            elif "sim" in message.strip().lower() or "s" in message.strip().lower():
                set_stage(session, new_quote_step='awaiting_usdot')
                return "Então, qual o número usdot?"
            return "Não entendi, digite sim ou não."

        elif session.cliente_substage == "awaiting_usdot":
            session.empresa_usdot = message
            set_stage(session, new_quote_step='awaiting_numero_registro')
            return "Perfeito! Qual o número de registro da empresa?"

        elif session.cliente_substage == "awaiting_numero_registro":
            session.empresa_numero_registro = message
            set_stage(session, new_quote_step="awaiting_estrutura_empresa")
            return "Agora, qual a estrutura da empresa? (LLC, Sociedade, Corporação)"

        elif session.cliente_substage == "awaiting_estrutura_empresa":
            session.empresa_estrutura = message
            set_stage(session, new_quote_step="awaiting_ramo")
            return "Okay, qual o ramo da empresa? (Ex: Pintura, Transporte de carga...)"

        elif session.cliente_substage == "awaiting_ramo":
            session.empresa_ramo = message
            set_stage(session, new_quote_step="awaiting_carga")
            return "Está quase acabando! Qual o tipo de carga que você carrega?"

        elif session.cliente_substage == "awaiting_carga":
            session.empresa_tipo_carga = message
            set_stage(session, new_quote_step="awaiting_milhas_dia")
            return "Para finalizar, quantas milhas em média você anda por dia?"

        elif session.cliente_substage == "awaiting_milhas_dia":
            try:
                milhas = int(message)
                session.empresa_milhas_trabalho = message
                session.empresa_milhas_ano = milhas * 365
            except ValueError:
                session.empresa_milhas_trabalho = message
            return concluir_cotacao(phone_number)






