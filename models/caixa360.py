from dataclasses import dataclass
import datetime
@dataclass

class Caixa360:
    id: int
    data: datetime
    valor: float
    tipo: str
    categoria: str
    saldo: float