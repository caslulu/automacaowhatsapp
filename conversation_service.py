from twilio.twiml.messaging_response import MessagingResponse
from utility import parse_data_flexivel
from datetime import datetime
from model import Cliente
from extensions import db





class ConversationFlow:
    def __init__(self):
        self.user_sessions = {}
    
    def get_user_session(self, phone_number):
        cliente = Cliente.query.filter_by(phone_number=phone_number).first()
        
        if not cliente:
            cliente = Cliente(phone_number=phone_number, cliente_stage='initial')
            db.session.add(cliente)
            db.session.commit()  
        return cliente

    def set_stage(self, cliente, new_stage=None, new_quote_step=None):
        if new_stage:
            cliente.cliente_stage = new_stage
        
        if new_quote_step:
            cliente.quote_step = new_quote_step
        db.session.commit()


    
    def process_message(self, phone_number, message):

        if message.strip().lower() in ["reiniciar", "restart"]:
            self.reset_session(phone_number)
            return "Conversa reiniciada, Digite um 'oi' para começar novamente."
        
        session = self.get_user_session(phone_number)
        stage = session.cliente_stage
        
        if stage == 'initial':
            return self.handle_initial(phone_number)
        elif stage == 'waiting_option':
            return self.handle_options(phone_number, message)
        elif stage == 'auto_quote':
            return self.handle_quote(phone_number, message)
        elif stage == 'suporte':
            return self.handle_support(phone_number, message)
        else:
            return "Digite reiniciar para começar novamente"
        

    def handle_initial(self, phone_number):
        session = self.get_user_session(phone_number)
        self.set_stage(session, new_stage='waiting_option')

        return "Ola! Como posso ajudar voce? \n 1- Cotação para veiculo\n 2- Suporte\n Para voltar para o inicio, digite reinciar."
    
    def handle_options(self, phone_number, message):
        session = self.get_user_session(phone_number)
        if "1" in message or "quote" in message or "cotacao" in message:
            self.set_stage(session, new_stage='auto_quote', new_quote_step='awaiting_name')
            return "(Passo 1 de 10) Otimo! Para comecar, qual o seu nome?"
        elif "2" in message or "suporte" in message:
            self.set_stage(session, new_stage='suporte')
            return "Entendi, qual problema voce esta tendo? Iremos conectar voce com um agente."
        elif "reiniciar" in message.lower() or "restart" in message.lower():
            self.reset_session(phone_number)
        
    def handle_quote(self, phone_number, message):
        session = self.get_user_session(phone_number)
        #nome do cliente
        if session.cliente_substage == 'awaiting_name':
            session.cliente_nome = message
            self.set_stage(session, new_quote_step='awaiting_birthdate')
            return "(Passo 2 de 10) Obrigado! Agora, qual a sua data de nascimento? (use o formato MM/DD/AAAA)"
        
        #data de nascimento do cliente
        elif session.cliente_substage == "awaiting_birthdate":
            data = parse_data_flexivel(message)
            if data is not None:
                data_formatada = datetime.strftime(data, "%m/%d/%Y")
                session.cliente_birthdate= data_formatada
                self.set_stage(session, new_quote_step='awaiting_driverlicense')
                return "(Passo 3 de 10) Obrigado! Agora, qual o numero da sua driver license ou cnh?"
            else:
                return "Ops! parece que voce digitou a data de nascimento errada, tem como voce corrigir?"
            
        #driver do cliente
        elif session.cliente_substage == "awaiting_driverlicense":
            session.cliente_driver = message
            self.set_stage(session, new_quote_step='awaiting_driverstate')
            return "(Passo 4 de 10) Perfeito! Poderia me dizer qual o estado da sua driver license? (Se for internacional, diga internacional)"
        
        #numero da driver do cliente
        elif session.cliente_substage == "awaiting_driverstate":
            session.cliente_driver_state = message
            self.set_stage(session, new_quote_step='awaiting_address')
            return ("(Passo 5 de 10) Obrigado! Poderia me dizer qual o seu endereço? (Inclua o zipcode, por favor!)")
        
        #endereco do cliente
        elif session.cliente_substage == "awaiting_address":
            session.cliente_address = message
            self.set_stage(session, new_quote_step='awaiting_veiculos')
            return ("(Passo 6 de 10) Okay! Poderia me dizer quantos veiculos voce deseja adicionar?")
        
        #veiculos do cliente
        elif session.cliente_substage == "awaiting_veiculos":
            try:
                qtd = int(message)
                if qtd < 1:
                    return "Por favor, informe um número válido de veículos."
                session.qtd_veiculos = qtd
                session.veiculo_atual = 1
                session.cliente_veiculos = []
                self.set_stage(session, new_quote_step='awaiting_vin')
                return f"(Passo 7 de 10) (Veículo 1 de {qtd}) Qual o VIN do veículo?"
            except ValueError:
                return "Por favor, informe um número válido de veículos."

        elif session.cliente_substage == "awaiting_vin":
            vin = message.strip()
            if len(vin) != 17:
                return "O VIN deve ter 17 caracteres. Por favor, verifique e envie novamente."
            veiculos_lista = session.cliente_veiculos or []
            veiculos_lista.append({"vin": vin})
            session.cliente_veiculos = veiculos_lista

            self.set_stage(session, new_quote_step='awaiting_financiado')
            return f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) O veículo é financiado ou quitado?"

        elif session.cliente_substage == "awaiting_financiado":
            financiado = message.strip().lower()
            if financiado not in ["financiado", "quitado"]:
                return "Por favor, responda apenas 'financiado' ou 'quitado'."
            veiculos_lista = session.cliente_veiculos
            veiculos_lista[-1]["financiado"] = financiado
            session.cliente_veiculos = veiculos_lista
            self.set_stage(session, new_quote_step='awaiting_tempo')

            return f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Há quanto tempo você possui esse veículo?"

        elif session.cliente_substage == "awaiting_tempo":
            tempo = message.strip()
            if not tempo:
                return "Por favor, informe há quanto tempo você possui o veículo."

            veiculos_lista = session.cliente_veiculos
            veiculos_lista[-1]["tempo"] = tempo
            session.cliente_veiculos = veiculos_lista

            if session.veiculo_atual < session.qtd_veiculos:
                session.veiculo_atual += 1
                self.set_stage(session, new_quote_step='awaiting_vin')
                return f"(Passo 7 de 10) (Veículo {session.veiculo_atual} de {session.qtd_veiculos}) Qual o VIN do veículo?"
            else:
                self.set_stage(session, new_quote_step='awaiting_outros_motoristas')
                return "(Passo 8 de 10) Todos os veículos foram cadastrados! Deseja cadastrar outros motoristas?"
            
        elif session.cliente_substage == "awaiting_outros_motoristas":
            resposta = message.lower()
            if "nao" in resposta or 'não' in resposta or 'n' == resposta:
                self.set_stage(session, new_quote_step="awaiting_seguro_anterior")
                return "(Passo 9 de 10) Ok, sem motoristas extras. Estamos quase acabando! Você possui seguro atualmente ou teve seguro nos últimos 30 dias?"
            elif "sim" in resposta or 's' == resposta:
                self.set_stage(session, new_quote_step='awaiting_qtd_motoristas')
                return "(Passo 8 de 10) Entendido. Quantos motoristas extras você gostaria de adicionar?"
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
                self.set_stage(session, new_quote_step='awaiting_motorista_birthdate')
                return f"(Passo 8 de 10) (Motorista extra 1 de {qtd}) Qual a data de nascimento? (use o formato MM/DD/AAAA)"
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
                self.set_stage(session, new_quote_step='awaiting_motorista_driver')
                return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o número da driver license desse motorista?"
            else:
                return "Data inválida. Por favor, informe a data de nascimento no formato MM/DD/AAAA."

        elif session.cliente_substage == "awaiting_motorista_driver":
            driverlicense = message.strip()
            if not driverlicense:
                return "O número da CNH não pode ficar em branco. Por favor, informe corretamente."
            motorista_lista = session.cliente_motoristas
            motorista_lista[-1]["driver_license"] = driverlicense
            session.cliente_motoristas = motorista_lista
            self.set_stage(session, new_quote_step='awaiting_motorista_state')
            return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o estado da driver license desse motorista?"

        elif session.cliente_substage == "awaiting_motorista_state":
            driverstate = message.strip()
            if not driverstate:
                return "O estado da CNH não pode ficar em branco. Por favor, informe corretamente."
            motorista_lista = session.cliente_motoristas
            motorista_lista[-1]["driver_license_state"] = driverstate
            session.cliente_motoristas = motorista_lista
            self.set_stage(session, new_quote_step='awaiting_motorista_relacao')
            return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a relação desse motorista com o motorista principal? (Ex: filho, esposa, amigo...)"

        elif session.cliente_substage == "awaiting_motorista_relacao":
            relacao = message.strip()
            if not relacao:
                return "A relação não pode ficar em branco. Por favor, informe corretamente (Ex: filho, esposa, amigo...)."
            motorista_lista = session.cliente_motoristas
            motorista_lista[-1]["relation"] = relacao
            session.cliente_motoristas = motorista_lista


            if session.motorista_atual < session.qtd_motoristas:
                session.motorista_atual += 1
                self.set_stage(session, new_quote_step='awaiting_motorista_birthdate')
                return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a data de nascimento? (use o formato MM/DD/AAAA)"
            else:
                self.set_stage(session, new_quote_step='awaiting_seguro_anterior')
                return "(Passo 9 de 10) Todos os motoristas extras foram cadastrados! Agora, você possui seguro atualmente ou teve seguro nos últimos 30 dias?"
        
        #seguro anterior do cliente
        elif session.cliente_substage == "awaiting_seguro_anterior":
            if "nao" in message.lower() or 'não' in message.lower() or 'n' in message.lower() or "0" in message.lower():
                return self.concluir_cotacao(phone_number)
            elif "sim" in message.lower() or 's' in message.lower() or "si" in message.lower():
                self.set_stage(session, new_quote_step='awaiting_tempo_seguro_anterior')
                return "(Passo 10 de 10) Para finalizar, quanto tempo de seguro voce tem/teve?"
            else:
                return "Desculpa, nao entendi a sua resposta! pode dizer sim ou nao?"
        elif session.cliente_substage == "awaiting_tempo_seguro_anterior":
            session.cliente_seguro_anterior = message
            return self.concluir_cotacao(phone_number)
        
    def concluir_cotacao(self, phone_number):
        self.reset_session(phone_number)
        return "Muito obrigado! Você completou a cotação. Todas as suas informações foram recebidas e em breve um de nossos especialistas te enviará os valores aqui mesmo no WhatsApp."
    
    def reset_session(self, phone_number):
        cliente = Cliente.query.filter_by(phone_number=phone_number).first()
        if cliente:
            cliente.cliente_stage = 'initial'
            cliente.cliente_nome = None 
            cliente.cliente_driver = None
            cliente.cliente_driver_state = None
            cliente.cliente_birthdate = None
            cliente.cliente_address = None
            cliente.cliente_veiculos = []
            cliente.cliente_motoristas = []
            cliente.cliente_seguro_anterior = None
            db.session.commit()
            