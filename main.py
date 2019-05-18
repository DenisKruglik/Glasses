from glasses import put_glasses
from PIL import Image
import cv2
import argparse
from detector import EyeDetector
import numpy as np


def process(image, detector):
    faces = detector.predict(image)
    img = cv2_to_pil(image)

    for left_eye, right_eye in faces:
        eye1_left_x, eye1_left_y, eye1_right_x, eye1_right_y = left_eye
        eye2_left_x, eye2_left_y, eye2_right_x, eye2_right_y = right_eye
        lefteye_x = eye1_left_x + ((eye1_right_x - eye1_left_x) // 2)
        lefteye_y = eye1_left_y + ((eye1_right_y - eye1_left_y) // 2)
        righteye_x = eye2_left_x + ((eye2_right_x - eye2_left_x) // 2)
        righteye_y = eye2_left_y + ((eye2_right_y - eye2_left_y) // 2)
        img = put_glasses(img, lefteye_x, lefteye_y, righteye_x, righteye_y)
    return pil_to_cv2(img)


def pil_to_cv2(pil_img):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def cv2_to_pil(cv_img):
    img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)


def run():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=False, help="path to facial landmark predictor", default='./resources/shape_predictor_68_face_landmarks.dat')
    args = vars(ap.parse_args())

    detector = EyeDetector(args['shape_predictor'])
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cool = process(frame, detector)
        cv2.imshow('frame', cool)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run()
