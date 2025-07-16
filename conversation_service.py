from model import Cliente
from extensions import db
from quotes.auto_quote_flow import AutoQuoteFlow
from quotes.commercial_quote_flow import ComercialQuoteFlow
from quotes.moto_quote_flow import MotoQuoteFlow
from trello_service import Trello


class ConversationFlow:
    texts = {
        'select_language': {
            'pt': "Se deseja conversar em português, selecione 1\nIf you would like to speak in English, press 2\nSi desea hablar en español, presione 3.",
            'en': "If you would like to speak in English, press 2\nSe deseja conversar em português, selecione 1\nSi desea hablar en español, presione 3.",
            'es': "Si desea hablar en español, presione 3.\nSe deseja conversar em português, selecione 1\nIf you would like to speak in English, press 2."
        },
        'initial': {
            'pt': "Olá! Como posso ajudar você?\n1- Cotação para veículo\n2- Suporte\nPara voltar para o início, digite reiniciar.",
            'en': "Hello! How can I help you?\n1- Vehicle quote\n2- Support\nTo return to the start, type restart.",
            'es': "¡Hola! ¿Cómo puedo ayudarte?\n1- Cotización para vehículo\n2- Soporte\nPara volver al inicio, escriba reiniciar."
        },
        'option_error': {
            'pt': "Não entendi sua opção. Por favor, escolha uma das opções acima ou digite 'reiniciar'.",
            'en': "I didn't understand your option. Please choose one of the options above or type 'restart'.",
            'es': "No entendí su opción. Por favor, elija una de las opciones arriba o escriba 'reiniciar'."
        },
        'type_quote': {
            'pt': "Escolha o tipo de cotação que você deseja:\n1-Carro\n2-Comercial\n3-Moto",
            'en': "Choose the type of quote you want:\n1-Car\n2-Commercial\n3-Motorcycle",
            'es': "Elija el tipo de cotización que desea:\n1-Auto\n2-Comercial\n3-Moto"
        },
        'type_quote_error': {
            'pt': "Desculpa, não entendi o tipo. Pode digitar um número válido?",
            'en': "Sorry, I didn't understand the type. Can you enter a valid number?",
            'es': "Disculpa, no entendí el tipo. ¿Puede ingresar un número válido?"
        },
        'restart': {
            'pt': "Conversa reiniciada, digite um 'oi' para começar novamente.",
            'en': "Conversation restarted, type 'hi' to start again.",
            'es': "Conversación reiniciada, escriba 'hola' para comenzar de nuevo."
        },
        'support': {
            'pt': "Entendi, qual problema você está tendo? Iremos conectar você com um agente.",
            'en': "I understand, what problem are you having? We will connect you with an agent.",
            'es': "Entiendo, ¿qué problema está teniendo? Lo conectaremos con un agente."
        },
        'language_error': {
            'pt': "Desculpa, não entendi. Você precisa selecionar uma das línguas disponíveis.",
            'en': "Sorry, I didn't understand. You need to select one of the available languages.",
            'es': "Disculpa, no entendí. Necesita seleccionar uno de los idiomas disponibles."
        },
        'quote_start': {
            'auto': {
                'pt': "(Passo 1 de 10) Perfeito! Para começar, qual o seu nome?",
                'en': "(Step 1 of 10) Perfect! To start, what is your name?",
                'es': "(Paso 1 de 10) ¡Perfecto! Para comenzar, ¿cuál es su nombre?"
            },
            'comercial': {
                'pt': "Perfeito! Para começar a sua cotação comercial, qual o seu nome?",
                'en': "Perfect! To start your commercial quote, what is your name?",
                'es': "¡Perfecto! Para comenzar su cotización comercial, ¿cuál es su nombre?"
            },
            'moto': {
                'pt': "Ótimo! Para começar a sua cotação de moto, qual o seu nome?",
                'en': "Great! To start your motorcycle quote, what is your name?",
                'es': "¡Genial! Para comenzar su cotización de moto, ¿cuál es su nombre?"
            }
        },
        'quote_complete': {
            'pt': "Muito obrigado! Você completou a cotação. Todas as suas informações foram recebidas e em breve um de nossos especialistas te enviará os valores aqui mesmo no WhatsApp.",
            'en': "Thank you very much! You have completed the quote. All your information has been received and soon one of our specialists will send you the prices right here on WhatsApp.",
            'es': "¡Muchas gracias! Ha completado la cotización. Toda su información ha sido recibida y pronto uno de nuestros especialistas le enviará los valores aquí mismo por WhatsApp."
        },
        'trello_error': {
            'pt': "Erro para localizar o cliente para enviar ao Trello. Um especialista irá te ajudar!",
            'en': "Error locating the client to send to Trello. A specialist will help you!",
            'es': "Error al localizar al cliente para enviar a Trello. ¡Un especialista le ayudará!"
        }
    }
    def __init__(self):
        self.trello_service = Trello()
        self.auto_quote = AutoQuoteFlow()
        self.comemercial_quote = ComercialQuoteFlow()
        self.moto_quote = MotoQuoteFlow()    
    def get_user_session(self, phone_number):
        cliente = Cliente.query.filter_by(phone_number=phone_number).first()
        
        if not cliente:
            cliente = Cliente(phone_number=phone_number, cliente_stage='select_language')
            db.session.add(cliente)
            db.session.commit()
        return cliente

    def set_stage(self, cliente, new_stage=None, new_quote_step=None):
        if new_stage:
            cliente.cliente_stage = new_stage
        
        if new_quote_step:
            cliente.cliente_substage = new_quote_step
        db.session.commit()


    
    def process_message(self, phone_number, message):
        session = self.get_user_session(phone_number)
        lang = getattr(session, 'language', 'pt')

        if message.strip().lower() in ["reiniciar", "restart"]:
            self.reset_session(phone_number)
            return self.texts['restart'][lang]

        stage = session.cliente_stage
        if stage == "select_language":
            return self.handle_select_language(phone_number)
        elif stage == 'initial':
            return self.handle_initial(phone_number)
        elif stage == 'waiting_option':
            return self.handle_options(phone_number, message)
        elif stage == 'waiting_type':
            return self.handle_type_quote(phone_number, message)
        elif stage == 'quote':
            return self.handle_quote(phone_number, message)
        elif stage == 'suporte':
            return self.handle_support(phone_number, message)
        else:
            return self.texts['restart'][lang]

    def handle_select_language(self, phone_number):
        session = self.get_user_session(phone_number)
        self.set_stage(session, new_stage='waiting_language')
        return (
            f"{self.texts['select_language']['pt']}\n\n"
            f"{self.texts['select_language']['en']}\n\n"
            f"{self.texts['select_language']['es']}"
        )

    def handle_option_language(self, phone_number, message):
        session = self.get_user_session(phone_number)
        if "1" in message.strip().lower() or "portugues" in message.strip().lower():
            session.language = "pt"
        elif "2" in message.strip().lower() or "english" in message.strip().lower():
            session.language = "en"
        elif "3" in message.strip().lower() or "espanhol" in message.strip().lower() or "español" in message.strip().lower():
            session.language = "es"
        else:
            lang = getattr(session, 'language', 'pt')
            return self.texts['language_error'][lang]
        self.set_stage(session, new_stage='initial')

    def handle_initial(self, phone_number):
        session = self.get_user_session(phone_number)
        self.set_stage(session, new_stage='waiting_option')
        lang = getattr(session, 'language', 'pt')
        return self.texts['initial'][lang]
    
    def handle_options(self, phone_number, message):
        session = self.get_user_session(phone_number)
        lang = getattr(session, 'language', 'pt')
        if "1" in message or "quote" in message or "cotacao" in message:
            self.set_stage(session, new_stage='waiting_type')
            return self.texts['type_quote'][lang]
        elif "2" in message or "suporte" in message:
            self.set_stage(session, new_stage='suporte')
            return self.texts['support'][lang]
        elif "reiniciar" in message.lower() or "restart" in message.lower():
            self.reset_session(phone_number)  
            return self.texts['restart'][lang]
        return self.texts['option_error'][lang]
        
    def handle_type_quote(self, phone_number, message):
        session = self.get_user_session(phone_number)
        lang = getattr(session, 'language', 'pt')
        msg = message.strip().lower()
        if "auto" in msg or "carro" in msg or "1" in msg:
            session.tipo_cotacao = 'auto'
            self.set_stage(session, new_stage="quote", new_quote_step='awaiting_name')
            return self.texts['quote_start']['auto'][lang]
        elif "comercial" in msg or "2" in msg:
            session.tipo_cotacao = 'comercial'
            self.set_stage(session, new_stage="quote", new_quote_step="awaiting_name")
            return self.texts['quote_start']['comercial'][lang]
        elif "moto" in msg or "motoclicleta" in msg or "3" in msg:
            session.tipo_cotacao = 'moto'
            self.set_stage(session, new_stage="quote", new_quote_step='awaiting_name')
            return self.texts['quote_start']['moto'][lang]
        return self.texts['type_quote_error'][lang]
        
    def handle_quote(self, phone_number, message):
        session = self.get_user_session(phone_number)
        if session.tipo_cotacao == "auto":
            return self.auto_quote.handle(phone_number, message, session, self.set_stage, self.concluir_cotacao)
        elif session.tipo_cotacao == 'comercial':
            return self.comercial_quote.handle(phone_number, message, session, self.set_stage, self.concluir_cotacao)
        elif session.tipo_cotacao == "moto":
            return self.moto_quote.handle(phone_number, message, session, self.set_stage, self.concluir_cotacao)

        
    def concluir_cotacao(self, phone_number):
        session = self.get_user_session(phone_number)
        if not session:
            lang = 'pt'
            return self.texts['trello_error'][lang]
        
        dados = {
            "nome": session.cliente_nome,
            "documento": f"{session.cliente_driver} - {session.cliente_driver_state}",
            "endereco": session.cliente_address,
            "data_nascimento": session.cliente_birthdate,
            "tempo_seguro": session.cliente_seguro_anterior,
            "tempo_no_endereco": session.cliente_tempo_endereco,
            "veiculos": session.cliente_veiculos,
            "pessoas": session.cliente_motoristas,
            "email": self.trello_service.gerar_email(session.cliente_nome),
            "tipo_cotacao": session.tipo_cotacao,
            #se a cotação for comercial:
            "empresa_nome": getattr(session, "empresa_nome", ""),
            "empresa_usdot": getattr(session, "empresa_usdot", ""),
            "empresa_numero_registro": getattr(session, "empresa_numero_registro", ""),
            "empresa_estrutura": getattr(session, "empresa_estrutura", ""),
            "empresa_ramo": getattr(session, "empresa_ramo", ""),
            "empresa_tipo_carga": getattr(session, "empresa_tipo_carga", ""),
            "empresa_endereco": getattr(session, "empresa_endereco", ""),
            "empresa_milhas_trabalho": getattr(session, "empresa_milhas_trabalho", ""),
            "empresa_milhas_ano": getattr(session, "empresa_milhas_ano", "")
        }
        self.trello_service.criar_carta(**dados)
        self.reset_session(phone_number)
        lang = getattr(session, 'language', 'pt')
        return self.texts['quote_complete'][lang]
    
    def reset_session(self, phone_number):
        cliente = Cliente.query.filter_by(phone_number=phone_number).first()
        if cliente:
            cliente.cliente_stage = 'initial'
            cliente.cliente_substage = None
            cliente.tipo_cotacao = None
            db.session.commit()
