from controller.control import AgendControl
from flask import Flask, request, render_template, redirect, url_for
from models.banco import Modelo
import os

# ---------- App ----------

app = Flask(__name__, template_folder=os.path.join('view', 'templates'), static_folder="view/static")

agenda = AgendControl()

# ---------- Database ----------

bd = Modelo()
bd.gera_banco()

# ---------- Titles ----------

def title(opc):
    match opc:
        case 1:
            return "FloraTime"
        case 2:
            return "FloraTime - Home"
        case 3:
            return "FloraTime - Create"
        case 4:
            return "FloraTime - Update"

# ---------- Routes ----------

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        login = agenda.valida_login(user, password)
        if login:
            return redirect(url_for('home'))
    return render_template('index.html', title=title(1))

@app.route('/home')
def home():
    all_agend = agenda.read_all()
    return render_template('home.html', title=title(2), agendamentos=all_agend)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        horario = request.form.get('horario')
        cliente = request.form.get('cliente')
        endereco = request.form.get('endereco')
        servico = request.form.get('servico')
        valor = request.form.get('valor')
        observacao = request.form.get('observacao')
        agenda.create(horario, cliente, endereco, servico, valor, observacao)
        return redirect(url_for('home'))
    return render_template('create.html', title=title(3))

@app.route('/<int:ordem>/update', methods=['GET', 'POST'])
def update(ordem):
    if request.method == 'POST':
        horario = request.form.get('horario')
        cliente = request.form.get('cliente')
        endereco = request.form.get('endereco')
        servico = request.form.get('servico')
        valor = request.form.get('valor')
        observacao = request.form.get('observacao')
        agenda.update(ordem, horario, cliente, endereco, servico, valor, observacao)
        return redirect(url_for('home'))
    agend = agenda.read(ordem)
    return render_template('update.html', title=title(4), dados=agend)

@app.route('/<int:ordem>/delete', methods=['POST'])
def delete(ordem):
    agenda.delete(ordem)
    return redirect(url_for('home'))

# ---------- Settings ----------

if __name__ == "__main__":
    app.run(debug=True)