from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

# O que o usuário PRECISA ENVIAR para se registrar
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# O que a API vai RETORNAR para o usuário
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# O que a API devolve quando o login dá certo
class Token(BaseModel):
    access_token: str
    token_type: str

# Os dados que ficam escondidos dentro do crachá (vamos guardar o ID do usuário lá)
class TokenData(BaseModel):
    user_id: UUID | None = None