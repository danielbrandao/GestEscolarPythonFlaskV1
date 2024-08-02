from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    turma = db.Column(db.String(100), nullable=False)

