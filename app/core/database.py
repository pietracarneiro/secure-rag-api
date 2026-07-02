from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Endereço de conexão: postgres://usuario:senha@localhost:porta/nome_do_banco
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/secureragdb"

# O engine é o motor que gerencia a conexão física com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cada objeto SessionLocal será uma conversa aberta com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Essa classe Base será herdada por todas as tabelas que criarmos no futuro
Base = declarative_base()

# Função auxiliar para abrir e fechar a conexão com o banco automaticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()