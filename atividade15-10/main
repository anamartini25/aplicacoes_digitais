from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import requests
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, auth

from database import Base, Session, engine
from models import Animais

load_dotenv()
app = FastAPI()
API_KEY = os.getenv("FIREBASE_API_KEY")
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
security = HTTPBearer()
Base.metadata.create_all(engine)

class AnimalPayLoad(BaseModel):
    nome: str
    especie: str
    raca: str
    idade: int 
    nome_tutor: str
    veterinario_id: str

class Veterinario(BaseModel):
    email: str
    senha: str

@app.post("/veterinarios")
def criar_usuario(usuario: Veterinario):
    try:
        novo_usuario = auth.create_user(email=usuario.email, password=usuario.senha)
        return {
            "uid": novo_usuario.uid,
            "email": novo_usuario.email
        }

    except Exception:
        raise HTTPException(status_code=400, detail="Não foi possível criar o usuário")

@app.post("/login")
def login(usuario: Veterinario):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    dados = {
        "email": usuario.email,
        "password": usuario.senha,
        "returnSecureToken": True
    }
    resposta = requests.post(url, json=dados)
    if resposta.status_code != 200:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    return {
        "token": resposta.json()["idToken"]
    }

def verificar_token(credenciais: HTTPAuthorizationCredentials = Depends(security)):
    token = credenciais.credentials
    try:
        usuario = auth.verify_id_token(token)
        return usuario
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")


@app.get("/perfil")
def perfil(usuario = Depends(verificar_token)):
    return {
        "uid": usuario["uid"],
        "email": usuario["email"]
    }


 
@app.post("/animais", status_code=status.HTTP_201_CREATED)
def cadastrar_animal(dados: AnimalPayLoad, usuario = Depends(verificar_token)):
    db = Session()

    animal = Animais(
        nome=dados.nome,
        especie=dados.especie,
        raca=dados.raca,
        idade=dados.idade,
        nome_tutor=dados.nome_tutor,
        veterinario_id=usuario["uid"]
    )

    db.add(animal)
    db.commit()
    db.refresh(animal)
    db.close()

    return animal

@app.get("/animais", status_code=status.HTTP_200_OK)
def listar_animais(usuario = Depends(verificar_token)):
    db = Session()

    try: 
        animal = db.query(Animais).all()
        return animal

    except Exception as e:
        print("Erro ao listar animais:", e)
    finally:
        db.close()

    

@app.get("/animais/{animal_id}", status_code=status.HTTP_200_OK)
def buscar_animal(animal_id: int, usuario = Depends(verificar_token)):
    db = Session()
    animal = db.query(Animais).filter(Animais.id == animal_id, Animais.veterinario_id == usuario["uid"]).first()
    db.close()

    if animal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal não encontrado"
        )

    return animal

@app.put("/animais/{animal_id}", status_code=status.HTTP_200_OK)
def atualizar_animal(animal_id: int, dados: AnimalPayLoad, usuario = Depends(verificar_token)):
    db = Session()

    animal = db.query(Animais).filter(Animais.id == animal_id).first()

    if animal is None:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal não encontrado"
        )

    animal.nome = dados.nome
    animal.especie = dados.especie
    animal.raca = dados.raca
    animal.idade = dados.idade
    animal.nome_tutor = dados.nome_tutor
    animal.veterinario_id = dados.veterinario_id

    db.commit()
    db.refresh(animal)
    db.close()

    return animal

@app.delete("/animais/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_animal(animal_id: int, usuario = Depends(verificar_token)):
    db = Session()
    animal = db.query(Animais).filter(Animais.id == animal_id, Animais.veterinario_id == usuario["uid"]).first()

    try:
        animal = db.query(Animais).filter(
            Animais.id == animal_id,
            Animais.veterinario_id == usuario["uid"]
        ).first()

        if animal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Animal não encontrado ou não pertence a este veterinário"
            )

        db.delete(animal)
        db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        
