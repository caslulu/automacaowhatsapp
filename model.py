from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from extensions import db


class Cliente(db.Model):
    phone_number: Mapped[str] = mapped_column(primary_key=True, unique=True)
    cliente_stage: Mapped[str] = mapped_column(nullable=True)
    cliente_nome: Mapped[str] = mapped_column(nullable=True)
    cliente_driver: Mapped[str] = mapped_column(nullable=True)
    cliente_driver_state: Mapped[str] = mapped_column(nullable=True)
    cliente_birthdate: Mapped[str] = mapped_column(nullable=True)
    cliente_address: Mapped[str] = mapped_column(nullable=True)
    cliente_veiculos: Mapped[list] = mapped_column(JSON, nullable=True, default=list)
    cliente_motoristas: Mapped[list] = mapped_column(JSON, nullable=True, default=list)
    cliente_seguro_anterior: Mapped[str] = mapped_column(nullable=True)
    cliente_substage: Mapped[str] = mapped_column(nullable=True)
    qtd_veiculos: Mapped[int] = mapped_column(Integer, nullable=True)
    veiculo_atual: Mapped[int] = mapped_column(Integer, nullable=True)

    qtd_motoristas: Mapped[int] = mapped_column(Integer, nullable=True)
    motorista_atual: Mapped[int] = mapped_column(Integer, nullable=True)


    
