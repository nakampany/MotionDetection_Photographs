face_rects, track_window = FaceDetection(img)
x, y, w, h = track_window
img2 = cv2.rectangle(img, pt1=(x, y), pt2=(x+w, y+h), color=(0, 0, 255), thickness=5)
img_show("window", img2, position=(
                bbox[0]*2-bbox[2], bbox[1]-30), size=(bbox[2]-bbox[0], bbox[3]-bbox[1]))
