#************************************************
# Cria as tabelas no Banco de Dados             *
#************************************************
from datetime import datetime

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class Store(Base, TimeStampMixin):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # "users.id" => nome da tabela . campo da tabela que se deseja fazer o vinculo
    owner: Mapped["User"] = relationship() # busca os dados do usuário para devolver para a requisição - Aula 4 ~ 1 hora


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()