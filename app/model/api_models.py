from pydantic import BaseModel
from typing import List, Optional

class SchemaDFVagas(BaseModel):
    id_vaga: str
    data_anuncio: str
    titulo_vaga: str
    titulo_resumo: str
    faixa_salarial: Optional[str]
    empresa_contratante: str
    estado:Optional[str]
    cidade: Optional[str] 
    url: str
    descricao: str
    beneficios: Optional[str]
    regimeContrato: Optional[str]
    regiao: Optional[str]
    perfil_vaga: str
    nivel_cargo: str
    salario: int

class SchemaDFRequisito(BaseModel):
    id_vaga: str
    tool: str
class ApiLlmSearchInput(BaseModel):
    text: str

class ApiLlmSearchOutput(BaseModel):
    success: List[SchemaDFVagas] = None  