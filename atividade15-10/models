from sqlalchemy import Column, Integer, String

from database import Base


class Animais(Base):
    __tablename__ = "animais"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    especie = Column(String)
    raca = Column(String)
    idade = Column(Integer)
    nome_tutor = Column(String)
    veterinario_id = Column(String)
