from dataclasses import dataclass
import datetime
@dataclass

class Caixa360:
    id: int
    data: datetime
    valor: float
    tipo: str
    descricao: str
    saldo: float = 0.0