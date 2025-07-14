from model import Cliente
from extensions import db
from quotes.auto_quote_flow import AutoQuoteFlow
from quotes.commercial_quote_flow import ComercialQuoteFlow
from quotes.moto_quote_flow import MotoQuoteFlow
from trello_service import Trello



class ConversationFlow:
    def __init__(self):
        self.trello_service = Trello()
        self.auto_quote = AutoQuoteFlow()
        self.comemercial_quote = ComercialQuoteFlow()
        self.moto_quote = MotoQuoteFlow()    
    def get_user_session(self, phone_number):
        cliente = Cliente.query.filter_by(phone_number=phone_number).first()
        
        if not cliente:
            cliente = Cliente(phone_number=phone_number, cliente_stage='initial')
            db.session.add(cliente)
            db.session.commit()
            cliente._imagens_memoria = []
        return cliente

    def set_stage(self, cliente, new_stage=None, new_quote_step=None):
        if new_stage:
            cliente.cliente_stage = new_stage
        
        if new_quote_step:
            cliente.cliente_substage = new_quote_step
        db.session.commit()


    
    def process_message(self, phone_number, message, image_file=None):

        if message.strip().lower() in ["reiniciar", "restart"]:
            self.reset_session(phone_number)
            return "Conversa reiniciada, Digite um 'oi' para começar novamente."
        
        session = self.get_user_session(phone_number)
        stage = session.cliente_stage
        
        if image_file and stage != "quote":
            return "Desculpa, nao entendi. Eu entendo apenas mensagens de texto."

        elif image_file and stage == "quote":
            if not hasattr(session, "_imagens_memoria"):
                session._imagens_memoria = []
            session._imagens_memoria.append(image_file)
            return "Obrigado! Recebi a sua imagem. Agora, responda a pergunta anterior."
        if stage == 'initial':
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
            return "Digite reiniciar para começar novamente"

    def handle_initial(self, phone_number):
        session = self.get_user_session(phone_number)
        self.set_stage(session, new_stage='waiting_option')

        return "Ola! Como posso ajudar voce?\n 1- Cotação para veiculo\n 2- Suporte\n Para voltar para o inicio, digite reinciar."
    
    def handle_options(self, phone_number, message):
        session = self.get_user_session(phone_number)
        if "1" in message or "quote" in message or "cotacao" in message:
            self.set_stage(session, new_stage='waiting_type')
            return "Escolha o tipo de cotação que você deseja: 1-Carro\n 2-Comercial\n 3-Moto"
        
        elif "2" in message or "suporte" in message:
            self.set_stage(session, new_stage='suporte')
            return "Entendi, qual problema voce esta tendo? Iremos conectar voce com um agente."
        
        elif "reiniciar" in message.lower() or "restart" in message.lower():
            self.reset_session(phone_number)  
            return "Digite reiniciar para começar novamente"
        return "Não entendi sua opção. Por favor, escolha uma das opções acima ou digite 'reiniciar'."
        
    def handle_type_quote(self, phone_number, message):
        session = self.get_user_session(phone_number)
        if "auto" in message.strip().lower() or "carro" in message.strip().lower() or "1" in message.strip().lower():
            session.tipo_cotacao = 'auto'
            self.set_stage(session, new_stage="quote", new_quote_step='awaiting_name')
            return "(Passo 1 de 10) Perfeito! Para começar, qual o seu nome?"
        elif "comercial" in message.strip().lower() or "2" in message.strip().lower():
            session.tipo_cotacao = 'comercial'
            self.set_stage(session, new_stage="quote", new_quote_step="awaiting_name")
            return "Perfeito! Para começar a sua cotação comercial, qual o seu nome?"
        elif "moto" in message.strip().lower() or "motoclicleta" in message.strip().lower() or "3" in message.lower().strip():
            session.tipo_cotacao = 'moto'
            self.set_stage(session, new_stage="quote", new_quote_step='awaiting_name')
            return "Otimo! Para começar a sua cotação de moto, qual o seu nome?"
        return "Desculpa, nao entendi o tipo. Pode digitar um numero valido?"
        
    def handle_quote(self, phone_number, message):
        session = self.get_user_session(phone_number)
        if session.tipo_cotacao == "auto":
            return self.auto_quote.handle(phone_number, message, session, self.set_stage, self.concluir_cotacao)
        elif session.tipo_cotacao == 'comercial':
            return self.comercial_quote.handle(phone_number, message, session, self.set_stage, self.concluir_cotacao)
        elif session.tipo_cotacao == "moto":
            return self.moto_quote.handle(phone_number, message, session, self.set_stage, self.concluir_cotacao)

        
    def concluir_cotacao(self, phone_number, imagens_files=None):
        session = self.get_user_session(phone_number)
        if not session:
            return "Erro para localizar o cliente para enviar ao Trello. Um especialista ira te ajudar!"
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
            #campos para comercial
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
        imagens_files = getattr(session, "_imagens_memoria", [])
        self.trello_service.criar_carta_e_anexar_imagem(dados, imagens_files)
        self.reset_session(phone_number)
        return "Muito obrigado! Você completou a cotação. Todas as suas informações foram recebidas e em breve um de nossos especialistas te enviará os valores aqui mesmo no WhatsApp."
    
    def reset_session(self, phone_number):
        cliente = Cliente.query.filter_by(phone_number=phone_number).first()
        if cliente:
            cliente.cliente_stage = 'initial'
            db.session.commit()
        if hasattr(cliente, "_imagens_memoria"):
            del cliente._imagens_memoria
            