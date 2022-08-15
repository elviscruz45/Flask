#bootstrap
from ensurepip import bootstrap
#Flask
from flask import request,make_response,redirect, render_template,session , url_for,flash
from flask_bootstrap import Bootstrap


#Testing
import unittest

#Importing files from app
from app import create_app
from app.forms import LoginForm

#Firestore base de datos
from app.firestore_service import get_users


#iniciar la aplicacion Flask
app=create_app()

todos=["Comprar cafe","Enviar solicitud de compra","Entregar video a productor"]

#Crear formularios
## Se paso al archivo app/forms.py


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



@app.route("/hello",methods=["GET"]) #,"POST"
def hello():
    #user_ip=request.cookies.get("user_ip")
    user_ip=session.get("user_ip")
    #login_form=LoginForm()
    username=session.get("username")
    context={
        "user_ip":user_ip,
        "todos":todos,
        #"login_form":login_form,
        "username":username
    }
    
#    if login_form.validate_on_submit():
#       username=login_form.username.data
#       session["username"]=username
#       flash("Nombre de usuario registrado con exito")
#        return redirect(url_for("index"))

    users=get_users()
    for user in users:
        print(user)
        
        
    return render_template("hello.html",**context)


