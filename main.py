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


@app.route("/index", methods=['GET', 'POST'])
def index():
    alum_form = forms.UsersForm2(request.form)
    if request.method == 'POST':
        alum = Alumnos(nombre=alum_form.nombre.data,
                       apaterno=alum_form.apaterno.data,
                       email=alum_form.email.data)
        db.session.add(alum)
        db.session.commit()
    return render_template("index.html", form=alum_form)


@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    alum_form = forms.UsersForm2(request.form)
    if request.method == 'GET':
        id = request.args.get("id")
        alumno1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum_form.id.data = request.args.get('id')
        alum_form.nombre.data = alumno1.nombre
        alum_form.apaterno.data = alumno1.apaterno
        alum_form.email.data = alumno1.email
    if request.method == 'POST':
        id = alum_form.id.data
        alumno = Alumnos.query.get(id)
        db.session.delete(alumno)
        db.session.commit()
        return redirect("ABC_Completo")

    return render_template("eliminar.html", form=alum_form)


@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    alum_form = forms.UsersForm2(request.form)
    if request.method == 'GET':
        id = request.args.get("id")
        alumno1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum_form.id.data = request.args.get('id')
        alum_form.nombre.data = alumno1.nombre
        alum_form.apaterno.data = alumno1.apaterno
        alum_form.email.data = alumno1.email
    if request.method == 'POST':
        id = alum_form.id.data
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alumno.nombre = alum_form.nombre.data
        alumno.apaterno = alum_form.apaterno.data
        alumno.email = alum_form.email.data
        db.session.add(alumno)
        db.session.commit()
        return redirect("ABC_Completo")

    return render_template("modificar.html", form=alum_form)


@app.route("/ABC_Completo", methods=["GET", "POST"])
def ABC_Completo():
    alum_form = forms.UsersForm2(request.form)
    alumno = Alumnos.query.all()
    return render_template("ABC_Completo.html", alumnos=alumno)


@app.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    alum_form = forms.UsersForm2(request.form)
    nom = ''
    apa = ''
    ama = ''
    edad = 0
    correo = ''
    if request.method == 'POST' and alum_form.validate():
        nom = alum_form.nombre.data
        apa = alum_form.apaterno.data
        correo = alum_form.email.data
        mensaje = f'Bienvenido {nom}'
        flash(mensaje)

    return render_template("alumnos.html", form=alum_form, nom=nom, apa=apa, ama=ama, edad=edad, correo=correo)


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
