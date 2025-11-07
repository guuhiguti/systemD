from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Apenas cria a instância
db = SQLAlchemy()

# ==========================
# USUÁRIOS
# ==========================
class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # colaborador / instituicao / administrador
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================
# RECURSOS
# ==========================
class Recurso(db.Model):
    __tablename__ = "recursos"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    quantidade = db.Column(db.Integer, nullable=False)
    responsavel = db.Column(db.String(100))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relação reversa (um recurso pode ter várias doações)
    doacoes = db.relationship("Doacao", backref="recurso", lazy=True)


# ==========================
# DOAÇÕES
# ==========================
class Doacao(db.Model):
    __tablename__ = "doacoes"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    recurso_id = db.Column(db.Integer, db.ForeignKey("recursos.id"), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship("Usuario", backref="doacoes", lazy=True)
