from sqlalchemy import Column, Integer, String, Boolean, Time
from sqlalchemy.orm import relationship
from core.configs import settings
from sqlalchemy.sql.schema import ForeignKey

class MusicaModel(settings.DBBaseModel):
    __tablename__ = 'musicas'
    
    id_musica: int = Column(Integer, primary_key=True, nullable=False)
    id_artista: int = Column(Integer, ForeignKey('artistas.id_artista'),nullable=False)
    nome: str = Column(String(255), nullable=False)
    id_album: int = Column(Integer, ForeignKey('album.id_album'),nullable=False)
    duracao: Time = Column(Time, nullable=False)
    def __repr__(self):
        return f"<MusicaModel(nome={self.nome}, id_artista={self.id_artista}, id_album={self.id_album}, duracao={self.duracao})>"
    
    def __str__(self):
        return f"{self.nome} - {self.duracao}"