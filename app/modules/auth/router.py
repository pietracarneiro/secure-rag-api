from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # IMPORTANTE
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token # IMPORTANTE
from app.modules.auth.models import User
from app.modules.auth.schemas import UserCreate, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado no sistema.")
    
    hashed_pwd = get_password_hash(user_in.password)
    new_user = User(email=user_in.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Procura o usuário pelo e-mail (que o FastAPI chama de username no form)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # 2. Se não achar ou se a senha estiver errada, joga erro de credenciais inválidas
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Se passou na portaria, gera o crachá contendo o ID do usuário convertido para string
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # 4. Retorna o token em formato JSON
    return {"access_token": access_token, "token_type": "bearer"}