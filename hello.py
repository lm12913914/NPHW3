from flask import Flask, session, redirect, url_for, escape, request
from flask.templating import render_template
import sqlite3
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('try1.db')
    c = conn.cursor()
    if 'username' in session:#logged in
        if request.method == 'POST':
            print(session['username'], request.form.get('password'), request.form.get('email'), session['username'])
            c.execute('UPDATE users SET name=?, password=?, email=? WHERE name=?', (session['username'], request.form.get('password'), request.form.get('email'), session['username']))
            conn.commit()
        c.execute("select * from users where name=?", (session['username'],))
        rvalue = c.fetchone()
        print(session['username'])
        print(rvalue)
        username, userpwd, useremail = rvalue
        c.close()
        return render_template('profile.html', username=username, userpwd=userpwd, useremail=useremail)
    c.close()
    return '''
            <p>You are not logged in</p>
            <p><a href="login">Clicke here to login</a></p>
            '''

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    conn = sqlite3.connect('try1.db')
    c = conn.cursor()
    if request.method == 'POST':
        item = (request.form.get('name'), request.form.get('password'), request.form.get('email'))
        print(item)
        c.execute("select name from users where name=?", (request.form.get('name'),))
        p=c.fetchall()
        if p==[]:
            c.execute("INSERT INTO users VALUES (?,?,?)", item)
            conn.commit()
            c.close()
        else:#already exist
            c.close()
            return '<div align="center"><p>Account is already exist!Please try another one.</p><p><a href="create">Click here to get back</a></p></div>'
        return redirect(url_for('login'))
    c.close()
    return render_template('createAccount.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('try1.db')
    c = conn.cursor()
    if request.method == 'POST':
        c.execute("select name from users where name=? and password=?", (request.form.get('account'),request.form.get('password')))
        p=c.fetchall()
        if p==[]:
            return '<div align="center"><p>Account/password not correct!</p><p><a href="login">Click here to get back</a></p></div>'
            c.close()
        session['username'] = request.form.get('account')
        return redirect(url_for('index'))
    c.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == "__main__":
    conn = sqlite3.connect('try1.db')
    c = conn.cursor()
    try:
        c.execute('CREATE TABLE users(name, password, email)')
        conn.commit()   
    except Exception as e:
        print(e)
    c.close()
    app.debug = True
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
    