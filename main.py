# importações do projeto
from flask import Flask, request, render_template, redirect, url_for

from models import Aluno, db

# Criando o objeto do projeto
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
db.init_app(app)

#criando a primeira rota
@app.route("/")
def main():
    return "<h1>Olá, bem-vindo ao nosso site. <h1>"

@app.route("/python")
def python():
    return "<H1>Bem-vindo a esta página </H1>. <h2>Aqui você vai aprender sobre Python.</h2>"

@app.route("/form_media")
def form_media():
    return render_template("form_media.html")

@app.route("/calcula_media")
def calcula_media():

    primeira = request.args.get('primeira')
    segunda = request.args.get('segunda')

    if primeira and segunda:
        primeira = float(primeira) # convertendo valor para decimal
        segunda = float(segunda) # convertendo valor para decimal

        media = (primeira + segunda) / 2

        if media >= 7:
            resultado = f"Média = {media}. Resultado: APROVADO."
        elif media >= 4:
            resultado = f"Média = {media}. Resultado: RECUPERAÇÃO."
        else:
            resultado = f"Média = {media}. Resultado: REPROVADO."

    else:
        resultado = "Insira as notas para calcular média. Ex: ?primeira=5&segunda=8"

    return render_template("form_media.html", media=media, resultado=resultado)

# CRUD - READ = LEITURA (SELECT)
@app.route("/aluno")
def lista_alunos():
    alunos = Aluno.query.all()
    return render_template("lista_alunos.html", alunos=alunos)

# CRUD - CREATE = INSERIR (INSERT)
@app.route("/aluno/add", methods=['GET','POST'])
def add_aluno():
    if request.method == "POST":
        nome = request.form['nome']
        turma = request.form['turma']

        novo_aluno = Aluno(nome=nome,turma=turma)
        db.session.add(novo_aluno)
        db.session.commit()

        return redirect(url_for('lista_alunos'))
    return render_template("add_aluno.html")

# CRUD - UPDATE - ALTERAÇÃO (UPDATE)
@app.route("/aluno/<int:id>/edit", methods=['GET','POST'])
def edit_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    if request.method == "POST":
        aluno.nome = request.form['nome']
        aluno.turma = request.form['turma']
        db.session.commit()

        return redirect(url_for('lista_alunos'))
    return render_template("edit_aluno.html", aluno=aluno)

# CRUD - DELETE - EXCLUSÃO (DELETE)
@app.route("/aluno/<int:id>/delete", methods=['POST'])
def delete_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('lista_alunos'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)