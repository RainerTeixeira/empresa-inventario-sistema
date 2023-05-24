from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Configuração do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventario'
mysql = MySQL(app)

# Configuração da sessão
app.secret_key = 'chave_secreta'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        senha = request.form['password']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM funcionarios WHERE login=%s AND senha=%s", (login, senha))
        user = cur.fetchone()

        if user:
            session['login'] = user['login']
            session['nivel_permissao'] = user['nivel_permissao']
            return redirect('/painel')
        else:
            return render_template('login.html', error='Usuário ou senha incorretos.')
    
    return render_template('login.html')

@app.route('/painel')
def painel():
    if 'login' in session:
        login = session['login']
        nivel_permissao = session['nivel_permissao']
        return render_template('painel.html', login=login, nivel_permissao=nivel_permissao)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
