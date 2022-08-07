from flask import Flask
app = Flask(__name__)

@app.route('/')
def tes():
    return 'Halo dunia!'

if __name__ == '__main__':
    app.run()