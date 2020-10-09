from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# App de servidor
app = Flask(__name__)


# Configuracion de mi conexion Db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'


# Ejecucion del modulo SQLAlchemy
# Cursor: Variable que me permite realizar consultas en DB
cursor = SQLAlchemy(app)


# Modelo
class Task(cursor.Model):
    id = cursor.Column(cursor.Integer, primary_key=True)
    content = cursor.Column(cursor.String(200))
    done = cursor.Column(cursor.Boolean)


# Ruta principal
@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks = tasks)


# Ruta CRUD
@app.route('/create-task', methods=['POST'])
def create():
    task = Task(content=request.form['content'], done=False)
    # Guardar nuestro objeto
    cursor.session.add(task)
    # Termina con la session
    cursor.session.commit()
    return redirect(url_for('home'))

@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id = int(id)).first()
    task.done = not(task.done)
    cursor.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<id>')
def delete(id):
    task = Task.query.filter_by(id=int(id)).delete()
    # Eliminar el item
    cursor.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
