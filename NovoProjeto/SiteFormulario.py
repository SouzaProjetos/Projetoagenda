from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurações do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Security@database-site.cfc2ysyaidks.us-east-1.rds.amazonaws.com/database-site'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do Banco de Dados
class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Mensagem {self.nome}>"

# Página inicial com o formulário
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        # Salvar os dados no banco de dados
        nova_mensagem = Mensagem(nome=nome, email=email, mensagem=mensagem)
        db.session.add(nova_mensagem)
        db.session.commit()

        # Redireciona para a página de agradecimento
        return redirect(url_for('obrigado'))

    return render_template('index.html')


# Página de agradecimento
@app.route('/obrigado')
def obrigado():
    return "Obrigado, assim que possível responderemos via e-mail."


if __name__ == '__main__':
    # Cria as tabelas no banco de dados (se não existirem)
    with app.app_context():
        db.create_all()

    app.run(debug=True)
