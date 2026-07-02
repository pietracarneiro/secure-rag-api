from fastapi import FastAPI

from app.modules.auth.router import router as auth_router # Importando as rotas de autenticação

app = FastAPI(title="Secure RAG API")

# Acoplamos as rotas de auth na nossa API principal
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure RAG API! The project has started."}

@app.get("/health")
def health_check():
    return {"status": "ok"}