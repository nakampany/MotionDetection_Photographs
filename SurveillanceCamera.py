#http://qiita.com/Algebra_nobu/items/a488fdf8c41277432ff3
import cv2
import os
import time
import datetime as dt
from time import sleep


#人の認識
u_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_upperbody.xml')


# カメラの起動
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
cap.set(cv2.CAP_PROP_FPS,5)

anterior = 0
shot_dense = 0.5
considerable_frames = 20
prev_faces = []
prev_shot = None


count=0
##カレントディレクトリのパスを取得
current = os.getcwd()
##ディレクトリ作成
now = dt.datetime.now()
dir_name = "/IMG_{0:%m%d%H%M}".format(now)
if os.path.isdir(current + dir_name) == False:
    os.mkdir(current + dir_name)  #make directory
os.chdir(current + dir_name)  #move to directory
#フレーム数カウント用"""

while True:

    # 動画ストリームからフレームを取得
    ret, frame_color = cap.read()

    # 顔検出の処理効率化のために、写真の情報量を落とす（モノクロにする）
    frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
    
    #物体認識（上半身）の実行
    upperrect = u_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(1, 1))
    
    if len(upperrect) > 0:
        #frame_RGB = cv2.cvtColor(frame_color,cv2.COLOR_BGR2RGB)

        t=str(dt.datetime.now())
        #frame_RGB=cv2.putText(frame_RGB, t,(10,20), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1,cv2.LINE_AA)
        frame_color=cv2.putText(frame_color, t,(10,20), cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1,cv2.LINE_AA)

        filename = "IMG_{}.jpg".format(count)
        #cv2.imwrite(filename, frame_RGB)
        cv2.imwrite(filename, frame_color)
        count += 1
        print(count)
        time.sleep(1)
        

    # 表示
    cv2.imshow("Show FLAME Image", frame_color)

    # qを押したら終了。
    print("qを押して終了")
    k = cv2.waitKey(1)
    if k == ord('q'):
        break



cap.release()

cv2.destroyAllWindows()

