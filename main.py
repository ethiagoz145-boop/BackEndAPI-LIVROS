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

# ---------------------------
# Explicação rápida da API:
# - FastAPI cria as rotas da aplicação web.
# - A API gerencia uma lista de livros em memória.
# - Cada livro tem nome, autor e ano.
# - A autenticação HTTP Basic exige usuário e senha antes de usar as rotas.
# ---------------------------

app = FastAPI(
    title="API de Livros",
    description="Uma API simples para gerenciar livros.",
    version="1.0.0",
    contact={
        "name": "Thiago Nunes",
        "email": "ethiagoz145@gmail.com"
    }
)

# Credenciais usadas para autenticação básica da API.
meu_usuario = "admin"
minha_senha = "admin"

# Configuração do esquema de autenticação HTTP Basic do FastAPI.
security = HTTPBasic()

# Banco de dados em memória: guarda os livros usando o ID como chave.
# Exemplo: {1: {"nome": "Livro A", "autor": "Autor X", "ano": 2024}}
meus_livros = {}

# Modelo de dados do livro recebido nas requisições.
# Pydantic valida os campos antes de salvar/atualizar.
class Livro(BaseModel):
    nome: str
    autor: str
    ano: int

# Função que valida usuário e senha.
# Se a autenticação falhar, gera um erro 401 e exige login básico.
def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, meu_usuario)
    is_password_correct = secrets.compare_digest(credentials.password, minha_senha)
    if not (is_password_correct and is_username_correct):
        raise HTTPException(
            status_code=401,
            detail="usuario ou senha incorreto.",
            headers={"WWW-Authenticate": "Basic"}
        )

# GET /livros
# Lista todos os livros cadastrados.
# Se não houver nenhum, retorna uma mensagem informando isso.
@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Parâmetros de paginação inválidos.")
    if not meus_livros:
        return {"message": "Nenhum livro cadastrado."}

    livros_ordenados = sorted(meus_livros.items(), key=lambda x: x[0])
    
    start = (page - 1) * limit
    end = start + limit

    livros_paginados = [
        {"id": id, "nome": livro["nome"], "autor": livro["autor"], "ano": livro["ano"]}
        for id, livro in livros_ordenados[start:end]
    ]
    return {"page":page, 
            "limit":limit,
            "total": len(meus_livros),
            "livros": livros_paginados}

# Estrutura esperada para cada livro:
# ID
# NOME
# AUTOR
# ANO

# POST /adicionar_livro
# Cria um novo livro no dicionário, usando o ID como chave.
# Se o ID já existir, retorna erro 400.
@app.post("/adicionar_livro")
def post_livro(id: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id in meus_livros:
        raise HTTPException(status_code=400, detail="Livro já existe.")

    meus_livros[id] = livro.model_dump()
    return {"message": "Livro adicionado com sucesso."}

# PUT /atualizar_livro/{id}
# Atualiza os dados de um livro já existente.
# Se o ID não for encontrado, retorna erro 404.
@app.put("/atualizar_livro/{id}")
def put_livro(id: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id not in meus_livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    meus_livros[id] = livro.model_dump()
    return {"message": "Livro atualizado com sucesso."}

# DELETE /remover_livro/{id}
# Remove um livro da lista usando o ID.
# Se o livro não existir, retorna erro 404.
@app.delete("/remover_livro/{id}")
def delete_livro(id:int, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if id in meus_livros:
        del meus_livros[id]
        return {"message": "Livro removido com sucesso."}
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
