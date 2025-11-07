from flask import Blueprint, render_template, request, redirect, url_for, session
from database.models import db, Usuario, Recurso, Doacao
from datetime import datetime

admin_route = Blueprint("admin", __name__)

# CRUD de usuários
@admin_route.route("/users")
def gerencia_user():
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for("auth.login"))

    usuarios = Usuario.query.all()
    return render_template("lista_users.html", usuarios=usuarios, usuario=usuario)


# ==========================
# CRUD DE RECURSOS
# ==========================

@admin_route.route("/recursos/<tipo>")
def lista_recursos(tipo):
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for("auth.login"))

    recursos = Recurso.query.filter_by(tipo=tipo).all()
    return render_template("recursos.html", tipo=tipo, recursos=recursos, usuario=usuario)


@admin_route.route("/recursos/novo", methods=["GET", "POST"])
def novo_recurso():
    if request.method == "POST":
        recurso = Recurso(
            tipo=request.form["tipo"],
            item=request.form["item"],
            descricao=request.form["descricao"],
            quantidade=request.form["quantidade"],
            responsavel=request.form["responsavel"]
        )
        db.session.add(recurso)
        db.session.commit()
        return redirect(url_for("admin.lista_recursos", tipo=recurso.tipo))
    return render_template("novo_recurso.html")


@admin_route.route("/recursos/<int:recurso_id>/editar", methods=["GET", "POST"])
def editar_recurso(recurso_id):
    recurso = Recurso.query.get_or_404(recurso_id)
    if request.method == "POST":
        recurso.tipo = request.form["tipo"]
        recurso.item = request.form["item"]
        recurso.descricao = request.form["descricao"]
        recurso.quantidade = request.form["quantidade"]
        recurso.responsavel = request.form["responsavel"]
        db.session.commit()
        return redirect(url_for("admin.lista_recursos", tipo=recurso.tipo))
    return render_template("editar_recurso.html", recurso=recurso)


@admin_route.route("/recursos/<int:recurso_id>/excluir")
def excluir_recurso(recurso_id):
    recurso = Recurso.query.get_or_404(recurso_id)
    tipo = recurso.tipo
    db.session.delete(recurso)
    db.session.commit()
    return redirect(url_for("admin.lista_recursos", tipo=tipo))


# ==========================
# REGISTRO DE DOAÇÃO
# ==========================

@admin_route.route("/recursos/<int:recurso_id>/doar", methods=["POST"])
def registrar_doacao(recurso_id):
    usuario_dict = session.get("usuario")
    if not usuario_dict:
        return redirect(url_for("auth.login"))

    usuario = Usuario.query.filter_by(email=usuario_dict["email"]).first()
    recurso = Recurso.query.get_or_404(recurso_id)

    doacao = Doacao(usuario_id=usuario.id, recurso_id=recurso.id)
    db.session.add(doacao)
    db.session.commit()

    print(f"✅ {usuario.nome} doou para {recurso.item}")
    return redirect(url_for("admin.lista_recursos", tipo=recurso.tipo))


# ==========================
# LISTA DE DOAÇÕES
# ==========================

@admin_route.route("/doacoes")
def lista_doacoes():
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for("auth.login"))

    doacoes = Doacao.query.join(Usuario).join(Recurso).add_columns(
        Usuario.nome.label("usuario_nome"),
        Recurso.item.label("item"),
        Recurso.tipo.label("tipo"),
        Doacao.data
    ).all()

    return render_template("lista_doacoes.html", doacoes=doacoes, usuario=usuario)
