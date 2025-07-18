from quotes.base_quote_flow import BaseQuoteFlow

class MotoQuoteFlow(BaseQuoteFlow):
    texts = {
        'birthdate': {
            'pt': "(Passo 2 de 10) Obrigado! Agora, qual a sua data de nascimento? (use o formato MM/DD/AAAA)",
            'en': "(Step 2 of 10) Thank you! Now, what is your date of birth? (use MM/DD/YYYY)",
            'es': "(Paso 2 de 10) ¡Gracias! Ahora, ¿cuál es su fecha de nacimiento? (use MM/DD/AAAA)"
        },
        'driverlicense': {
            'pt': "(Passo 3 de 10) Obrigado! Agora, qual o número da sua driver license, cnh ou passaporte?",
            'en': "(Step 3 of 10) Thank you! Now, what is your driver license or passporte?",
            'es': "(Paso 3 de 10) ¡Gracias! Ahora, ¿cuál es su número de licencia de conducir o pasaporte?"
        },
        'driver_state': {
            'pt': "(Passo 4 de 10) Perfeito! Qual o estado da sua driver license? (Se for internacional, diga internacional)",
            'en': "(Step 4 of 10) Perfect! What is the state of your driver license? (If international, say international)",
            'es': "(Paso 4 de 10) ¡Perfecto! ¿Cuál es el estado de su licencia de conducir? (Si es internacional, diga internacional)"
        },
        'address': {
            'pt': "(Passo 5 de 10) Obrigado! Qual o seu endereço? (Inclua o zipcode, por favor!)",
            'en': "(Step 5 of 10) Thank you! What is your address? (Please include the zipcode!)",
            'es': "(Paso 5 de 10) ¡Gracias! ¿Cuál es su dirección? (¡Incluya el código postal, por favor!)"
        },
        'tempo_endereco': {
            'pt': "(Passo 6 de 10) Há quanto tempo você mora nesse endereço?",
            'en': "(Step 6 of 10) How long have you lived at this address?",
            'es': "(Paso 6 de 10) ¿Cuánto tiempo ha vivido en esta dirección?"
        },
        'qtd_veiculos': {
            'pt': "(Passo 6 de 10) Quantas motos você deseja adicionar?",
            'en': "(Step 6 of 10) How many motorcycles would you like to add?",
            'es': "(Paso 6 de 10) ¿Cuántas motos desea agregar?"
        },
        'qtd_veiculos_erro': {
            'pt': "Por favor, informe um número válido de motos.",
            'en': "Please enter a valid number of motorcycles.",
            'es': "Por favor, ingrese un número válido de motos."
        },
        'vin_erro': {
            'pt': "O VIN deve ter 17 caracteres. Por favor, verifique e envie novamente.",
            'en': "The VIN must be 17 characters. Please check and send again.",
            'es': "El VIN debe tener 17 caracteres. Por favor, verifique y envíe nuevamente."
        },
        'financiado_erro': {
            'pt': "Por favor, responda apenas 'financiado' ou 'quitado'.",
            'en': "Please answer only 'financed' or 'paid off'.",
            'es': "Por favor, responda solo 'financiado' o 'pagado'."
        },
        'tempo_erro': {
            'pt': "Por favor, informe há quanto tempo você possui a moto.",
            'en': "Please inform how long you have owned the motorcycle.",
            'es': "Por favor, indique cuánto tiempo ha tenido la moto."
        },
        'cadastrar_outros_motoristas': {
            'pt': "(Passo 8 de 10) Todas as motos foram cadastradas! Deseja cadastrar outros motoristas?",
            'en': "(Step 8 of 10) All motorcycles have been registered! Would you like to add other drivers?",
            'es': "(Paso 8 de 10) ¡Todas las motos han sido registradas! ¿Desea agregar otros conductores?"
        },
        'sem_outros_motoristas': {
            'pt': "(Passo 9 de 10) Ok, sem motoristas extras. Estamos quase acabando! Você possui seguro atualmente ou teve seguro nos últimos 30 dias?",
            'en': "(Step 9 of 10) Ok, no extra drivers. We're almost done! Do you currently have insurance or have you had insurance in the last 30 days?",
            'es': "(Paso 9 de 10) Ok, sin conductores adicionales. ¡Ya casi terminamos! ¿Actualmente tiene seguro o ha tenido seguro en los últimos 30 días?"
        },
        'quantos_motoristas': {
            'pt': "(Passo 8 de 10) Entendido. Quantos motoristas extras você gostaria de adicionar?",
            'en': "(Step 8 of 10) Understood. How many extra drivers would you like to add?",
            'es': "(Paso 8 de 10) Entendido. ¿Cuántos conductores adicionales le gustaría agregar?"
        },
        'qtd_motorista_erro': {
            'pt': "Não entendi. Por favor, digite apenas o número de motoristas extras.",
            'en': "I didn't understand. Please enter only the number of extra drivers.",
            'es': "No entendí. Por favor, ingrese solo el número de conductores adicionales."
        },
        'qtd_motorista_menor_erro': {
            'pt': "Por favor, digite um número válido (1 ou mais).",
            'en': "Please enter a valid number (1 or more).",
            'es': "Por favor, ingrese un número válido (1 o más)."
        },
        'nome_erro': {
            'pt': "O nome não pode ficar em branco.",
            'en': "The name cannot be blank.",
            'es': "El nombre no puede estar en blanco."
        },
        'data_maior_erro': {
            'pt': "Data inválida. Por favor, informe uma data de nascimento válida.",
            'en': "Invalid date. Please provide a valid date of birth.",
            'es': "Fecha inválida. Por favor, proporcione una fecha de nacimiento válida."
        },
        'birthdate_invalido': {
            'pt': "Data inválida. Por favor, informe a data de nascimento no formato MM/DD/AAAA.",
            'en': "Invalid date. Please provide the date of birth in MM/DD/YYYY format.",
            'es': "Fecha inválida. Por favor, proporcione la fecha de nacimiento en formato MM/DD/AAAA."
        },
        'motorista_driver_erro': {
            'pt': "O número da CNH não pode ficar em branco. Por favor, informe corretamente.",
            'en': "The driver license number cannot be blank. Please provide it correctly.",
            'es': "El número de la licencia de conducir no puede estar en blanco. Por favor, infórmelo correctamente."
        },
        'motorista_driver_state_erro': {
            'pt': "O estado da CNH não pode ficar em branco. Por favor, informe corretamente.",
            'en': "The driver license state cannot be blank. Please provide it correctly.",
            'es': "El estado de la licencia de conducir no puede estar en blanco. Por favor, infórmelo correctamente."
        },
        'relacao_vazia_erro': {
            'pt': "A relação não pode ficar em branco. Por favor, informe corretamente (Ex: filho, esposa, amigo...).",
            'en': "The relationship cannot be blank. Please provide it correctly (e.g., son, wife, friend...).",
            'es': "La relación no puede estar en blanco. Por favor, infórmela correctamente (Ej: hijo, esposa, amigo...)."
        },
        'tem_seguro_anterior': {
            'pt': "(Passo 10 de 10) Para finalizar, quanto tempo de seguro você tem/teve?",
            'en': "(Step 10 of 10) To finish, how long have you had insurance?",
            'es': "(Paso 10 de 10) Para finalizar, ¿cuánto tiempo de seguro ha tenido?"
        },
        'tem_seguro_anterior_erro': {
            'pt': "Desculpa, não entendi a sua resposta! pode dizer sim ou não?",
            'en': "Sorry, I didn't understand your answer! Can you say yes or no?",
            'es': "Disculpa, ¡no entendí su respuesta! ¿Puede decir sí o no?"
        }
    }

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

        elif session.cliente_substage == 'awaiting_vin':
            result = self.handle_vin(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 7 de 10) (Moto {session.veiculo_atual} de {session.qtd_veiculos}) A moto é financiada ou quitada?",
                    'en': f"(Step 7 of 10) (Motorcycle {session.veiculo_atual} of {session.qtd_veiculos}) Is the motorcycle financed or paid off?",
                    'es': f"(Paso 7 de 10) (Moto {session.veiculo_atual} de {session.qtd_veiculos}) ¿La moto está financiada o pagada?"
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
