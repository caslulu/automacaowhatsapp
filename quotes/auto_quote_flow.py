from base_quote_flow import BaseQuoteFlow

class AutoQuoteFlow(BaseQuoteFlow):
    texts = {
        'birthdate': "(Passo 2 de 10) Obrigado! Agora, qual a sua data de nascimento? (use o formato MM/DD/AAAA)",
        'birtdate_error': "Ops! parece que voce digitou a data de nascimento errada, tem como voce corrigir?",
        'driverlicense':  "(Passo 3 de 10) Obrigado! Agora, qual o numero da sua driver license ou cnh?",
        'driver_state':  "(Passo 4 de 10) Perfeito! Poderia me dizer qual o estado da sua driver license? (Se for internacional, diga internacional)",
        'address': "(Passo 5 de 10) Obrigado! Poderia me dizer qual o seu endereço? (Inclua o zipcode, por favor!)",
        'tempo_endereco': "(Passo 6 de 10) Okay! Poderia me dizer quanto tempo voce mora nesse endereço atual?",
        'qtd_veiculos':"(Passo 7 de 10) Poderia me dizer quantos veiculos voce deseja adicionar?",
        'qtd_veiculos_erro': "Por favor, informe um número válido de veículos.",
        'vin_erro':  "O VIN deve ter 17 caracteres. Por favor, verifique e envie novamente.",
        'financiado_erro':  "Por favor, responda apenas 'financiado' ou 'quitado'.",
        'tempo_erro': "Por favor, informe há quanto tempo você possui o veículo.",
        "cadastrar_outros_motoristas": "(Passo 8 de 10) Todos os veículos foram cadastrados! Deseja cadastrar outros motoristas?",
        "sem_outros_motoristas": "(Passo 9 de 10) Ok, sem motoristas extras. Estamos quase acabando! Você possui seguro atualmente ou teve seguro nos últimos 30 dias?",
        "quantos_motoristas":  "(Passo 8 de 10) Entendido. Quantos motoristas extras você gostaria de adicionar?",
        "cadastrar_outros_motoristas_erro": "Não entendi sua resposta. Por favor, responda com 'sim' ou 'não'.",
        "qtd_motorista_menor_erro":  "Por favor, digite um número válido (1 ou mais).",
        "qtd_motorista_erro":  "Não entendi. Por favor, digite apenas o número de motoristas extras.",
        "nome_erro": "O nome nao pode ficar em branco",
        "data_maior_erro":  "Data inválida. Por favor, informe uma data de nascimento válida.",
        "birthdate_invalido":  "Data inválida. Por favor, informe a data de nascimento no formato MM/DD/AAAA.",
        "motorista_driver_erro":  "O número da CNH não pode ficar em branco. Por favor, informe corretamente.",
        "motorista_driver_state_erro":  "O estado da CNH não pode ficar em branco. Por favor, informe corretamente.",
        "relacao_vazia_erro":  "A relação não pode ficar em branco. Por favor, informe corretamente (Ex: filho, esposa, amigo...).",
        "tem_seguro_anterior": "(Passo 9 de 10) Todos os motoristas extras foram cadastrados! Agora, você possui seguro atualmente ou teve seguro nos últimos 30 dias?",
        "tempo_seguro_anterior":  "(Passo 10 de 10) Para finalizar, quanto tempo de seguro voce tem/teve?",
        "tem_seguro_anterior_erro": "Desculpa, nao entendi a sua resposta! pode dizer sim ou nao?",

    }
    def handle(self, phone_number, message, session, set_stage, concluir_cotacao):    
        if message.strip().lower() in ["voltar", "back"]:
            self.handle_back(session, set_stage)
            #nome do cliente

        if session.cliente_substage == 'awaiting_name':
            return self.handle_nome(session, message, set_stage)

        #data de nascimento do cliente
        elif session.cliente_substage == "awaiting_birthdate":
            return self.handle_birthdate(session, message, set_stage)

        #driver do cliente
        elif session.cliente_substage == "awaiting_driverlicense":
            return self.handle_driverlicense(session, message, set_stage)

        #numero da driver do cliente
        elif session.cliente_substage == "awaiting_driverstate":        
            return self.handle_driverstate(session, message, set_stage)

        #endereco do cliente
        elif session.cliente_substage == "awaiting_address":
            return self.handle_address(session, message, set_stage)

        elif session.cliente_substage == "awaiting_tempo_endereco": 
            return self.handle_tempo_address(session, message, set_stage)

        #veiculos do cliente
        elif session.cliente_substage == "awaiting_veiculos":
            result = self.handle_qtd_veiculos(session, message, set_stage)
            if result is True:
                return f"(Passo 7 de 10) (Veículo 1 de {session.qtd_veiculos}) Qual o VIN do veículo?"
            return result

        elif session.cliente_substage == "awaiting_vin":
            result = self.handle_vin(session, message, set_stage)
            if result == True: 
                return f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) O veículo é financiado ou quitado?"
            return result

        elif session.cliente_substage == "awaiting_financiado":
            result = self.handle_financiado(session, message, set_stage)
            if result == True:
                return f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Há quanto tempo você possui esse veículo?"
            return result

        elif session.cliente_substage == "awaiting_tempo":
            result = self.handle_tempo(session, message, set_stage)
            if result == True:
                return f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Qual o VIN do veículo?"
            return result 

        elif session.cliente_substage == "awaiting_outros_motoristas":
                    #outros motoristas
            return self.handle_outros_motoristas(session, message, set_stage)

        elif session.cliente_substage == "awaiting_qtd_motoristas":
            result = self.handle_qtd_motoristas(session, message, set_stage)
            if result == True:
               return f"(Passo 8 de 10) (Motorista extra 1 de {session.qtd_motorista}) Qual o nome do motorista extra?"
            return result

        elif session.cliente_substage == "awaiting_motorista_nome":
            result = self.handle_nome_motoristas(session, message, set_stage)
            if result == True:
                return f"(Passo 8 de 10) ( Motorista extra {session.motorista_atual} de {session.qtd_motorista}) Qual a data de nascimento? (use o formato MM/DD/AAAA)"
            return result

        elif session.cliente_substage == "awaiting_motorista_birthdate":
            result = self.handle_birthdate_motoristas(session, message, set_stage)
            if result == True:
                return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o número da driver license desse motorista?"
            return result

        elif session.cliente_substage == "awaiting_motorista_driver":
            result = self.handle_driver_motoristas(session, message, set_stage)
            if result == True:
               return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o estado da driver license desse motorista?"
            return result

        elif session.cliente_substage == "awaiting_motorista_state":
            result = self.handle_driver_motoristas_state(session, message, set_stage)
            if result == True:
                return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a relação desse motorista com o motorista principal? (Ex: filho, esposa, amigo...)"
            return result

        elif session.cliente_substage == "awaiting_motorista_relacao":
            result = self.handle_motoristas_relacao(session, message, set_stage)
            if result == True:
                return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a data de nascimento? (use o formato MM/DD/AAAA)"
            return result

        #seguro anterior do cliente
        elif session.cliente_substage == "awaiting_seguro_anterior":
           return self.handle_tem_seguro_anterior(session, message, set_stage, concluir_cotacao, phone_number)
           
        elif session.cliente_substage == "awaiting_tempo_seguro_anterior":
            session.cliente_seguro_anterior = message
            return concluir_cotacao(phone_number)
    
            