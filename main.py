#bootstrap
from ensurepip import bootstrap
#Flask
from flask import request,make_response,redirect, render_template,session , url_for,flash
from flask_bootstrap import Bootstrap
from flask_login import login_required,current_user

#Testing
import unittest

#Importing files from app
from app import create_app
from app.forms import TodoForm, DeleteTodoForm,UpdateTodoForm

#Firestore base de datos
from app.firestore_service import update_todo,get_users , get_todos, put_todo,delete_todo

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

@app.route("/hello",methods=["GET","POST"])
@login_required
def hello():
    user_ip=session.get("user_ip")
    username=current_user.id
    todo_form=TodoForm()
    delete_form=DeleteTodoForm()
    update_form=UpdateTodoForm()
    context={
        "user_ip":user_ip,
        "todos":get_todos(user_id=username),
        "username":username,
        "todo_form":todo_form,
        "delete_form":delete_form,
        "update_form":update_form
    }
    
    if todo_form.validate_on_submit():
        put_todo(user_id=username,description=todo_form.description.data)
        flash("Tu tarea se creo con exito! ")
        return redirect(url_for("hello"))
    return render_template("hello.html",**context)

@app.route("/todos/delete/<todo_id>",methods=["POST"])
def delete(todo_id):
    user_id=current_user.id
    delete_todo(user_id=user_id,todo_id=todo_id)
    return redirect(url_for("hello"))


@app.route("/todos/update/<todo_id>/<int:done>",methods=["POST"])
def update(todo_id,done):
    user_id=current_user.id
    update_todo(user_id=user_id,todo_id=todo_id,done=done)
    return redirect(url_for("hello"))


if __name__=="__main__":
    app.run(port=5000,debug=True)

