from dataclasses import dataclass
from datetime import date
from datetime import time

@dataclass

class Caixa360:
    id: int
    data: date
    hora: time
    valor: float
    tipo: str
    descricao: str