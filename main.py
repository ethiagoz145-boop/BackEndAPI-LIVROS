#API basica de livros 
#====================================================================================================================================================================================================================================================
#Metodos HTTP: GET, POST, PUT, DELETE. 

#(CRUD)
#Create
#Read
#Update
#Delete

#POST = adicionar novos  livros = Create
#GET = Buscar os dados do livro = Read
#PUT = Atualizar os dados de um livro existente = Update
#DELETE = Remover um livro = Delete
#====================================================================================================================================================================================================================================================

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
import secrets
import os

app = FastAPI(
    title="API de Livros",
    description="Uma API simples para gerenciar livros.",
    version="1.0.0",
    contact={
        "name": "Thiago Nunes",
        "email": "ethiagoz145@gmail.com"
    }
)
meu_usuario = "admin"
minha_senha = "admin"

security = HTTPBasic()

meus_livros = {}

class Livro(BaseModel):
    nome: str
    autor: str
    ano: int

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, meu_usuario)
    is_password_correct = secrets.compare_digest(credentials.password, minha_senha)
    if not (is_password_correct and is_username_correct):
        raise HTTPException(status_code=401, detail="usuario ou senha incorreto.",headers={"WWW-Authenticate": "Basic"})
@app.get("/livros")
def get_livros(credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if not meus_livros:
        return {"message": "Nenhum livro encontrado."}
    else:
        return {"livros": meus_livros}

#ID
#NOME
#AUTOR
#ANO

@app.post("/adicionar_livro")
def post_livro(id: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id in meus_livros:
        raise HTTPException(status_code=400, detail="Livro já existe.")

    meus_livros[id] = livro.model_dump()
    return {"message": "Livro adicionado com sucesso."}

@app.put("/atualizar_livro/{id}")
def put_livro(id: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id not in meus_livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    meus_livros[id] = livro.model_dump()
    return {"message": "Livro atualizado com sucesso."}

@app.delete("/remover_livro/{id}")
def delete_livro(id:int, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id in meus_livros:
        del meus_livros[id]
        return {"message": "Livro removido com sucesso."}
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
