from models.model import Cliente
import time
from utils.extensions import db
from quotes.auto_quote_flow import AutoQuoteFlow
from quotes.commercial_quote_flow import ComercialQuoteFlow
from quotes.moto_quote_flow import MotoQuoteFlow
from services.trello_service import Trello
from quotes.messages import texts

class ConversationFlow:
    texts = texts
    def __init__(self):
        self.trello_service = Trello()
        self.auto_quote = AutoQuoteFlow()
        self.comercial_quote = ComercialQuoteFlow()
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

        if not message:
            return self.texts['only_text'][lang]

        if message.strip().lower() in ["reiniciar", "restart"]:
            self.reset_session(phone_number)
            return self.texts['restart'][lang]
        
        elif message.strip().lower() in ["suporte", "support", "soporte"]:
            self.handle_support(phone_number, message)
            return self.texts['suporte_certeza'][lang]

        elif message.strip().lower() in ["ajuda", "ayuda", "help"]:
            return self.texts['help'][lang]
        
        elif message.strip().lower() in ['salir', "sair", "exit"]:
            return self.handle_exit(phone_number)

        stage = session.cliente_stage
        if stage == "select_language":
            return self.handle_select_language(phone_number)
        elif stage == "waiting_language":
            return self.handle_option_language(phone_number, message)
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
            return self.texts['erro_reiniciar'][lang]

        
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
            if lang not in ['pt', 'en', 'es']:
                lang = 'pt'
            return self.texts['language_error'][lang]
        self.set_stage(session, new_stage='initial')
        return self.handle_initial(phone_number)

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
            return self.texts['suporte_certeza'][lang]
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
    
    def handle_support(self, phone_number, message):
        session = self.get_user_session(phone_number)

        lang = getattr(session, 'language', 'pt')

        ## garante que a ultima interação foi há menos de 10 minutos
        now = time.time()
        timeout = 600 
        last_interaction = getattr(session, 'last_interaction', now)
        if now - last_interaction > timeout and session.cliente_stage == 'suporte':
            self.set_stage(session, new_stage='initial')
            session.last_interaction = now
            return self.texts['support_timeout'][lang]

        if message.strip().lower() in ["sim", "yes", "si"]:
            self.set_stage(session, new_stage='suporte')
            return self.texts['support'][lang]

        elif message.strip().lower() in ["nao", "no", "não"]:
            return self.texts['support_no'][lang]
        else:
            return self.texts['option_error'][lang]

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
            "tempo_de_seguro": session.cliente_seguro_anterior,
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
        cliente = self.get_user_session(phone_number)
        if cliente:
            cliente.cliente_stage = 'initial'
            cliente.cliente_substage = None
            cliente.tipo_cotacao = None

            cliente.cliente_motoristas = None
            cliente.cliente_seguro_anterior = None

            cliente.empresa_usdot = None
            cliente.empresa_endereco = None

            db.session.commit()

    def handle_exit(self, phone_number):
        session = self.get_user_session(phone_number)
        if session:
            session.cliente_stage = 'select_language'
            session.cliente_substage = None
            session.tipo_cotacao = None

            session.cliente_motoristas = None
            session.cliente_seguro_anterior = None

            session.empresa_usdot = None
            session.empresa_endereco = None

            db.session.commit()
        lang = getattr(session, 'language', 'pt')
        return {
            'pt': "Conversa finalizada. Se precisar, é só mandar uma mensagem novamente!",
            'en': "Conversation ended. If you need anything, just send a message again!",
            'es': "Conversación finalizada. Si necesita algo, solo envíe un mensaje nuevamente!"
        }[lang]
