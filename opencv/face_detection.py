#pip install opencv-python
#curl https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml > haarcascade_frontalface_default.xml
import cv2

img = SCT(bbox)

def FaceDetection(img):
    face_cascade = cv2.CascadeClassifier(
        'haarcascade_frontalface_default.xml')
    face_rects = face_cascade.detectMultiScale(img)
    (face_x, face_y, w, h) = tuple(face_rects[0])
    track_window = (face_x, face_y, w, h)

    roi = img[face_y:face_y+h, face_x:face_x+w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
    rect, track_window = cv2.meanShift(dst, track_window, term_crit)

    return face_rects, track_window
