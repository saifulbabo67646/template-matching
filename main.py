from flask import Flask, request
from flask_cors import CORS
import cv2, numpy as np
app = Flask(__name__)
CORS(app)

@app.route('/')
def tes():
    return 'Halo dunia!'

@app.route('/api/tm', methods=["POST"])
def tm():
    # print('tesaja')
    image_req = request.files['image'].read()
    template_req = request.files['template'].read()
    if image_req and template_req:
        img_bytes = np.fromstring(image_req, np.uint8)
        template_bytes = np.fromstring(template_req, np.uint8)
        img = cv2.imdecode(img_bytes, cv2.IMREAD_UNCHANGED)
        template = cv2.imdecode(template_bytes, cv2.IMREAD_UNCHANGED)
        print(img)
        return "OK"
    return "not ok"

if __name__ == '__main__':
    app.run(debug=True)