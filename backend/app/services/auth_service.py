from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import settings
from app.models.cliente import Cliente
from app.repositories.cliente_repository import ClienteRepository


class AuthService:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def register(self, nome: str, email: str, senha: str) -> Cliente:
        if self.cliente_repository.get_by_email(email):
            raise ValueError("Email já cadastrado")

        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
        cliente = Cliente(nome=nome, email=email, senha_hash=senha_hash)
        return self.cliente_repository.create(cliente)

    def login(self, email: str, senha: str) -> str:
        cliente = self.cliente_repository.get_by_email(email)
        if not cliente or not bcrypt.checkpw(senha.encode(), cliente.senha_hash.encode()):
            raise ValueError("Credenciais inválidas")

        return self._gerar_token(str(cliente.id))

    def _gerar_token(self, cliente_id: str) -> str:
        expira = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        payload = {"sub": cliente_id, "exp": expira}
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> str:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload["sub"]
