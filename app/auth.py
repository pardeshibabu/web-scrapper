from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "defaulttoken")

def authenticate(x_token: str = Header(...)):
    if x_token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

def validate_token(token: str):
    from app.config import TOKEN
    if token != TOKEN:
        raise ValueError("Invalid token")
    
