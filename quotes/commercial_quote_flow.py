from quotes.base_quote_flow import BaseQuoteFlow
from sqlalchemy.orm.attributes import flag_modified
from quotes.messages import texts
class ComercialQuoteFlow(BaseQuoteFlow):
    texts = texts
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
        return self.texts['sem_outros_motoristas'][lang]

    def handle_address(self, session, message, set_stage):
        lang = getattr(session, 'language', 'pt')
        session.cliente_address = message
        set_stage(session, new_quote_step="awaiting_comercial_address")
        return self.texts["comercial_address"][lang]

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
            return self.texts['comercial_address'][lang]

        # Etapa específica do comercial
        elif session.cliente_substage == "awaiting_comercial_address":
            if "mesmo" in message.strip().lower() or "mesmo endereço" in message.strip().lower() or "mesmo endereco" in message.strip().lower():
                session.empresa_endereco = session.cliente_address 
            else:
                session.empresa_endereco = message
            set_stage(session, new_quote_step='awaiting_veiculos')
            return self.texts['qtd_veiculos_comercial'][lang]

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






