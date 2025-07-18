from quotes.base_quote_flow import BaseQuoteFlow
from sqlalchemy.orm.attributes import flag_modified
class ComercialQuoteFlow(BaseQuoteFlow):
    texts = {
        'birthdate': {
            'pt': "(Passo 2 de 10) Obrigado! Agora, qual a sua data de nascimento? (use o formato MM/DD/AAAA)",
            'en': "(Step 2 of 10) Thank you! Now, what is your date of birth? (use MM/DD/YYYY)",
            'es': "(Paso 2 de 10) ¡Gracias! Agora, ¿cuál es su fecha de nacimiento? (use MM/DD/AAAA)"
        },
        'birthdate_error': {
            'pt': "Ops! parece que você digitou a data de nascimento errada, tem como corrigir?",
            'en': "Oops! It looks like you entered the wrong date of birth, can you correct it?",
            'es': "¡Ups! Parece que ingresó la fecha de nacimiento incorrecta, ¿puede corregirla?"
        },
        'birthdate_invalido': {
            'pt': "Data inválida. Por favor, informe a data de nascimento no formato MM/DD/AAAA.",
            'en': "Invalid date. Please provide the date of birth in MM/DD/YYYY format.",
            'es': "Fecha inválida. Por favor, proporcione la fecha de nacimiento en formato MM/DD/AAAA."
        },
        'data_maior_erro': {
            'pt': "Data inválida. Por favor, informe uma data de nascimento válida.",
            'en': "Invalid date. Please provide a valid date of birth.",
            'es': "Fecha inválida. Por favor, proporcione una fecha de nacimiento válida."
        },
        'nome_erro': {
            'pt': "O nome não pode ficar em branco.",
            'en': "The name cannot be blank.",
            'es': "El nombre no puede estar en blanco."
        },
        'driverlicense': {
            'pt': "(Passo 3 de 10) Obrigado! Agora, qual o número da sua driver license ou cnh?",
            'en': "(Step 3 of 10) Thank you! Now, what is your driver license or CNH number?",
            'es': "(Paso 3 de 10) ¡Gracias! Agora, ¿cuál es su número de licencia de conducir o CNH?"
        },
        'driver_state': {
            'pt': "(Passo 4 de 10) Perfeito! Poderia me dizer qual o estado da sua driver license? (Se for internacional, diga internacional)",
            'en': "(Step 4 of 10) Perfect! Could you tell me the state of your driver license? (If international, say international)",
            'es': "(Paso 4 de 10) ¡Perfecto! ¿Podría decirme el estado de su licencia de conducir? (Si es internacional, diga internacional)"
        },
        'motorista_driver_erro': {
            'pt': "O número da CNH não pode ficar em branco. Por favor, informe corretamente.",
            'en': "The driver license number cannot be blank. Please provide it correctly.",
            'es': "El número de la licencia de conducir no puede estar en blanco. Por favor, infórmelo corretamente."
        },
        'motorista_driver_state_erro': {
            'pt': "O estado da CNH não pode ficar em branco. Por favor, informe corretamente.",
            'en': "The driver license state cannot be blank. Please provide it correctly.",
            'es': "El estado de la licencia de conducir no puede estar en blanco. Por favor, infórmelo corretamente."
        },
        'relacao_vazia_erro': {
            'pt': "A relação não pode ficar em branco. Por favor, informe corretamente (Ex: funcionário, sócio, etc).",
            'en': "The relationship cannot be blank. Please provide it correctly (e.g., employee, partner, etc).",
            'es': "La relación no puede estar en blanco. Por favor, infórmela correctamente (Ej: empleado, socio, etc)."
        },
        'address': {
            'pt': "(Passo 5 de 10) Obrigado! Poderia me dizer qual o seu endereço? (Inclua o zipcode, por favor!)",
            'en': "(Step 5 of 10) Thank you! Could you tell me your address? (Please include the zipcode!)",
            'es': "(Paso 5 de 10) ¡Gracias! ¿Podría decirme su dirección? (¡Incluya el código postal, por favor!)"
        },
        'comercial_address': {
            'pt': "(Passo 6 de 10) Qual o endereço comercial? (Se for o mesmo, digite 'mesmo')",
            'en': "(Step 6 of 10) What is the business address? (If the same, type 'same')",
            'es': "(Paso 6 de 10) ¿Cuál es la dirección comercial? (Si es la misma, escriba 'misma')"
        },
        'qtd_veiculos': {
            'pt': "(Passo 7 de 10) Quantos veículos você deseja adicionar?",
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
            'pt': "Todos os veículos foram cadastrados! Deseja cadastrar outros motoristas?",
            'en': "All vehicles have been registered! Would you like to add other drivers?",
            'es': "¡Todos los vehículos han sido registrados! ¿Desea agregar otros conductores?"
        },
        'sem_outros_motoristas': {
            'pt': "Ok, sem motoristas extras. Estamos quase acabando! Qual o nome da empresa?",
            'en': "Ok, no extra drivers. We're almost done! What is the company name?",
            'es': "Ok, sin conductores adicionales. ¡Ya casi terminamos! ¿Cuál es el nombre de la empresa?"
        },
        'quantos_motoristas': {
            'pt': "Entendido. Quantos motoristas extras você gostaria de adicionar?",
            'en': "Understood. How many extra drivers would you like to add?",
            'es': "Entendido. ¿Cuántos conductores adicionales le gustaría agregar?"
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
        'tempo_endereco': {
            'pt': "(Passo 6 de 10) Okay! Poderia me dizer quanto tempo você mora nesse endereço atual?",
            'en': "(Step 6 of 10) Okay! How long have you lived at your current address?",
            'es': "(Paso 6 de 10) ¡Bien! ¿Cuánto tiempo ha vivido en esta dirección atual?"
        },

        'cadastrar_outros_motoristas_erro': {
            'pt': "Não entendi sua resposta. Por favor, responda com 'sim' ou 'não'.",
            'en': "I didn't understand your answer. Please reply with 'yes' or 'no'.",
            'es': "No entendí su respuesta. Por favor, responda con 'sí' o 'no'."
        },
    }

    def handle_outros_motoristas(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        if "sim" in message.strip().lower() or "yes" in message.strip().lower():
            set_stage(session, new_quote_step='awaiting_qtd_motoristas')
            return self.texts['quantos_motoristas'][lang]
        elif "nao" in message.strip().lower() or "no" in message.strip().lower():
            set_stage(session, new_quote_step='awaiting_nome_empresa')
            return self.texts['sem_outros_motoristas'][lang]
        else:
            return self.texts['cadastrar_outros_motoristas_erro']

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
        set_stage(session, new_quote_step='awaiting_nome_empresa')
        return "Agora, qual o nome da empresa?"

    def handle_back(self, session, set_stage):
        if session.cliente_substage == 'awaiting_nome_empresa':
            set_stage(session, new_quote_step='awaiting_outros_motoristas')
        elif session.cliente_substage == 'awaiting_tem_usdot':
            set_stage(session, new_quote_step='awaiting_nome_empresa')
        elif session.cliente_substage == 'awaiting_usdot':
            set_stage(session, new_quote_step='awaiting_tem_usdot')
        elif session.cliente_substage == 'awaiting_numero_registro':
            set_stage(session, new_quote_step='awaiting_usdot')
        elif session.cliente_substage == 'awaiting_estrutura_empresa':
            set_stage(session, new_quote_step='awaiting_numero_registro')
        elif session.cliente_substage == 'awaiting_ramo':
            set_stage(session, new_quote_step='awaiting_estrutura_empresa')
        elif session.cliente_substage == 'awaiting_carga':
            set_stage(session, new_quote_step='awaiting_ramo')
        elif session.cliente_substage == 'awaiting_milhas_dia':
            set_stage(session, new_quote_step='awaiting_carga')
        else:
            super().handle_back(session, set_stage)

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
            # Após o endereço do cliente, pedir o endereço comercial
            self.handle_address(session, message, set_stage)
            set_stage(session, new_quote_step='awaiting_comercial_address')
            return self.texts['comercial_address'][lang]

        # Etapa específica do comercial
        elif session.cliente_substage == "awaiting_comercial_address":
            if "mesmo" in message.strip().lower() or "mesmo endereço" in message.strip().lower() or "mesmo endereco" in message.strip().lower():
                session.empresa_endereco = session.cliente_address 
            else:
                session.empresa_endereco = message
            set_stage(session, new_quote_step='awaiting_veiculos')
            return self.texts['qtd_veiculos'][lang]

        # Delegar etapas de veículos e motoristas para métodos herdados
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
                    'es': f"(Paso 7 de 10) (Vehículo {session.veiculo_atual} de {session.qtd_veiculos}) ¿El veículo está financiado ou pagado?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_financiado":
            result = self.handle_financiado(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Há quanto tempo possui o veículo?",
                    'en': f"(Step 7 of 10) (Vehicle {session.veiculo_atual} of {session.qtd_veiculos}) How long have you owned the vehicle?",
                    'es': f"(Paso 7 de 10) (Vehículo {session.veiculo_atual} de {session.qtd_veiculos}) ¿Cuánto tempo ha tenido el veículo?"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_tempo":
            result = self.handle_tempo(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Qual o VIN do veículo?",
                    'en': f"(Step 7 of 10) (Vehicle {session.veiculo_atual} of {session.qtd_veiculos}) What is the vehicle's VIN?",
                    'es': f"(Paso 7 de 10) (Vehículo {session.veiculo_atual} de {session.qtd_veiculos}) ¿Cuál é el VIN del veículo?"
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
                set_stage(session, new_quote_step="awaiting_motorista_birthdate")
                return {
                    'pt': f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a data de nascimento? (use o formato MM/DD/AAAA)",
                    'en': f"(Step 8 of 10) (Extra driver {session.motorista_atual} of {session.qtd_motoristas}) What is the date of birth? (use MM/DD/YYYY)",
                    'es': f"(Paso 8 de 10) (Conductor extra {session.motorista_atual} de {session.qtd_motoristas}) ¿Cuál es la fecha de nacimiento? (use MM/DD/AAAA)"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_motorista_birthdate":
            result = self.handle_birthdate_motoristas(session, message, set_stage)
            if result is True:
                set_stage(session, new_quote_step="awaiting_motorista_driver")
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
                    'pt': f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a relação desse motorista com a empresa? (Ex: funcionário, sócio, etc)",
                    'en': f"(Step 8 of 10) (Extra driver {session.motorista_atual} of {session.qtd_motoristas}) What is this driver's relationship to the company? (e.g., employee, partner, etc)",
                    'es': f"(Paso 8 de 10) (Conductor extra {session.motorista_atual} de {session.qtd_motoristas}) ¿Cuál es la relación de este conductor com a empresa? (Ej: empleado, socio, etc)"
                }[lang]
            return result

        elif session.cliente_substage == "awaiting_motorista_relacao":
            result = self.handle_motoristas_relacao(session, message, set_stage)
            if result is True:
                return {
                    'pt': f"(Passo 8 de 10) (Motorista extra {session.motorista_atual+1} de {session.qtd_motoristas}) Qual o nome do motorista extra?",
                    'en': f"(Step 8 of 10) (Extra driver {session.motorista_atual+1} of {session.qtd_motoristas}) What is the extra driver's name?",
                    'es': f"(Paso 8 de 10) (Conductor extra {session.motorista_atual+1} de {session.qtd_motoristas}) ¿Cuál es el nombre del conductor extra?"
                }[lang]
            return result

        # Etapas finais específicas do comercial
        elif session.cliente_substage == "awaiting_nome_empresa":
            session.empresa_nome = message
            set_stage(session, new_quote_step='awaiting_tem_usdot')
            return {
                'pt': "Obrigado, a sua empresa possui número usdot?",
                'en': "Thank you, does your company have a USDOT number?",
                'es': "Gracias, ¿su empresa tiene número USDOT?"
            }[lang]

        elif session.cliente_substage == "awaiting_tem_usdot":
            if "nao" in message.strip().lower() or "n" in message.strip().lower():
                set_stage(session, new_quote_step="awaiting_numero_registro")
                return {
                    'pt': "Não tem problema. Qual o número de registro da empresa?",
                    'en': "No problem. What is the company's registration number?",
                    'es': "No hay problema. ¿Cuál es el número de registro de la empresa?"
                }[lang]
            elif "sim" in message.strip().lower() or "s" in message.strip().lower():
                set_stage(session, new_quote_step='awaiting_usdot')
                return {
                    'pt': "Então, qual o número usdot?",
                    'en': "So, what is the USDOT number?",
                    'es': "Entonces, ¿cuál es el número USDOT?"
                }[lang]
            return {
                'pt': "Não entendi, digite sim ou não.",
                'en': "I didn't understand, type yes or no.",
                'es': "No entendí, escriba sí o no."
            }[lang]

        elif session.cliente_substage == "awaiting_usdot":
            session.empresa_usdot = message
            set_stage(session, new_quote_step='awaiting_numero_registro')
            return {
                'pt': "Perfeito! Qual o número de registro da empresa?",
                'en': "Perfect! What is the company's registration number?",
                'es': "¡Perfecto! ¿Cuál es el número de registro de la empresa?"
            }[lang]

        elif session.cliente_substage == "awaiting_numero_registro":
            session.empresa_numero_registro = message
            set_stage(session, new_quote_step="awaiting_estrutura_empresa")
            return {
                'pt': "Agora, qual a estrutura da empresa? (LLC, Sociedade, Corporação)",
                'en': "Now, what is the company's structure? (LLC, Partnership, Corporation)",
                'es': "Ahora, ¿cuál es la estructura de la empresa? (LLC, Sociedad, Corporación)"
            }[lang]

        elif session.cliente_substage == "awaiting_estrutura_empresa":
            session.empresa_estrutura = message
            set_stage(session, new_quote_step="awaiting_ramo")
            return {
                'pt': "Okay, qual o ramo da empresa? (Ex: Pintura, Transporte de carga...)",
                'en': "Okay, what is the company's business area? (e.g., Painting, Freight Transport...)",
                'es': "Bien, ¿cuál es el ramo de la empresa? (Ej: Pintura, Transporte de carga...)"
            }[lang]

        elif session.cliente_substage == "awaiting_ramo":
            session.empresa_ramo = message
            set_stage(session, new_quote_step="awaiting_carga")
            return {
                'pt': "Está quase acabando! Qual o tipo de carga que você carrega?",
                'en': "Almost done! What type of cargo do you carry?",
                'es': "¡Ya casi terminamos! ¿Qué tipo de carga transporta?"
            }[lang]

        elif session.cliente_substage == "awaiting_carga":
            session.empresa_tipo_carga = message
            set_stage(session, new_quote_step="awaiting_milhas_dia")
            return {
                'pt': "Para finalizar, quantas milhas em média você anda por dia?",
                'en': "To finish, how many miles do you drive on average per day?",
                'es': "Para finalizar, ¿cuántas millas recorre en promedio por día?"
            }[lang]

        elif session.cliente_substage == "awaiting_milhas_dia":
            try:
                milhas = int(message)
                session.empresa_milhas_trabalho = message
                session.empresa_milhas_ano = milhas * 365
            except ValueError:
                session.empresa_milhas_trabalho = message
            return concluir_cotacao(phone_number)






