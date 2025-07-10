from twilio.twiml.messaging_response import MessagingResponse
from utility import parse_data_flexivel
from datetime import datetime
from model import Cliente
from extensions import db





class ConversationFlow:
    def __init__(self):
        self.user_sessions = {}
    
    def get_user_session(self, phone_number):
        if phone_number not in self.user_sessions:
            cliente = Cliente.query.filter_by(phone_number=phone_number).first()
            if cliente:
                self.user_sessions[phone_number] = {
                    'stage': cliente.cliente_stage or 'initial',
                    'data':{
                        "nome_cliente": cliente.cliente_nome,
                        "driverlicense_cliente": cliente.cliente_driver,
                        "driverstate_cliente": cliente.cliente_driver_state,
                        "birthdate_cliente": cliente.cliente_birthdate,
                        "address_cliente": cliente.cliente_address,
                        "veiculos": cliente.cliente_veiculos or [],
                        "motoristas": cliente.cliente_motoristas or [],
                        "tempo_seguro_anterior": cliente.cliente_seguro_anterior,
                    }
                }
            else:
                self.user_sessions[phone_number] =  {
                    "stage": 'initial',
                    'data': {}
                }
        return self.user_sessions[phone_number]
    def set_stage(self, phone_number, new_stage, data=None):
        session = self.get_user_session(phone_number)
        session['stage'] = new_stage
        if data:
            session['data'].update(data)
        cliente = Cliente.query.filter_by(phone_number=phone_number).first()
        if not cliente:
            cliente = Cliente(phone_number=phone_number)
            db.session.add(cliente)
        cliente.cliente_stage = new_stage
        if 'nome_cliente' in session['data']:
            cliente.cliente_nome = session['data']['nome_cliente']
        if 'driverlicense_cliente' in session['data']:
            cliente.cliente_driver = session['data']['driverlicense_cliente']
        if 'driverstate_cliente' in session['data']:
            cliente.cliente_driver_state = session['data']['driverstate_cliente']
        if 'birthdate_cliente' in session['data']:
            cliente.cliente_birthdate = session['data']['birthdate_cliente']
        if 'address_cliente' in session['data']:
            cliente.cliente_address = session['data']['address_cliente']
        if 'veiculos' in session['data']:
            cliente.cliente_veiculos = session['data']['veiculos']
        if 'motoristas' in session['data']:
            cliente.cliente_motoristas = session['data']['motoristas']
        if 'tempo_seguro_anterior' in session['data']:
            cliente.cliente_seguro_anterior = session['data']['tempo_seguro_anterior']
        elif not 'tempo_seguro_anterior' in session['data']:
            cliente.cliente_seguro_anterior = "nao tem"
        db.session.commit()


    
    def process_message(self, phone_number, message):

        if message.strip().lower() in ["reiniciar", "restart"]:
            self.reset_session(phone_number)
            return "Conversa reiniciada, Digite um 'oi' para começar novamente."
        
        session = self.get_user_session(phone_number)
        stage = session['stage']
        
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
        self.set_stage(phone_number, 'waiting_option')
        return "Ola! Como posso ajudar voce? \n 1- Cotação para veiculo\n 2- Suporte\n Para voltar para o inicio, digite reinciar."
    
    def handle_options(self, phone_number, message):
        if "1" in message or "quote" in message or "cotacao" in message:
            self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_name'})
            return "(Passo 1 de 10) Otimo! Para comecar, qual o seu nome?"
        elif "2" in message or "suporte" in message:
            self.set_stage(phone_number, 'suporte')
            return "Entendi, qual problema voce esta tendo? Iremos conectar voce com um agente."
        elif "reiniciar" in message.lower() or "restart" in message.lower():
            self.reset_session(phone_number)
        
    def handle_quote(self, phone_number, message):
        session = self.get_user_session(phone_number)
        step = session['data'].get('quote_step', 'awaiting_name')

        #nome do cliente
        if step == 'awaiting_name':
            session['data']['nome_cliente'] = message
            self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_birthdate'})
            return "(Passo 2 de 10) Obrigado! Agora, qual a sua data de nascimento? (use o formato MM/DD/AAAA)"
        
        #data de nascimento do cliente
        elif step == "awaiting_birthdate":
            data = parse_data_flexivel(message)
            if data is not None:
                data_formatada = datetime.strftime(data, "%m/%d/%Y")
                session['data']['birthdate_cliente'] = data_formatada
                self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_driverlicense'})
                return "(Passo 3 de 10) Obrigado! Agora, qual o numero da sua driver license ou cnh?"
            else:
                return "Ops! parece que voce digitou a data de nascimento errada, tem como voce corrigir?"
            
        #driver do cliente
        elif step == "awaiting_driverlicense":
            session['data']['driverlicense_cliente'] = message
            self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_driverstate'})
            return "(Passo 4 de 10) Perfeito! Poderia me dizer qual o estado da sua driver license? (Se for internacional, diga internacional)"
        
        #numero da driver do cliente
        elif step == "awaiting_driverstate":
            session['data']['driverstate_cliente'] = message
            self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_address'})
            return ("(Passo 5 de 10) Obrigado! Poderia me dizer qual o seu endereço? (Inclua o zipcode, por favor!)")
        
        #endereco do cliente
        elif step == "awaiting_address":
            session['data']['address_cliente'] = message
            self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_veiculos'})
            return ("(Passo 6 de 10) Okay! Poderia me dizer quantos veiculos voce deseja adicionar?")
        #veiculos do cliente
        elif step == "awaiting_veiculos":
            try:
                qtd = int(message)
                if qtd < 1:
                    return "Por favor, informe um número válido de veículos."
                session['data']['qtd_veiculos'] = qtd
                session['data']['veiculos'] = []
                session['data']['veiculo_atual'] = 1
                self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_vin'})
                return f"(Passo 7 de 10) (Veículo 1 de {qtd}) Qual o VIN do veículo?"
            except ValueError:
                return "Por favor, informe um número válido de veículos."

        elif step == "awaiting_vin":
            vin = message.strip()
            if len(vin) != 17:
                return "O VIN deve ter 17 caracteres. Por favor, verifique e envie novamente."
            veiculo = {'vin': vin}
            session['data']['veiculo_em_edicao'] = veiculo
            self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_financiado'})
            atual = session['data']['veiculo_atual']
            total = session['data']['qtd_veiculos']
            return f"(Passo 7 de 10) (Veículo {atual} de {total}) O veículo é financiado ou quitado?"

        elif step == "awaiting_financiado":
            veiculo = session['data']['veiculo_em_edicao']
            financiado = message.strip().lower()
            if not financiado or financiado not in ["financiado", "quitado"]:
                return "Por favor, responda apenas 'financiado' ou 'quitado'."
            veiculo['financiado'] = financiado
            self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_tempo'})
            atual = session['data']['veiculo_atual']
            total = session['data']['qtd_veiculos']
            return f"(Passo 7 de 10) (Veículo {atual} de {total}) Há quanto tempo você possui esse veículo?"

        elif step == "awaiting_tempo":
            veiculo = session['data']['veiculo_em_edicao']
            tempo = message.strip()
            if not tempo:
                return "Por favor, informe há quanto tempo você possui o veículo."
            veiculo['tempo'] = tempo
            session['data']['veiculos'].append(veiculo)
            atual = session['data']['veiculo_atual']
            total = session['data']['qtd_veiculos']
            if atual < total:
                session['data']['veiculo_atual'] += 1
                self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_vin'})
                return f"(Passo 7 de 10) (Veículo {atual+1} de {total}) Qual o VIN do veículo?"
            else:
                self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_outros_motoristas'})
                session['data'].pop('veiculo_em_edicao', None)
                session['data'].pop('veiculo_atual', None)
                return "(Passo 8 de 10) Todos os veículos foram cadastrados! Deseja cadastrar outros motoristas? ."
        elif step == "awaiting_outros_motoristas":
            resposta = message.lower()
            if "nao" in resposta or 'não' in resposta or 'n' == resposta:
                self.set_stage(phone_number, 'auto_quote', {'quote_step': "awaiting_seguro_anterior"})
                return "(Passo 9 de 10) Ok, sem motoristas extras. Estamos quase acabando! Você possui seguro atualmente ou teve seguro nos últimos 30 dias?"
            elif "sim" in resposta or 's' == resposta:
                self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_qtd_motoristas'})
                return "(Passo 8 de 10) Entendido. Quantos motoristas extras você gostaria de adicionar?"
            else:
                return "Não entendi sua resposta. Por favor, responda com 'sim' ou 'não'."
            
        #outros motoristas
        elif step == "awaiting_qtd_motoristas":
            try:
                qtd = int(message)
                if qtd < 1:
                    return "Por favor, digite um número válido (1 ou mais)."
                session['data']['qtd_motoristas'] = qtd
                session['data']['motoristas'] = []
                session['data']['motorista_atual'] = 1
                self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_motorista_birthdate'})
                return f"(Passo 8 de 10) (Motorista extra 1 de {qtd}) Qual a data de nascimento? (use o formato MM/DD/AAAA)"
            except ValueError:
                return "Não entendi. Por favor, digite apenas o número de motoristas extras."

        elif step == "awaiting_motorista_birthdate":
            motorista = {}
            data = parse_data_flexivel(message)
            if data is not None:
                if data > datetime.now():
                    return "Data inválida. Por favor, informe uma data de nascimento válida."
                data_formatada = datetime.strftime(data, "%m/%d/%Y")
                motorista['birthdate'] = data_formatada
                session['data']['motorista_em_edicao'] = motorista
                self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_motorista_driver'})
                atual = session['data']['motorista_atual']
                total = session['data']['qtd_motoristas']
                return f"(Passo 8 de 10) (Motorista extra {atual} de {total}) Qual o número da driver license desse motorista?"
            else:
                return "Data inválida. Por favor, informe a data de nascimento no formato MM/DD/AAAA."

        elif step == "awaiting_motorista_driver":
            motorista = session['data']['motorista_em_edicao']
            driverlicense = message.strip()
            if not driverlicense:
                return "O número da CNH não pode ficar em branco. Por favor, informe corretamente."
            motorista['driverlicense'] = driverlicense
            self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_motorista_state'})
            atual = session['data']['motorista_atual']
            total = session['data']['qtd_motoristas']
            return f"(Passo 8 de 10) (Motorista extra {atual} de {total}) Qual o estado da driver license desse motorista?"

        elif step == "awaiting_motorista_state":
            motorista = session['data']['motorista_em_edicao']
            driverstate = message.strip()
            if not driverstate:
                return "O estado da CNH não pode ficar em branco. Por favor, informe corretamente."
            motorista['driverstate'] = driverstate
            self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_motorista_relacao'})
            atual = session['data']['motorista_atual']
            total = session['data']['qtd_motoristas']
            return f"(Passo 8 de 10) (Motorista extra {atual} de {total}) Qual a relação desse motorista com o motorista principal? (Ex: filho, esposa, amigo...)"

        elif step == "awaiting_motorista_relacao":
            motorista = session['data']['motorista_em_edicao']
            relacao = message.strip()
            if not relacao:
                return "A relação não pode ficar em branco. Por favor, informe corretamente (Ex: filho, esposa, amigo...)."
            motorista['relacao'] = relacao
            session['data']['motoristas'].append(motorista)
            atual = session['data']['motorista_atual']
            total = session['data']['qtd_motoristas']
            if atual < total:
                session['data']['motorista_atual'] += 1
                self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_motorista_birthdate'})
                return f"(Passo 8 de 10) (Motorista extra {atual+1} de {total}) Qual a data de nascimento? (use o formato MM/DD/AAAA)"
            else:
                self.set_stage(phone_number, 'auto_quote', {'quote_step': 'awaiting_seguro_anterior'})
                session['data'].pop('motorista_em_edicao', None)
                session['data'].pop('motorista_atual', None)
                return "(Passo 9 de 10) Todos os motoristas extras foram cadastrados! Agora, você possui seguro atualmente ou teve seguro nos últimos 30 dias?"
        #seguro anterior do cliente
        elif step == "awaiting_seguro_anterior":
            if "nao" in message.lower() or 'não' in message.lower() or 'n' in message.lower() or "0" in message.lower():
                return self.concluir_cotacao(phone_number)
            elif "sim" in message.lower() or 's' in message.lower() or "si" in message.lower():
                self.set_stage(phone_number, 'auto_quotes', {'quote_step': 'awaiting_tempo_seguro_anterior'})
                return "(Passo 10 de 10) Para finalizar, quanto tempo de seguro voce tem/teve?"
            else:
                return "Desculpa, nao entendi a sua resposta! pode dizer sim ou nao?"
        elif step == "awaiting_tempo_seguro_anterior":
            session['data']['tempo_seguro_anterior'] = message
            return self.concluir_cotacao(phone_number)
        
    def concluir_cotacao(self, phone_number):
        self.reset_session(phone_number)
        return "Muito obrigado! Você completou a cotação. Todas as suas informações foram recebidas e em breve um de nossos especialistas te enviará os valores aqui mesmo no WhatsApp."
    
    def reset_session(self, phone_number):
        if phone_number in self.user_sessions:
            del self.user_sessions[phone_number]
        
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
            