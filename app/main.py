from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import cv2, numpy as np
from imutils.object_detection import non_max_suppression
import base64
from app.solver import PuzzleSolver

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
    tm_type = request.form.get('type')
    print(tm_type)
    print(method)
    if image_req and template_req and method:
        # let me write the puzzleSolver code here
        # Encode images to base64
        base64_puzzle = base64.b64encode(image_req).decode("utf-8")
        base64_piece = base64.b64encode(template_req).decode("utf-8")
        solver = PuzzleSolver(base64_puzzle, base64_piece)
        res = solver.get_position()
        #puzzleSolver end
        img_bytes = np.frombuffer(image_req, np.uint8)
        template_bytes = np.frombuffer(template_req, np.uint8)
        img = cv2.imdecode(img_bytes, cv2.IMREAD_UNCHANGED)
        template = cv2.imdecode(template_bytes, cv2.IMREAD_UNCHANGED)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        w, h = template_gray.shape[::-1]
        # res = cv2.matchTemplate(img_gray, template_gray, int(method))
        if(int(tm_type)):
            print("i am calling from if")
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
        else:
            print("i am calling from else")
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            # if method=="0" or method=="1":
            #     top_left = min_loc
            # else:
            #     top_left = max_loc
            top_left = max_loc
            bottom_right = (top_left[0]+w, top_left[1]+h)
            cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), 3)
            data = cv2.imencode('.png', img)[1].tobytes()
            # return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n', mimetype='image/png; boundary=frame')

            data = base64.b64encode(data).decode()   

            return jsonify({
                'msg': 'success', 
                'format': 'png',
                'detected': 1,
                'img': data
            })
    return "not ok"

# if __name__ == '__main__':
#     app.run(debug=True)