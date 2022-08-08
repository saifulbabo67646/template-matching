from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import cv2, numpy as np
from imutils.object_detection import non_max_suppression
import base64

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
    threshold = request.form.get('threshold')
    method = request.form.get('method')
    if image_req and template_req and threshold:
        print("threshold:", threshold)
        img_bytes = np.frombuffer(image_req, np.uint8)
        template_bytes = np.frombuffer(template_req, np.uint8)
        img = cv2.imdecode(img_bytes, cv2.IMREAD_UNCHANGED)
        template = cv2.imdecode(template_bytes, cv2.IMREAD_UNCHANGED)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        w, h = template_gray.shape[::-1]
        res = cv2.matchTemplate(img_gray, template_gray, int(method))
        (y_points, x_points) = np.where(res >= float(threshold))
        boxes = list()
        for (x, y) in zip(x_points, y_points):
            boxes.append((x, y, x + w, y + h))
        boxes = non_max_suppression(np.array(boxes))
        c=0
        for (x1, y1, x2, y2) in boxes:
            c+=1
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0),2)
        # return "Detected object: "+str(c)
        data = cv2.imencode('.png', img)[1].tobytes()
        # return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n', mimetype='image/png; boundary=frame')

        data = base64.b64encode(data).decode()   

        return jsonify({
            'msg': 'success', 
            'format': 'png',
            'detected': c,
            'img': data
        })
    return "not ok"

if __name__ == '__main__':
    app.run(debug=True)