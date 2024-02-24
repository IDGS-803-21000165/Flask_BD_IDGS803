from flask import Flask, render_template, request, flash, Response, g, redirect
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def index():
    escuela = "UTL!!!"
    alumnos = ["Simón", "Alec", "Ulises"]
    return render_template("index.html", escuela=escuela, alumnos=alumnos)


@app.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    alum_form = forms.UsersForm(request.form)
    nom = ''
    apa = ''
    ama = ''
    edad = 0
    correo = ''
    if request.method == 'POST' and alum_form.validate():
        nom = alum_form.nombre.data
        apa = alum_form.aPaterno.data
        ama = alum_form.aMaterno.data
        edad = alum_form.edad.data
        correo = alum_form.correo.data
        mensaje = f'Bienvenido {nom}'
        flash(mensaje)

    return render_template("alumnos.html", form=alum_form, nom=nom, apa=apa, ama=ama, edad=edad, correo=correo)


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
