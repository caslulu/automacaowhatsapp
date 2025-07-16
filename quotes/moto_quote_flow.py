
from quotes.base_quote_flow import BaseQuoteFlow

class MotoQuoteFlow(BaseQuoteFlow):
    texts = {
        'birthdate': "(Passo 2 de 10) Obrigado! Agora, qual a sua data de nascimento? (use o formato MM/DD/AAAA)",
        'driverlicense': "(Passo 3 de 10) Obrigado! Agora, qual o número da sua driver license ou cnh?",
        'driver_state': "(Passo 4 de 10) Perfeito! Qual o estado da sua driver license? (Se for internacional, diga internacional)",
        'address': "(Passo 5 de 10) Obrigado! Qual o seu endereço? (Inclua o zipcode, por favor!)",
        'tempo_endereco': "(Passo 6 de 10) Há quanto tempo você mora nesse endereço?",
        'qtd_veiculos': "(Passo 6 de 10) Quantas motos você deseja adicionar?",
        'qtd_veiculos_erro': "Por favor, informe um número válido de motos.",
        'vin_erro': "O VIN deve ter 17 caracteres. Por favor, verifique e envie novamente.",
        'financiad_erro': "Por favor, responda apenas 'financiado' ou 'quitado'.",
        'tempo_erro': "Por favor, informe há quanto tempo você possui a moto.",
        'cadastrar_outros_motoristas': "(Passo 8 de 10) Todas as motos foram cadastradas! Deseja cadastrar outros motoristas?",
        'sem_outros_motoristas': "(Passo 9 de 10) Ok, sem motoristas extras. Estamos quase acabando! Você possui seguro atualmente ou teve seguro nos últimos 30 dias?",
        'quantos_motoristas': "(Passo 8 de 10) Entendido. Quantos motoristas extras você gostaria de adicionar?",
        'qtd_motorista_erro': "Não entendi. Por favor, digite apenas o número de motoristas extras.",
        'qtd_motorista_menor_erro': "Por favor, digite um número válido (1 ou mais).",
        'nome_erro': "O nome não pode ficar em branco.",
        'data_maior_erro': "Data inválida. Por favor, informe uma data de nascimento válida.",
        'birthdate_invalido': "Data inválida. Por favor, informe a data de nascimento no formato MM/DD/AAAA.",
        'motorista_driver_erro': "O número da CNH não pode ficar em branco. Por favor, informe corretamente.",
        'motorista_driver_state_erro': "O estado da CNH não pode ficar em branco. Por favor, informe corretamente.",
        'relacao_vazia_erro': "A relação não pode ficar em branco. Por favor, informe corretamente (Ex: filho, esposa, amigo...).",
        'tem_seguro_anterior': "(Passo 10 de 10) Para finalizar, quanto tempo de seguro você tem/teve?",
        'tem_seguro_anterior_erro': "Desculpa, não entendi a sua resposta! pode dizer sim ou não?"
    }

    def handle(self, phone_number, message, session, set_stage, concluir_cotacao):
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

        elif session.cliente_substage == 'awaiting_veiculos':
            result = self.handle_qtd_veiculos(session, message, set_stage)
            if result is True:
                return f"(Passo 7 de 10) (Moto 1 de {session.qtd_veiculos}) Qual o VIN da moto?"
            return result

        elif session.cliente_substage == 'awaiting_vin':
            result = self.handle_vin(session, message, set_stage)
            if result is True:
                return f"(Passo 7 de 10) (Moto {session.veiculo_atual} de {session.qtd_veiculos}) A moto é financiado ou quitado?"
            return result

        elif session.cliente_substage == 'awaiting_financiado':
            result = self.handle_financiado(session, message, set_stage)
            if result is True:
                return f"(Passo 7 de 10) (Moto {session.veiculo_atual} de {session.qtd_veiculos}) Há quanto tempo você possui essa moto?"
            return result

        elif session.cliente_substage == 'awaiting_tempo':
            result = self.handle_tempo(session, message, set_stage)
            if result is True:
                if session.veiculo_atual <= session.qtd_veiculos:
                    return f"(Passo 7 de 10) (Moto {session.veiculo_atual} de {session.qtd_veiculos}) Qual o VIN da moto?"
                else:
                    return "(Passo 8 de 10) Todas as motos foram cadastradas! Deseja cadastrar outros motoristas?"
            return result

        elif session.cliente_substage == 'awaiting_outros_motoristas':
            result = self.handle_outros_motoristas(session, message, set_stage)
            return result

        elif session.cliente_substage == 'awaiting_qtd_motoristas':
            result = self.handle_qtd_motoristas(session, message, set_stage)
            if result is True:
                return f"(Passo 8 de 10) (Motorista extra 1 de {session.qtd_motoristas}) Qual o nome do motorista?"
            return result

        elif session.cliente_substage == 'awaiting_motorista_nome':
            result = self.handle_nome_motoristas(session, message, set_stage)
            if result is True:
                return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a data de nascimento? (use o formato MM/DD/AAAA)"
            return result

        elif session.cliente_substage == 'awaiting_motorista_birthdate':
            result = self.handle_birthdate_motoristas(session, message, set_stage)
            if result is True:
                return f"(Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o número da driver license desse motorista?"
            return result

        elif session.cliente_substage == 'awaiting_motorista_driver':
            result = self.handle_driver_motoristas(session, message, set_stage)
            if result is True:
                return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual o estado da driver license desse motorista?"
            return result

        elif session.cliente_substage == 'awaiting_motorista_state':
            result = self.handle_driver_motoristas_state(session, message, set_stage)
            if result is True:
                return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a relação desse motorista com o motorista principal? (Ex: filho, esposa, amigo...)"
            return result

        elif session.cliente_substage == 'awaiting_motorista_relacao':
            result = self.handle_motoristas_relacao(session, message, set_stage)
            if result is True:
                if session.motorista_atual <= session.qtd_motoristas:
                    return f"(Passo 8 de 10) (Motorista extra {session.motorista_atual} de {session.qtd_motoristas}) Qual a data de nascimento? (use o formato MM/DD/AAAA)"
                else:
                    return "(Passo 9 de 10) Todos os motoristas extras foram cadastrados! Agora, você possui seguro atualmente ou teve seguro nos últimos 30 dias?"
            return result

        elif session.cliente_substage == 'awaiting_seguro_anterior':
            return self.handle_tem_seguro_anterior(session, message, set_stage, concluir_cotacao, phone_number)

        elif session.cliente_substage == 'awaiting_tempo_seguro_anterior':
            session.cliente_seguro_anterior = message
            return concluir_cotacao(phone_number)

        else:
            return "Desculpe, não entendi sua resposta. Por favor, tente novamente ou digite 'voltar' para retornar ao passo anterior."
