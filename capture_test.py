import cv2


def main():
    # VideoCaptureの引数にはdeviceのインデックスを指定
    avg = None
    cap = cv2.VideoCapture(1)
    if cap.isOpened() is False:
        print("cannot open video capture.")
        return

    cv2.namedWindow("capture", cv2.WINDOW_NORMAL)
    print("press any key to stop")
    while(True):
        ret, frame = cap.read()
        #動体検知処理
        #グレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 比較用にフレームの切り出し保存
        if avg is None:
            avg = gray.copy().astype("float")
            continue

        #現在のフレームと移動平均との差を計算
        cv2.accumulateWeighted(gray, avg, 0.8)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

        #画像を２値化する
        thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]

        #輪郭を抽出する
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        # 差分があった点を画面に描く
        for target in contours:
            x, y, w, h = cv2.boundingRect(target)

            if w < 30: continue #条件以下の変更点は除外

            #動体の位置を描画
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 2)

        #画像表示
        cv2.imshow("capture", frame)
        key = cv2.waitKey(1)
        if key is not -1:
            break
    return


if __name__ == "__main__":
    main()
