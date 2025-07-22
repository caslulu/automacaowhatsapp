from quotes.base_quote_flow import BaseQuoteFlow
from quotes.messages import texts
class AutoQuoteFlow(BaseQuoteFlow):
    texts = texts
    def handle(self, phone_number, message, session, set_stage, concluir_cotacao):
        lang = getattr(session, 'language', 'pt')
        if message.strip().lower() in ["voltar", "back"]:
            self.handle_back(session, set_stage)
            #nome do cliente

        if session.cliente_substage == 'awaiting_name':
            return self.handle_nome(session, message, set_stage)

        elif session.cliente_substage == "awaiting_birthdate":
            return self.handle_birthdate(session, message, set_stage)

        elif session.cliente_substage == "awaiting_driverlicense":
            return self.handle_driverlicense(session, message, set_stage)

        elif session.cliente_substage == "awaiting_driverstate":        
            return self.handle_driverstate(session, message, set_stage)

        elif session.cliente_substage == "awaiting_address":
            return self.handle_address(session, message, set_stage)

        elif session.cliente_substage == "awaiting_tempo_endereco": 
            return self.handle_tempo_address(session, message, set_stage)

        elif session.cliente_substage == "awaiting_veiculos":
            result = self.handle_qtd_veiculos(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 7 de 10) (Veículo 1 de {session.qtd_veiculos}) Qual o VIN do veículo?",
                    'en': f"(Step 7 of 10) (Vehicle 1 of {session.qtd_veiculos}) What is the vehicle's VIN?",
                    'es': f"(Paso 7 de 10) (Vehículo 1 de {session.qtd_veiculos}) ¿Cuál es el VIN del vehículo?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_vin":
            return self.handle_vin(session, message, set_stage)

        elif session.cliente_substage == "awaiting_vehicle_confirmation":
            result =  self.handle_vehicle_confirmation(session, message, set_stage)
            if result == True:
                return {
                    'pt': f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) O veículo é financiado ou quitado?",
                    'en': f"(Step 7 of 10) (Vehicle {session.veiculo_atual} of {session.qtd_veiculos}) Is the vehicle financed or paid off?",
                    'es': f"(Paso 7 de 10) (Vehículo {session.veiculo_atual} de {session.qtd_veiculos}) ¿El vehículo está financiado o pagado?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_financiado":
            result = self.handle_financiado(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Há quanto tempo possui o veículo?",
                    'en': f"(Step 7 of 10) (Vehicle {session.veiculo_atual} of {session.qtd_veiculos}) How long have you owned the vehicle?",
                    'es': f"(Paso 7 de 10) (Vehículo {session.veiculo_atual} de {session.qtd_veiculos}) ¿Cuánto tiempo ha tenido el vehículo?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_tempo":
            result = self.handle_tempo(session, message, set_stage)
            if result is True:
                # Pergunta o VIN do próximo veículo
                return {
                    'pt': f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Qual o VIN do veículo?",
                    'en': f"(Step 7 of 10) (Vehicle {session.veiculo_atual} of {session.qtd_veiculos}) What is the vehicle's VIN?",
                    'es': f"(Paso 7 de 10) (Vehículo {session.veiculo_atual} de {session.qtd_veiculos}) ¿Cuál es el VIN del vehículo?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_outros_motoristas":
            return self.handle_outros_motoristas(session, message, set_stage)

        elif session.cliente_substage == "awaiting_qtd_motoristas":
            result = self.handle_qtd_motoristas(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 8 de 10) (Motorista extra 1 de {session.qtd_motoristas}) Qual o nome do motorista extra?",
                    'en': f"(Step 8 of 10) (Extra driver 1 of {session.qtd_motoristas}) What is the extra driver's name?",
                    'es': f"(Paso 8 de 10) (Conductor extra 1 de {session.qtd_motoristas}) ¿Cuál es el nombre del conductor extra?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_motorista_nome":
            result = self.handle_nome_motoristas(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a data de nascimento? (use o formato MM/DD/AAAA)",
                    'en': f"(Step 8 of 10) (Extra driver {session.motorista_atual} of {session.qtd_motoristas}) What is the date of birth? (use MM/DD/YYYY)",
                    'es': f"(Paso 8 de 10) (Conductor extra {session.motorista_atual} de {session.qtd_motoristas}) ¿Cuál es la fecha de nacimiento? (use MM/DD/AAAA)"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_motorista_birthdate":
            result = self.handle_birthdate_motoristas(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o número da driver license desse motorista?",
                    'en': f"(Step 8 of 10) (Extra driver {session.motorista_atual} of {session.qtd_motoristas}) What is this driver's license number?",
                    'es': f"(Paso 8 de 10) (Conductor extra {session.motorista_atual} de {session.qtd_motoristas}) ¿Cuál es el número de licencia de conducir de este conductor?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_motorista_driver":
            result = self.handle_driver_motoristas(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o estado da driver license desse motorista?",
                    'en': f"(Step 8 of 10) (Extra driver {session.motorista_atual} of {session.qtd_motoristas}) What is this driver's license state?",
                    'es': f"(Paso 8 de 10) (Conductor extra {session.motorista_atual} de {session.qtd_motoristas}) ¿Cuál es el estado de la licencia de conducir de este conductor?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_motorista_state":
            result = self.handle_driver_motoristas_state(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a relação desse motorista com o motorista principal? (Ex: filho, esposa, amigo...)",
                    'en': f"(Step 8 of 10) (Extra driver {session.motorista_atual} of {session.qtd_motoristas}) What is this driver's relationship to the main driver? (e.g., son, wife, friend...)",
                    'es': f"(Paso 8 de 10) (Conductor extra {session.motorista_atual} de {session.qtd_motoristas}) ¿Cuál es la relación de este conductor con el conductor principal? (Ej: hijo, esposa, amigo...)"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_motorista_relacao":
            result = self.handle_motoristas_relacao(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o nome do motorista extra?",
                    'en': f"(Step 8 of 10) (Extra driver {session.motorista_atual} of {session.qtd_motoristas}) What is the extra driver's name?",
                    'es': f"(Paso 8 de 10) (Conductor extra {session.motorista_atual} de {session.qtd_motoristas}) ¿Cuál es el nombre del conductor extra?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_seguro_anterior":
            return self.handle_tem_seguro_anterior(session, message, set_stage, concluir_cotacao, phone_number)

        elif session.cliente_substage == "awaiting_tempo_seguro_anterior":
            session.cliente_seguro_anterior = message
            return concluir_cotacao(phone_number)

        else:
            return {
                'pt': "Desculpe, não entendi sua resposta. Por favor, tente novamente ou digite 'voltar' para retornar ao passo anterior.",
                'en': "Sorry, I didn't understand your answer. Please try again or type 'back' to return to the previous step.",
                'es': "Disculpa, no entendí su respuesta. Por favor, inténtelo de nuevo o escriba 'volver' para regresar al paso anterior."
            }[lang]

