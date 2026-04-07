from dataclasses import dataclass


@dataclass
class Usuario:
    id: int
    usuario: str
    senha: str
    trocar_senha: int