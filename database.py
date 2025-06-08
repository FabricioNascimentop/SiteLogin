from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

load_dotenv()
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
DATABASE_URI = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

class Usuario(db.Model):
    __tablename__ = 'SiteLogin'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    telefone: Mapped[str] = mapped_column(String(12), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(128)) 
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.senha = generate_password_hash(password,  method="pbkdf2:sha256", salt_length=16)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def password(self):
        raise AttributeError("Password is write-only")

