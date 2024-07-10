from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

#importar los models
from flask_app.models.users import User

#importar BCrpyt 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register",methods=["post"])
def register():



    if not User.validate_user(request.form):
        #No es válida la info, redireccionamos al formulario
        return redirect('/')    
    
    #Encriptamos la contraseña
    pass_encrypt = bcrypt.generate_password_hash(request.form['password'])
    #Generar un diccionario con toda la info del formulario
    form = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pass_encrypt
    }

    id = User.save(form) #Recibo a cambio el ID del nuevo usuario
    session['user_id'] = id #Guardamos en sesión el identificador del usuario
    return redirect('/dashboard')

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("favor iniciar session","not_in_session")
        return redirect("/")

    form = {"id": session["user_id"]}
    user=User.get_by_id(form)

    return render_template("dashboard.html", user=user)


@app.route("/login", methods=["post"])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("E-mail no registrado", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("password incorrecto", "login")
        return redirect("/")

    session["user_id"] = user.id
    return redirect("/dashboard")


@app.route("/logout")
def logaut():
    session.clear()
    return redirect("/")
