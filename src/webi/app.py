from flask import Flask, render_template, redirect, session, request
from .. import base

app = Flask(__name__)
app.secret_key = 'PARMAN_DjkmcVPEWRLHT34'

handler = base.MainHandler('sqlite:///parman.db')

@app.route('/')
def index():
    if session.get('username') and session.get('password'):
        return render_template('index.html', records=handler.get_records({
        'username' : session['username'],
        'password' : session['password']
    })['records'])
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = handler.login({
            'username' : username,
            'password' : password
        })
        if response['status'] == 200:
            session['username'] = username
            session['password'] = password
            return redirect('/')
        return render_template('login.html', error_msg=response['msg'])
    return render_template('login.html')

@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        username = session['username']
        password = session['password']
        response = handler.login({
            'username' : username,
            'password' : password
        })
        if response['status'] == 200:
            response2 = handler.add_record({
                'credits' : {
                    'username' : username,
                    'password' : password
                },
                'record' : {
                    'service' : request.form.get('service'),
                    'username' : request.form.get('username'),
                    'password' : request.form.get('password'),
                    'description' : request.form.get('description')
                }
            })
            if response2['status'] == 201:
                return render_template('close_window.html')
            return render_template('add_record.html', error_msg=response2['msg'])
        return redirect('/', 403)
    return render_template('add_record.html')

@app.route('/logout')
def logout():
    session['username'] = None
    session['password'] = None
    return redirect('/')

if __name__ == '__main__':
    app.run()