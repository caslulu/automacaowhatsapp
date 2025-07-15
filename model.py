from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from extensions import db


class Cliente(db.Model):
    phone_number: Mapped[str] = mapped_column(primary_key=True, unique=True)
    cliente_stage: Mapped[str] = mapped_column(nullable=True)
    cliente_substage: Mapped[str] = mapped_column(nullable=True)
    tipo_cotacao: Mapped[str] = mapped_column(nullable=True)

    ##### COTACAO PARA VEICULOS
    cliente_nome: Mapped[str] = mapped_column(nullable=True)
    cliente_driver: Mapped[str] = mapped_column(nullable=True)
    cliente_driver_state: Mapped[str] = mapped_column(nullable=True)
    cliente_birthdate: Mapped[str] = mapped_column(nullable=True)
    cliente_address: Mapped[str] = mapped_column(nullable=True)
    cliente_tempo_endereco: Mapped[str] = mapped_column(nullable=True)
    cliente_veiculos: Mapped[list] = mapped_column(JSON, nullable=True, default=list)
    cliente_motoristas: Mapped[list] = mapped_column(JSON, nullable=True, default=list)
    cliente_seguro_anterior: Mapped[str] = mapped_column(nullable=True)

    qtd_veiculos: Mapped[int] = mapped_column(Integer, nullable=True)
    veiculo_atual: Mapped[int] = mapped_column(Integer, nullable=True)

    qtd_motoristas: Mapped[int] = mapped_column(Integer, nullable=True)
    motorista_atual: Mapped[int] = mapped_column(Integer, nullable=True)


    ##### CAMPOS EXTRAS PARA COTAÇÃO COMERCIAL
    empresa_nome: Mapped[str] = mapped_column(nullable=True)
    empresa_usdot: Mapped[str] = mapped_column(nullable=True)
    empresa_numero_registro: Mapped[str] = mapped_column(nullable=True)
    empresa_estrutura: Mapped[str] = mapped_column(nullable=True)
    empresa_ramo: Mapped[str] = mapped_column(nullable=True)
    empresa_tipo_carga: Mapped[str] = mapped_column(nullable=True)
    empresa_qtd_funcionarios: Mapped[str] = mapped_column(nullable=True)
    empresa_endereco: Mapped[str] = mapped_column(nullable=True)
    empresa_milhas_trabalho: Mapped[str] = mapped_column(nullable=True)
    empresa_milhas_ano: Mapped[str] = mapped_column(nullable=True)





