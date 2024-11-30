from pydantic import BaseModel
from typing import List, Union

class ResponseModelVaga(BaseModel):
    id_vaga: int
    data_anuncio: str
    titulo_vaga: str
    titulo_resumo: str
    faixa_salarial: str
    empresa_contratante: str
    estado:str
    cidade: str 
    url: str
    descricao: str
    beneficios: str
    regimeContrato: str
    regiao: str
    perfil_vaga: str
    nivel_cargo: str
    salario: int

class ApiLlmSearchInput(BaseModel):
    text: str

class ApiLlmSearchOutput(BaseModel):
    success: List[int] = None  # Para o caso de sucesso
    error: str = None          # Para o caso de erro