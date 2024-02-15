from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import time
from sqlalchemy.sql.sqltypes import TIMESTAMP

from core.configs import settings

import album_model
import musicas_model
import usuario_model

class GeneroModel(settings.DBBaseModel):
    __tablename__ = 'generos'
    
    id_genero: int = Column(Integer, primary_key=True, nullable=False)
    nome: str = Column(String(255), nullable=False)
    
    def __repr__(self):
        return f"<GeneroModel(nome={self.nome})>"
    
    def __str__(self):
        return f"{self.nome}"

class PaisModel(settings.DBBaseModel):
    __tablename__ = 'paises'
    
    id_pais: int = Column(Integer, primary_key=True, nullable=False)
    nome: str = Column(String(255), nullable=False)
    
    def __repr__(self):
        return f"<PaisModel(nome={self.nome})>"
    
    def __str__(self):
        return f"{self.nome}"
    
class ArtistaModel(settings.DBBaseModel):
    __tablename__ = 'artistas'
    
    id_artista: int = Column(Integer, primary_key=True, nullable=False)
    nome: str = Column(String(255), nullable=False)
    id_pais: int = Column(Integer, ForeignKey('paises.id_pais'),nullable=False)
    id_genero: int = Column(Integer, ForeignKey('generos.id_genero'),nullable=False)
    
    pais = relationship('PaisModel', backref='artistas') # Many to One relationship with PaisModel
    genero = relationship('GeneroModel', backref='artistas') # Many to One relationship with GeneroModel
    album = relationship('AlbumModel', backref='artistas') # One to Many relationship with AlbumModel
    musicas = relationship('MusicaModel', backref='artistas') # One to Many relationship with MusicaModel
    
    def __repr__(self):
        return f"<ArtistaModel(nome={self.nome}, id_pais={self.id_pais}, id_genero={self.id_genero})>"
    
    def __str__(self):
        return f"{self.nome}"

class ExecucoesModel(settings.DBBaseModel):
    __tablename__ = 'execucoes'
    
    id_exec: int = Column(Integer, primary_key=True, nullable=False)
    id_usuario: int = Column(Integer, ForeignKey('usuarios.id_usuario'),nullable=False)
    id_musica: int = Column(Integer, ForeignKey('musicas.id_musicas'),nullable=False)
    id_artista: int = Column(Integer, ForeignKey('artistas.id_artista'),nullable=False)
    hora_exec: TIMESTAMP = Column(TIMESTAMP, nullable=False)
    
    usuario = relationship('UsuarioModel', backref='execucoes') # Many to One relationship with UsuarioModel
    musica = relationship('MusicaModel', backref='execucoes') # Many to One relationship with MusicaModel
    
    def __repr__(self):
        return f"<ExecucoesModel(id_usuario={self.id_usuario}, id_musica={self.id_musica})>"
    
    def __str__(self):
        return f"{self.id_usuario} - {self.id_musica}"