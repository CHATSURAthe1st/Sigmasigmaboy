from flask import Flask, render_template, request, jsonify
import sympy as sp
import pyautogui
import cv2
import mediapipe as mp
import threading

app = Flask(__name__)

# Solve algebra, general math, or quadratic equations
@app.route('/solve', methods=['POST'])
def solve():
    try:
        expression = request.json['expression'].replace('^', '**')  # Replace ^ with ** for SymPy compatibility
        if "=" in expression:
            lhs, rhs = expression.split("=")
            equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            solution = sp.solve(equation)
        else:
            result = sp.sympify(expression)
            solution = sp.simplify(result)
        return jsonify({'result': str(solution)})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    return render_template('index.html')

# Background thread for facial movement tracking
def track_face():
    mp_face = mp.solutions.face_detection
    cap = cv2.VideoCapture(0)

    with mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(frame_rgb)

            if results.detections:
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    x_center = bbox.xmin + bbox.width / 2
                    y_center = bbox.ymin + bbox.height / 2

                    screen_width, screen_height = pyautogui.size()
                    mouse_x = int(x_center * screen_width)
                    mouse_y = int(y_center * screen_height)

                    pyautogui.moveTo(mouse_x, mouse_y, duration=0.1)

    cap.release()

# Start the face-tracking thread
threading.Thread(target=track_face, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)
