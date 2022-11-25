#!/usr/bin/python3

import cv2
import numpy as np
import platform
import time
import datetime as dt
import sys
import os

def check_camera_connection():
    """
    接続されているカメラをチェック
    """

    print('接続されているカメラの番号を調べています...')
    true_camera_is = []  # 空の配列を用意
    cam_number = []

    # カメラ番号を0～9まで変えて、COM_PORTに認識されているカメラを探す
    for camera_number in range(0, 10):
        try:
            cap = cv2.VideoCapture(camera_number)
            ret, frame = cap.read()
        except:
            ret = False
        if ret == True:
            true_camera_is.append(camera_number)
            print("カメラ番号->", camera_number, "接続済")

            cam_number.append(camera_number)
        else:
            print("カメラ番号->", camera_number, "未接続")
    print("接続されているカメラは", len(true_camera_is), "台です。")
    print("カメラのインデックスは", true_camera_is,"です。")
    sys.exit("カメラ番号を調べ終わりました。")
    return 0


camera_auto_setting = "n" # FPSと解像度を自動的に設定
camera_mirror = "n"       # 反転して映る際はyesに変更      
show_version = "y"        # pythonとopencvのバージョンを確認する場合はyes
save_fig = "n"            # 静止画保存
imshow = "y"              # キャプチャー画像を見る場合はyes
calibration = "n"         # センターキャリブレーション
rotation = "y"            # キャプチャ画像を回転
camera_check = "n"        # 接続されているカメラの番号を調べる

# 各定数定義
FPS = 40
size_X = 640
size_Y = 480

disp_X = 640
disp_Y = 480

CAMERA_INDEX=0


# 撮影する画像を回転させる角度
# ラジアンではなく，角度(°)ディグリー
ANGLE = 0

# 拡大比率
SCALE = 1.0
size = ( size_X , size_Y )
disp_size = (disp_X , disp_Y )

if camera_check == "y":
    check_camera_connection()

save_video=input('# 録画しますか(y/n default=y)')
if save_video=='':
    save_video = "y"
if save_video=='y':
    filename = 'out.mp4'
    while os.path.exists(filename):
        print("# %sはすでに存在しています．" % filename)
        filename = input('## 新しい出力ファイル名:')
        filename = filename + '.mp4'
    print('%s に動画を書き出します．' % filename)
     # 動画保存用設定
    cap_now = dt.datetime.now()
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # 動画保存時のfourcc設定（mp4用）
    video = cv2.VideoWriter(filename, fourcc, fps, (width, hight))  
    # 動画の仕様（ファイル名、fourcc, FPS, サイズ)




camera = cv2.VideoCapture(CAMERA_INDEX)#camera インスタンス生成
# 0:内蔵カメラ , -1:自動的にカメラが選択される
# 0以外の番号はcamera_check.pyで確認する．

# 動画ファイル保存用の設定
if camera_auto_setting == 'y':
    fps = int(camera.get(cv2.CAP_PROP_FPS))           # カメラのFPSを取得
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)) # カメラの横幅を取得
    hight = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))# カメラの縦幅を取得
else:
    fps = int(FPS)
    width = int(size_X)
    hight = int(size_Y)

# pythonとopencvのバージョンを確認
if show_version == "y":
    py_ver = str(platform.python_version_tuple())
    py_ver = py_ver.replace("'",'')
    py_ver = py_ver.replace(",",'.')
    py_ver = py_ver.replace("(",'')
    py_ver = py_ver.replace(")",'')
    py_ver = py_ver.replace(" ",'')
    print("Python3のバージョン： ",end="")
    print(py_ver)
    print("opencvのバージョン： ",end="")
    print(cv2.__version__)




# トリミングする際の幅,高さを計算
triming_range = 100
triming_start_x = (width//2) - (triming_range//2)
triming_start_y = (hight//2) - (triming_range//2)



print(" fps= %d " % fps , end="" )
print(" width= %d " % width , end="" )
print(" hight= %d" % hight )
size = ( width , hight )
now = time.time()
start = now
count = 0


while True:
    ret, frame = camera.read()
    if camera_mirror == "y":
        frame = frame[:,::-1]

    if save_fig == "y":
        cap_time = dt.datetime.now()
        cap_time = str(cap_time.strftime('%y%m%d_%H%M%S'))
        cap_time = cap_time.replace("'",'')
        picname = cap_time+".png"
        cv2.imwrite(picname, frame)

    if save_video == "y":
        video.write(frame)
    if rotation == "y":
         #回転させる処理
        center2 = tuple(np.array([frame.shape[1] * 0.5, frame.shape[0] * 0.5]))
        rotation_matrix = cv2.getRotationMatrix2D(center2, ANGLE, SCALE)
        frame = cv2.warpAffine(frame, rotation_matrix, size, flags=cv2.INTER_CUBIC)
    if calibration == "y":
         #キャプチャ画像のセンターを表示する処理
        frame = frame[triming_start_x:triming_start_x + triming_range , triming_start_y:triming_start_y + triming_range]
        frame = cv2.resize(frame, disp_size)
    if imshow == "y":
        cv2.imshow("camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    count = count + 1       
    now = time.time()
rate=count/(now-start)
speed=1.0/rate*1000
print("rate=%5.2f (Hz)" % rate)
print("speed=%5.2f (msec)" % speed)
camera.release()
cv2.destroyAllWindows()