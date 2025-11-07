import os
from dotenv import load_dotenv
from flask import Flask
from database.models import db
from routes.admin import admin_route
from routes.auth import auth_route
from routes.home import home_route

# Carrega o .env (apenas local; em produção Render usa variáveis de ambiente)
load_dotenv()  # procura pelo .env na raiz do projeto e carrega para os env vars

app = Flask(__name__)

# SECRET_KEY vem do .env (ou usa fallback seguro)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24).hex()

# Configuração do banco: usa DATABASE_URL do .env ou fallback local
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///doa_mais.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o SQLAlchemy
db.init_app(app)

# Registrar rotas
app.register_blueprint(admin_route, url_prefix="/admin")
app.register_blueprint(auth_route, url_prefix="/auth")
app.register_blueprint(home_route)

# Criação automática das tabelas
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
