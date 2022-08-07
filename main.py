from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def tes():
    return 'Halo dunia!'

@app.route('/api/tm', methods=["POST"])
def tm():
    # print('tesaja')
    file = request.files['image']
    if file:
        print(file)
        return "OK"
    return "not ok"

if __name__ == '__main__':
    app.run()