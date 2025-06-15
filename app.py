from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/random-image')
def random_image():
    return render_template('random_image.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
