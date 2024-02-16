from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    pwd = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<UsuarioModel(nome={self.nome}, username={self.username})>"
