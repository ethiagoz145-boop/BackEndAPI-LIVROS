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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI(
    title="API de Livros",
    description="Uma API simples para gerenciar livros.",
    version="1.0.0",
    contact={
        "name": "Thiago Nunes",
        "email": "ethiagoz145@gmail.com"
    }
)

meus_livros = {}

class Livro(BaseModel):
    nome: str
    autor: str
    ano: int

@app.get("/livros")
def get_livros():
    if not meus_livros:
        return {"message": "Nenhum livro encontrado."}
    else:
        return {"livros": meus_livros}

#ID
#NOME
#AUTOR
#ANO

@app.post("/adicionar_livro")
def post_livro(id: int, livro: Livro):
    if id in meus_livros:
        raise HTTPException(status_code=400, detail="Livro já existe.")

    meus_livros[id] = livro.model_dump()
    return {"message": "Livro adicionado com sucesso."}

@app.put("/atualizar_livro/{id}")
def put_livro(id: int, livro: Livro):
    if id not in meus_livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    meus_livros[id] = livro.model_dump()
    return {"message": "Livro atualizado com sucesso."}

@app.delete("/remover_livro/{id}")
def delete_livro(id:int):
    if id in meus_livros:
        del meus_livros[id]
        return {"message": "Livro removido com sucesso."}
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
