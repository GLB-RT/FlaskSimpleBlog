from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import send_from_directory, abort
import json
from flask import jsonify
import os

app = Flask(__name__)
app.secret_key = 'f3bb66dc-23fe-40a6-b5ac-f633c804c49d' #random API key from https://codepen.io/corenominal/pen/rxOmMJ

USERNAME = "username"
PASSWORD = "password"

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/pliki')
@login_required
def pliki():
    folder = os.path.join(os.path.dirname(__file__), 'nazwa_folderu')
    if not os.path.exists(folder):
        os.makedirs(folder)
    lista_plikow = os.listdir(folder)
    return render_template('pliki.html', pliki=lista_plikow)

@app.route('/pliki/<filename>')
@login_required
def otworz_plik(filename):
    folder = os.path.join(os.path.dirname(__file__), 'nazwa_folderu')
    filepath = os.path.join(folder, filename)
    if not os.path.isfile(filepath):
        abort(404)
    return send_from_directory(folder, filename)

@app.route('/get_files')
@login_required
def get_files():
    folder = os.path.join(os.path.dirname(__file__), 'nazwa_folderu')
    if not os.path.exists(folder):
        os.makedirs(folder)
    lista_plikow = os.listdir(folder)
    return jsonify(lista_plikow)


@app.route('/Social')
@login_required
def contact():
    return render_template('contact.html')

@app.route('/redditscraper')
@login_required
def redditscraper():
    return render_template('redditscraper.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Nieprawidłowy login lub hasło!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
