import dlib
import cv2
import imutils
from imutils import face_utils


class EyeDetector:
    def __init__(self, shape_predictor):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_predictor)

    def predict(self, img):
        height, width, ch = img.shape
        img = imutils.resize(img, width=500)
        koef_x = width / 500.
        koef_y = height / img.shape[0]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 1)
        result = []

        for (i, rect) in enumerate(rects):
            eye_pair = []
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            keys = ['left_eye', 'right_eye']
            for k in keys:
                i, j = face_utils.FACIAL_LANDMARKS_68_IDXS[k]
                pts = shape[i:j]
                min_x = int(min(map(lambda i: i[0], pts)) * koef_x)
                min_y = int(min(map(lambda i: i[1], pts)) * koef_y)
                max_x = int(max(map(lambda i: i[0], pts)) * koef_x)
                max_y = int(max(map(lambda i: i[1], pts)) * koef_y)
                eye_pair.append((min_x, min_y, max_x, max_y))
            result.append(eye_pair)
        return result
