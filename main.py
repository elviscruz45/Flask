#bootstrap
from ensurepip import bootstrap
#Flask
from flask import Flask,request,make_response,redirect, render_template,session , url_for,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

#wtf formularios
from wtforms.fields import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired

#Testing
import unittest

from app import create_app

#iniciar la aplicacion Flask
app=create_app()

todos=["Comprar cafe","Enviar solicitud de compra","Entregar video a productor"]

#Crear formularios

class LoginForm(FlaskForm):
    username=StringField("Nombre de usuario",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Enviar")

#Testing

@app.cli.command()
def test():
    tests=unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)
    
# error managements

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html",error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)

# Routes

@app.route("/")
def index():
    user_ip=request.remote_addr
    response=make_response(redirect("/hello"))
    #response.set_cookie("user_ip",user_ip)
    session["user_ip"]=user_ip
    
    return response



@app.route("/hello",methods=["GET","POST"])
def hello():
    #user_ip=request.cookies.get("user_ip")
    user_ip=session.get("user_ip")
    login_form=LoginForm()
    username=session.get("username")
    context={
        "user_ip":user_ip,
        "todos":todos,
        "login_form":login_form,
        "username":username
    }
    
    if login_form.validate_on_submit():
        username=login_form.username.data
        session["username"]=username
        flash("Nombre de usuario registrado con exito")
        return redirect(url_for("index"))

    return render_template("hello.html",**context)


if __name__=="__main__":
    app.run(port=5000,debug=True)

