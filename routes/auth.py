from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.usuarios import USUARIOS

auth_route = Blueprint('auth', __name__)

# --- Garantir que o admin exista ---
def garantir_admin():
    if not any(u["tipo"] == "administrador" for u in USUARIOS):
        admin = {
            "id": 1,
            "nome": "Administrador",
            "email": "admin@doa.com",
            "senha": "123",
            "tipo": "administrador"
        }
        USUARIOS.append(admin)
        print("Administrador padrão criado:", admin)

garantir_admin()


# --- Cadastro ---
@auth_route.route("/cadastro", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        tipo = request.form.get("tipo")
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        # Verifica se o e-mail já está cadastrado
        if any(u["email"] == email for u in USUARIOS):
            flash("E-mail já cadastrado!", "danger")
            return redirect(url_for("auth.register"))

        # Cria o novo usuário
        novo_usuario = {
            "id": len(USUARIOS) + 1,
            "nome": nome,
            "email": email,
            "senha": senha,
            "tipo": tipo
        }

        USUARIOS.append(novo_usuario)
        print("USUÁRIO CADASTRADO:", novo_usuario)
        print("TODOS OS USUÁRIOS:", USUARIOS)
        flash("Cadastro realizado com sucesso! Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# --- Login ---
@auth_route.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        # Busca o usuário no "banco"
        usuario = next((u for u in USUARIOS if u["email"] == email and u["senha"] == senha), None)

        if usuario:
            session["usuario"] = usuario
            flash(f"Bem-vindo(a), {usuario['nome']}!", "success")
            return redirect(url_for("home.home"))  # redireciona pra home geral
        else:
            flash("E-mail ou senha incorretos!", "danger")

    return render_template("login.html")


# --- Logout ---
@auth_route.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Você saiu da conta.", "info")
    return redirect(url_for("auth.login"))
