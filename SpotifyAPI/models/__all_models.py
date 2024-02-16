from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP

from core.configs import settings

from models import album_model
from models import musicas_model
from models import usuario_model

class GeneroModel(settings.DBBaseModel):
    __tablename__ = 'genero'
    
    id_genero: int = Column(Integer, primary_key=True, nullable=False)
    genero: str = Column(String(255), nullable=False)
    
    def __repr__(self):
        return f"<GeneroModel(nome={self.genero})>"
    
    def __str__(self):
        return f"{self.genero}"

class PaisModel(settings.DBBaseModel):
    __tablename__ = 'pais'
    
    id_pais: int = Column(Integer, primary_key=True, nullable=False)
    pais: str = Column(String(255), nullable=False)
    
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
    
    def __repr__(self):
        return f"<ExecucoesModel(id_usuario={self.id_usuario}, id_musica={self.id_musica})>"
    
    def __str__(self):
        return f"{self.id_usuario} - {self.id_musica}"