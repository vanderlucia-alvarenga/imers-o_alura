from sqlalchemy import Column, Integer, String, Boolean, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import time
from sqlalchemy.sql.schema import ForeignKey

from core.configs import settings

class AlbumModel(settings.DBBaseModel):
    __tablename__ = 'album'
    
    id_album: int = Column(Integer, primary_key=True, nullable=False)
    nome: str = Column(String(255), nullable=False)
    id_artista: int = Column(Integer, ForeignKey('artistas.id_artista'),nullable=False)
    ano_lancamento: int = Column(Integer, nullable=False)
    genero: int = Column(Integer, nullable=False)
    musicas = relationship('MusicaModel', backref='album') # One to Many relationship with MusicaModel
    artista = relationship('ArtistaModel', backref='album') # Many to One relationship with ArtistaModel

    def __repr__(self):
        return f"<AlbumModel(nome={self.nome}, id_artista={self.id_artista}, ano_lancamento={self.ano_lancamento})>"

    def __str__(self):
        return f"{self.nome} - {self.ano_lancamento}"