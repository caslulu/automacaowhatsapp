from base_quote_flow import BaseQuoteFlow

class AutoQuoteFlow(BaseQuoteFlow):
    texts = {
        'birthdate': {
            'pt': "(Passo 2 de 10) Obrigado! Agora, qual a sua data de nascimento? (use o formato MM/DD/AAAA)",
            'en': "(Step 2 of 10) Thank you! Now, what is your date of birth? (use MM/DD/YYYY)",
            'es': "(Paso 2 de 10) ¡Gracias! Ahora, ¿cuál es su fecha de nacimiento? (use MM/DD/AAAA)"
        },
        'birthdate_error': {
            'pt': "Ops! parece que você digitou a data de nascimento errada, tem como corrigir?",
            'en': "Oops! It looks like you entered the wrong date of birth, can you correct it?",
            'es': "¡Ups! Parece que ingresó la fecha de nacimiento incorrecta, ¿puede corregirla?"
        },
        'driverlicense': {
            'pt': "(Passo 3 de 10) Obrigado! Agora, qual o número da sua driver license ou cnh?",
            'en': "(Step 3 of 10) Thank you! Now, what is your driver license or CNH number?",
            'es': "(Paso 3 de 10) ¡Gracias! Ahora, ¿cuál es su número de licencia de conducir o CNH?"
        },
        'driver_state': {
            'pt': "(Passo 4 de 10) Perfeito! Poderia me dizer qual o estado da sua driver license? (Se for internacional, diga internacional)",
            'en': "(Step 4 of 10) Perfect! Could you tell me the state of your driver license? (If international, say international)",
            'es': "(Paso 4 de 10) ¡Perfecto! ¿Podría decirme el estado de su licencia de conducir? (Si es internacional, diga internacional)"
        },
        'address': {
            'pt': "(Passo 5 de 10) Obrigado! Poderia me dizer qual o seu endereço? (Inclua o zipcode, por favor!)",
            'en': "(Step 5 of 10) Thank you! Could you tell me your address? (Please include the zipcode!)",
            'es': "(Paso 5 de 10) ¡Gracias! ¿Podría decirme su dirección? (¡Incluya el código postal, por favor!)"
        },
        'tempo_endereco': {
            'pt': "(Passo 6 de 10) Okay! Poderia me dizer quanto tempo você mora nesse endereço atual?",
            'en': "(Step 6 of 10) Okay! How long have you lived at your current address?",
            'es': "(Paso 6 de 10) ¡Bien! ¿Cuánto tiempo ha vivido en esta dirección actual?"
        },
        'qtd_veiculos': {
            'pt': "(Passo 7 de 10) Poderia me dizer quantos veículos você deseja adicionar?",
            'en': "(Step 7 of 10) How many vehicles would you like to add?",
            'es': "(Paso 7 de 10) ¿Cuántos vehículos desea agregar?"
        },
        'qtd_veiculos_erro': {
            'pt': "Por favor, informe um número válido de veículos.",
            'en': "Please enter a valid number of vehicles.",
            'es': "Por favor, ingrese un número válido de vehículos."
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
            'pt': "Por favor, informe há quanto tempo você possui o veículo.",
            'en': "Please inform how long you have owned the vehicle.",
            'es': "Por favor, indique cuánto tiempo ha tenido el vehículo."
        },
        'cadastrar_outros_motoristas': {
            'pt': "(Passo 8 de 10) Todos os veículos foram cadastrados! Deseja cadastrar outros motoristas?",
            'en': "(Step 8 of 10) All vehicles have been registered! Would you like to add other drivers?",
            'es': "(Paso 8 de 10) ¡Todos los vehículos han sido registrados! ¿Desea agregar otros conductores?"
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
        'cadastrar_outros_motoristas_erro': {
            'pt': "Não entendi sua resposta. Por favor, responda com 'sim' ou 'não'.",
            'en': "I didn't understand your answer. Please reply with 'yes' or 'no'.",
            'es': "No entendí su respuesta. Por favor, responda con 'sí' o 'no'."
        },
        'qtd_motorista_menor_erro': {
            'pt': "Por favor, digite um número válido (1 ou mais).",
            'en': "Please enter a valid number (1 or more).",
            'es': "Por favor, ingrese un número válido (1 o más)."
        },
        'qtd_motorista_erro': {
            'pt': "Não entendi. Por favor, digite apenas o número de motoristas extras.",
            'en': "I didn't understand. Please enter only the number of extra drivers.",
            'es': "No entendí. Por favor, ingrese solo el número de conductores adicionales."
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
            'pt': "(Passo 9 de 10) Todos os motoristas extras foram cadastrados! Agora, você possui seguro atualmente ou teve seguro nos últimos 30 dias?",
            'en': "(Step 9 of 10) All extra drivers have been registered! Now, do you currently have insurance or have you had insurance in the last 30 days?",
            'es': "(Paso 9 de 10) ¡Todos los conductores adicionales han sido registrados! Ahora, ¿tiene seguro actualmente o ha tenido seguro en los últimos 30 días?"
        },
        'tempo_seguro_anterior': {
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
            result = self.handle_vin(session, message, set_stage)
            if result is True:
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
                if session.veiculo_atual < session.qtd_veiculos:
                    return {
                        'pt': f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Qual o VIN do veículo?",
                        'en': f"(Step 7 of 10) (Vehicle {session.veiculo_atual} of {session.qtd_veiculos}) What is the vehicle's VIN?",
                        'es': f"(Paso 7 de 10) (Vehículo {session.veiculo_atual} de {session.qtd_veiculos}) ¿Cuál es el VIN del vehículo?"
                    }[lang]
                else:
                    return self.texts['cadastrar_outros_motoristas'][lang]
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
                if session.motorista_atual < session.qtd_motoristas:
                    return {
                        'pt': f"(Passo 8 de 10) (Motorista extra {session.motorista_atual+1} de {session.qtd_motoristas}) Qual o nome do motorista extra?",
                        'en': f"(Step 8 of 10) (Extra driver {session.motorista_atual+1} of {session.qtd_motoristas}) What is the extra driver's name?",
                        'es': f"(Paso 8 de 10) (Conductor extra {session.motorista_atual+1} de {session.qtd_motoristas}) ¿Cuál es el nombre del conductor extra?"
                    }[lang]
                else:
                    return self.texts['tem_seguro_anterior'][lang]
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

