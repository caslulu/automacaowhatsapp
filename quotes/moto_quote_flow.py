from quotes.base_quote_flow import BaseQuoteFlow
from quotes.messages import texts

class MotoQuoteFlow(BaseQuoteFlow):
    texts = texts

    def handle(self, phone_number, message, session, set_stage, concluir_cotacao):
        lang = getattr(session, 'language', 'pt')

        if message.strip().lower() in ["voltar", "back"]:
            self.handle_back(session, set_stage)

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

        elif session.cliente_substage == "awaiting_tempo_endereco": 
            return self.handle_tempo_address(session, message, set_stage)

        elif session.cliente_substage == 'awaiting_veiculos':
            result = self.handle_qtd_veiculos(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 7 de 10) (Moto 1 de {session.qtd_veiculos}) Qual o VIN da moto?",
                    'en': f"(Step 7 of 10) (Motorcycle 1 of {session.qtd_veiculos}) What is the motorcycle's VIN?",
                    'es': f"(Paso 7 de 10) (Moto 1 de {session.qtd_veiculos}) ¿Cuál es el VIN de la moto?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_vin":
            return self.handle_vin(session, message, set_stage)

        elif session.cliente_substage == "awaiting_vehicle_confirmation":
            result =  self.handle_vehicle_confirmation(session, message, set_stage)
            if result == True:
                return {
                    'pt': f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) A moto é financiado ou quitado?",
                    'en': f"(Step 7 of 10) (Vehicle {session.veiculo_atual} of {session.qtd_veiculos}) Is the motorcycle financed or paid off?",
                    'es': f"(Paso 7 de 10) (Vehículo {session.veiculo_atual} de {session.qtd_veiculos}) ¿la moto está financiado o pagado?"
                }[lang]
            return result

        elif session.cliente_substage == 'awaiting_financiado':
            result = self.handle_financiado(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 7 de 10) (Moto {session.veiculo_atual} de {session.qtd_veiculos}) Há quanto tempo possui a moto?",
                    'en': f"(Step 7 of 10) (Motorcycle {session.veiculo_atual} of {session.qtd_veiculos}) How long have you owned the motorcycle?",
                    'es': f"(Paso 7 de 10) (Moto {session.veiculo_atual} de {session.qtd_veiculos}) ¿Cuánto tiempo ha tenido la moto?"
                }[lang]
            return result

        elif session.cliente_substage == 'awaiting_tempo':
            result = self.handle_tempo(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 7 de 10) (Moto {session.veiculo_atual} de {session.qtd_veiculos}) Qual o VIN da moto?",
                    'en': f"(Step 7 of 10) (Motorcycle {session.veiculo_atual} of {session.qtd_veiculos}) What is the motorcycle's VIN?",
                    'es': f"(Paso 7 de 10) (Moto {session.veiculo_atual} de {session.qtd_veiculos}) ¿Cuál es el VIN de la moto?"
                }[lang]
            return result

        elif session.cliente_substage == 'awaiting_outros_motoristas':
            result = self.handle_outros_motoristas(session, message, set_stage)
            return result

        elif session.cliente_substage == 'awaiting_qtd_motoristas':
            result = self.handle_qtd_motoristas(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 9 de 10) Qual o nome do motorista extra 1?",
                    'en': f"(Step 9 of 10) What is the name of extra driver 1?",
                    'es': f"(Paso 9 de 10) ¿Cuál es el nombre del conductor extra 1?"
                }[lang]
            return result

        elif session.cliente_substage == 'awaiting_motorista_nome':
            result = self.handle_nome_motoristas(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 9 de 10) Qual a data de nascimento do motorista extra {session.motorista_atual}?",
                    'en': f"(Step 9 of 10) What is the date of birth of extra driver {session.motorista_atual}?",
                    'es': f"(Paso 9 de 10) ¿Cuál es la fecha de nacimiento del conductor extra {session.motorista_atual}?"
                }[lang]
            return result

        elif session.cliente_substage == 'awaiting_motorista_birthdate':
            result = self.handle_birthdate_motoristas(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 9 de 10) Qual o número da CNH do motorista extra {session.motorista_atual}?",
                    'en': f"(Step 9 of 10) What is the driver license number of extra driver {session.motorista_atual}?",
                    'es': f"(Paso 9 de 10) ¿Cuál es el número de la CNH del conductor extra {session.motorista_atual}?"
                }[lang]
            return result

        elif session.cliente_substage == 'awaiting_motorista_driver':
            result = self.handle_driver_motoristas(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 9 de 10) Qual o estado da CNH do motorista extra {session.motorista_atual}?",
                    'en': f"(Step 9 of 10) What is the driver license state of extra driver {session.motorista_atual}?",
                    'es': f"(Paso 9 de 10) ¿Cuál es el estado de la CNH del conductor extra {session.motorista_atual}?"
                }[lang]
            return result

        elif session.cliente_substage == 'awaiting_motorista_state':
            result = self.handle_driver_motoristas_state(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 9 de 10) Qual a relação do motorista extra {session.motorista_atual} com o segurado?",
                    'en': f"(Step 9 of 10) What is the relationship of extra driver {session.motorista_atual} to the insured?",
                    'es': f"(Paso 9 de 10) ¿Cuál es la relación del conductor extra {session.motorista_atual} con el asegurado?"
                }[lang]
            return result

        elif session.cliente_substage == 'awaiting_motorista_relacao':
            result = self.handle_motoristas_relacao(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 9 de 10) Qual o nome do motorista extra {session.motorista_atual}?",
                    'en': f"(Step 9 of 10) What is the name of extra driver {session.motorista_atual}?",
                    'es': f"(Paso 9 de 10) ¿Cuál es el nombre del conductor extra {session.motorista_atual}?"
                }[lang]
            return result

        elif session.cliente_substage == 'awaiting_seguro_anterior':
            return self.handle_tem_seguro_anterior(session, message, set_stage, concluir_cotacao, phone_number)

        elif session.cliente_substage == 'awaiting_tempo_seguro_anterior':
            session.cliente_seguro_anterior = message
            return concluir_cotacao(phone_number)

        else:
            return {
                'pt': "Desculpe, não entendi sua resposta. Por favor, tente novamente ou digite 'voltar' para retornar ao passo anterior.",
                'en': "Sorry, I didn't understand your answer. Please try again or type 'back' to return to the previous step.",
                'es': "Disculpa, no entendí su respuesta. Por favor, inténtelo de nuevo o escriba 'volver' para regresar al paso anterior."
            }[lang]
