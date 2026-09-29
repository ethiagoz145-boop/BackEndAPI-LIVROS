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

app = FastAPI()

meus_livros = {}

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
def post_livro(id:int, nome:str, autor:str, ano:int):
    if id in meus_livros: 
        raise HTTPException(status_code=400, detail="Livro já existe.")
    else:
        meus_livros[id] = {"nome": nome, "autor": autor, "ano": ano}
        return {"message": "Livro adicionado com sucesso."}
@app.put(" ")
def put_nome(id:int, nome:str, autor:str, ano:int):
    meu_livro = meus_livros.get(id)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        if nome:
            meu_livro["nome"] = nome 
        if autor:
            meu_livro["autor"] = autor
        if ano:
            meu_livro["ano"] = ano
        return {"message": "Livro atualizado com sucesso."}

@app.delete("/remover_livro/{id}")
def delete_livro(id:int):
    if id in meus_livros:
        del meus_livros[id]
        return {"message": "Livro removido com sucesso."}
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")