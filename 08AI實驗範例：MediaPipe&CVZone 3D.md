## 1. Google MediaPipe 機器學習框架
官方網址：[MediaPipe Solutions](https://ai.google.dev/edge/mediapipe/solutions/)
**Google MediaPipe** 是 Google 公司於 **2019 年**推出的開源機器學習框架。
主要針對 **電腦視覺（Computer Vision）** 領域，提供快速且跨平台的解決方案。
用 **機器學習管線（ML Pipeline）** 的概念，來處理複雜任務。
    
### 1.1. 機器學習管線（ML Pipeline）
機器學習管線：一個讓系統自動化產生 ML 模型的作業流程。
類似「系統開發生命週期（SDLC）」的概念，但是針對機器學習的版本。
特點：強調版本控制、自動測試、反覆迭代（Iterative Cycle）。
涉及步驟：
- 資料蒐集
- 資料預處理
- 模型訓練與評估

### 1.2. Lab：在樹莓派安裝 MediaPipe
```bash
pip install mediapipe==0.10.14
```
### 1.3. Lab：MediaPipe圖片人臉偵測



基礎模型：使用 BlazeFace 模型
- 由 Google 自行開發
- 基於 Single Shot Detector (SSD) 架構，針對移動裝置與輕量級應用優化設計
功能特點：
- 超快速偵測人臉
- 模型輕量、運算速度快
- 可以在圖片或影片中偵測出多張人臉
- 同時標示出每張人臉的6個關鍵點（Key Points）

MediaPipe 人臉偵測回傳資料
- 偵測到的人臉的矩形範圍座標（bounding box）
- 偵測到的人臉上的6個關鍵點座標：左眼、右眼、鼻尖、嘴巴、左耳、右耳


```python
import cv2
import mediapipe as mp

# 初始化 MediaPipe 模組
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(
                      min_detection_confidence=0.5)

# 讀取圖片
img = cv2.imread("./image03.png")
if img is None:
    print("圖片讀取失敗，請檢查路徑！")
    exit()

# 偵測人臉
results = face_detection.process(img)

# 畫出偵測結果
if results.detections:
    for detection in results.detections:
        mp_drawing.draw_detection(img, detection)

# 儲存圖片
cv2.imwrite("./resulted_image.jpg", img)
```


![upgit_20250422_1745331984.png|324x373](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250422_1745331984.png)

### 1.4. Lab：MediaPipe圖片臉部網格
```python
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)

img = cv2.imread("./image03.png")
results = face_mesh.process(img)
if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(image=img,
                   landmark_list=face_landmarks,
                   connections=mp_face_mesh.FACEMESH_CONTOURS,
                   landmark_drawing_spec=drawing_spec,
                   connection_drawing_spec=drawing_spec)


# 儲存圖片
cv2.imwrite("face_detected.jpg", img)
print("偵測後的圖片已儲存到 images/face_detected.jpg")
```


![upgit_20250422_1745332325.png|437x503](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250422_1745332325.png)

### 1.5. Lab：MediaPipe圖片手勢追蹤
```python
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5)

img = cv2.imread("./hand.jpg")
results = hands.process(img)
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

# 儲存圖片
cv2.imwrite("face_detected.jpg", img)
```

![upgit_20250422_1745334223.png|462x616](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250422_1745334223.png)

### 1.6. Lab：MediaPipe圖片人體姿態估計

![upgit_20250422_1745334255.png|450x310](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250422_1745334255.png)

```python
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5)
                    
img = cv2.imread("./pose01.jpg")
results = pose.process(img)
mp_drawing.draw_landmarks(
           img,
           results.pose_landmarks,
           mp_pose.POSE_CONNECTIONS)



# 儲存圖片
cv2.imwrite("face_detected.jpg", img)
```

![upgit_20250422_1745334386.png|233x350](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250422_1745334386.png)

## 2. CVZone 電腦視覺套件
🔗 官方網站：https://github.com/cvzone/cvzone

CVZone 是基於 OpenCV 和 MediaPipe 的 Python套件。
可以讓我們用更少的 Python 程式碼，快速完成影像處理和 AI 電腦視覺功能。 
 CVZone 可以做什麼？
- 臉部偵測
- 3D 臉部網格建立
- 姿勢偵測
- 手勢追蹤
- 人體姿態估計

### 2.1. 安裝 CVZone 步驟
要配合mediapipe版本
```
pip install mediapipe==0.10.14
pip install cvzone==1.6.1
```


### 2.2. Lab：CVZone偵測臉部網格

```python
from cvzone.FaceMeshModule import FaceMeshDetector
import cv2

detector = FaceMeshDetector(maxFaces=2)

img = cv2.imread("./face02.jpg")
img, faces = detector.findFaceMesh(img)
if faces:
    print(faces[0])


# 儲存圖片
cv2.imwrite("face_detected.jpg", img)
```

![upgit_20250423_1745412957.png|465x320](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250423_1745412957.png)


### 2.3. Lab：CVZone圖片多手勢追蹤

```python
from cvzone.HandTrackingModule import HandDetector  # 匯入 cvzone 的手部偵測模組
import cv2  # 匯入 OpenCV 做圖像處理

# 建立手部偵測器物件，設定偵測信心閾值為 0.5，最多偵測兩隻手
detector = HandDetector(detectionCon=0.5, maxHands=2)

# 讀取一張手部圖片
img = cv2.imread("./hand.jpg")

# 執行手部偵測，回傳偵測到的手部資訊與標註後的圖片
hands, img = detector.findHands(img)

# 如果有偵測到手
if hands:
    # 處理第一隻手的資訊
    hand1 = hands[0]  # 取出第一隻手的資料
    lmList1 = hand1["lmList"]  # 手部21個關鍵點座標（list of x,y,z）
    bbox1 = hand1["bbox"]  # 邊界框（x, y, w, h）
    centerPoint1 = hand1['center']  # 中心點座標
    handType1 = hand1["type"]  # 左手或右手（"Left" / "Right"）
    fingers1 = detector.fingersUp(hand1)  # 判斷哪幾根手指是伸直的，回傳一個5個元素的列表

    # 如果偵測到兩隻手
    if len(hands) == 2:
        hand2 = hands[1]  # 第二隻手
        lmList2 = hand2["lmList"]
        bbox2 = hand2["bbox"]
        centerPoint2 = hand2['center']
        handType2 = hand2["type"]
        fingers2 = detector.fingersUp(hand2)

        # 計算兩隻手的食指指尖（編號8）之間的距離
        length, info, img = detector.findDistance(
            lmList1[8][0:2],  # 第一隻手的食指指尖 (x, y)
            lmList2[8][0:2],  # 第二隻手的食指指尖 (x, y)
            img  # 傳入圖像用於畫線和標記
        )

# 將偵測結果的圖像儲存成檔案
cv2.imwrite("face_detected.jpg", img)
```

![upgit_20250423_1745413173.png|331x442](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250423_1745413173.png)


### 2.4. Lab：CVZone webcam多手勢追蹤

```python
from cvzone.HandTrackingModule import HandDetector
import cv2

# 啟用 webcam（0 代表預設攝影機）
cap = cv2.VideoCapture(0)

# 建立手部偵測器
detector = HandDetector(detectionCon=0.5, maxHands=2)

while True:
    success, img = cap.read()  # 讀取一幀影像
    if not success:
        break

    # 偵測手部
    hands, img = detector.findHands(img)

    # 如果有偵測到手
    if hands:
        # 手 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerPoint1 = hand1["center"]
        handType1 = hand1["type"]
        fingers1 = detector.fingersUp(hand1)

        # 如果有兩隻手
        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            centerPoint2 = hand2["center"]
            handType2 = hand2["type"]
            fingers2 = detector.fingersUp(hand2)

            # 計算兩隻手的食指指尖之間的距離
            length, info, img = detector.findDistance(
                lmList1[8][0:2], lmList2[8][0:2], img
            )

    # 顯示畫面
    cv2.imshow("Webcam Hand Tracking", img)

    # 按下 q 鍵離開
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源
cap.release()
cv2.destroyAllWindows()
```



![upgit_20250423_1745413486.png|534x477](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250423_1745413486.png)


### 2.5. Lab：CVZone webcam計算伸出幾根手指
```python
from cvzone.HandTrackingModule import HandDetector
import cv2

# 啟用 webcam，0 代表預設攝影機
cap = cv2.VideoCapture(1)

# 建立手部偵測器，只偵測 1 隻手
detector = HandDetector(detectionCon=0.5, maxHands=1)

while True:
    success, img = cap.read()  # 讀取一張影像
    if not success:
        break

    # 偵測手部
    hands, img = detector.findHands(img)
    
    if hands:
        hand = hands[0]  # 取得第一隻手的資料
        bbox = hand['bbox']  # 取得手的邊界框 [x, y, w, h]
        fingers = detector.fingersUp(hand)  # 判斷手指狀態，回傳5個元素的list
        totalFingers = fingers.count(1)  # 計算伸出的手指數量（1代表伸出）
        
        # 在手的上方顯示手指數量
        if bbox:
            cv2.putText(img, f'Fingers: {totalFingers}',
                        (bbox[0] + 100, bbox[1] - 30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # 顯示影像畫面
    cv2.imshow("CVZone Hand Detection", img)

    # 按下 q 離開
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源
cap.release()
cv2.destroyAllWindows()
```


![upgit_20250423_1745414153.png|493x441](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250423_1745414153.png)


### 2.6. Lab：CVZone webcam計算手指之間的距離

```python
from cvzone.HandTrackingModule import HandDetector
import cv2

# 啟用 webcam
cap = cv2.VideoCapture(1)

# 建立手部偵測器，最多偵測 2 隻手
detector = HandDetector(detectionCon=0.5, maxHands=2)

while True:
    success, img = cap.read()
    if not success:
        break

    # 偵測手部
    hands, img = detector.findHands(img)

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerPoint1 = hand1["center"]
        handType1 = hand1["type"]
        fingers1 = detector.fingersUp(hand1)

        # 計算大拇指 (4) 和食指 (8) 的距離
        length, info, img = detector.findDistance(
            lmList1[4][0:2], lmList1[8][0:2], img
        )

        # 顯示距離
        cv2.putText(img, f'Dist: {int(length)}',
                    (bbox1[0] + 50, bbox1[1] - 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # 顯示畫面
    cv2.imshow("CVZone Thumb-Index Distance", img)

    # 按下 q 鍵離開
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝影機與關閉視窗
cap.release()
cv2.destroyAllWindows()
```

![upgit_20250423_1745420531.png|483x418](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250423_1745420531.png)


### 2.7. Lab：CVZone圖片人體姿態估計

```python
from cvzone.PoseModule import PoseDetector
import cv2

detector = PoseDetector()

img = cv2.imread("./pose01.jpg")
img = detector.findPose(img)
lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)
if bboxInfo:
    center = bboxInfo["center"]
    cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)


# 儲存圖片
cv2.imwrite("face_detected.jpg", img)
```

![upgit_20250423_1745420782.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250423_1745420782.png)


### 2.8. Lab：CVZone圖片計算人體姿態的姿態的距離與角度
```python
from cvzone.PoseModule import PoseDetector
import cv2

# 建立姿勢偵測器 PoseDetector（內部基於 MediaPipe）
detector = PoseDetector()

# 讀取輸入圖像
img = cv2.imread("./pose.jpg")

# 偵測人體骨架姿勢，會繪製骨架在圖像上
img = detector.findPose(img)

# 取得所有關鍵點座標（lmList）與整體包覆框 bboxInfo
lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)

if bboxInfo:
    # 如果偵測到身體

    # ✳️ 計算左肩(11)到左手腕(15)之間的距離
    length, img, info = detector.findDistance(
        lmList[11][0:2],  # 第11點：左肩 (x, y)
        lmList[15][0:2],  # 第15點：左手腕 (x, y)
        img=img,          # 在圖像上畫線
        color=(255, 0, 0), # 線條顏色為藍色 (BGR)
        scale=10          # 線條寬度與圓圈大小比例
    )

    # ✳️ 計算左肩(11)、左手肘(13)、左手腕(15)之間的夾角
    angle, img = detector.findAngle(
        lmList[11][0:2],  # 左肩
        lmList[13][0:2],  # 左手肘
        lmList[15][0:2],  # 左手腕
        img=img,          # 在圖像上畫出角度
        color=(0, 0, 255), # 線條顏色為紅色
        scale=10
    )

    # ✳️ 檢查角度是否接近 50 度（容許誤差 ±10）
    isCloseAngle50 = detector.angleCheck(
        myAngle=angle,       # 當前角度
        targetAngle=50,      # 目標角度
        offset=10            # 誤差範圍 ±10
    )

    # 印出距離和角度是否接近目標角度
    print(length, isCloseAngle50)

# 儲存加上骨架與角度標示後的圖片
cv2.imwrite("face_detected.jpg", img)

```
![upgit_20250423_1745423563.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250423_1745423563.png)



### 2.9. Lab：從 2D 圖片偵測人體姿勢 → 轉為 3D 骨架
共兩個檔案
```python
# Pose3D.py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plotPose3D(lmList):
    face_index_list = [8, 6, 5, 4, 0, 1, 2, 3, 7]
    mouth_index_list = [9, 10]
    right_arm_index_list = [11, 13, 15, 17, 19, 15, 21]
    left_arm_index_list = [12, 14, 16, 18, 20, 16, 22]
    right_body_side_index_list = [11, 23, 25, 27, 29, 31, 27]
    left_body_side_index_list = [12, 24, 26, 28, 30, 32, 28]
    shoulder_index_list = [11, 12]
    waist_index_list = [23, 24]

    # 眼耳鼻 - 臉部
    face_x, face_y, face_z = [], [], []
    for index in face_index_list:
        point = lmList[index]
        face_x.append(point[0])
        face_y.append(point[1])
        face_z.append(point[2])
    
    # 嘴巴   
    mouth_x, mouth_y, mouth_z = [], [], []
    for index in mouth_index_list:
        point = lmList[index]
        mouth_x.append(point[0])
        mouth_y.append(point[1])
        mouth_z.append(point[2])
    
    # 右手
    right_arm_x, right_arm_y, right_arm_z = [], [], []
    for index in right_arm_index_list:
        point = lmList[index]
        right_arm_x.append(point[0])
        right_arm_y.append(point[1])
        right_arm_z.append(point[2])

    # 左手
    left_arm_x, left_arm_y, left_arm_z = [], [], []
    for index in left_arm_index_list:
        point = lmList[index]
        left_arm_x.append(point[0])
        left_arm_y.append(point[1])
        left_arm_z.append(point[2])

    # 右半身
    right_body_side_x, right_body_side_y, right_body_side_z = [], [], []
    for index in right_body_side_index_list:
        point = lmList[index]
        right_body_side_x.append(point[0])
        right_body_side_y.append(point[1])
        right_body_side_z.append(point[2])

    # 左半身
    left_body_side_x, left_body_side_y, left_body_side_z = [], [], []
    for index in left_body_side_index_list:
        point = lmList[index]
        left_body_side_x.append(point[0])
        left_body_side_y.append(point[1])
        left_body_side_z.append(point[2])

    # 肩
    shoulder_x, shoulder_y, shoulder_z = [], [], []
    for index in shoulder_index_list:
        point = lmList[index]
        shoulder_x.append(point[0])
        shoulder_y.append(point[1])
        shoulder_z.append(point[2])

    # 腰
    waist_x, waist_y, waist_z = [], [], []
    for index in waist_index_list:
        point = lmList[index]
        waist_x.append(point[0])
        waist_y.append(point[1])
        waist_z.append(point[2])
            
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ax.scatter(face_x, face_y, face_z)
    ax.plot(mouth_x, mouth_y, mouth_z)
    ax.plot(right_arm_x, right_arm_y, right_arm_z)
    ax.plot(left_arm_x, left_arm_y, left_arm_z)
    ax.plot(right_body_side_x, right_body_side_y, right_body_side_z)
    ax.plot(left_body_side_x, left_body_side_y, left_body_side_z)
    ax.plot(shoulder_x, shoulder_y, shoulder_z)
    ax.plot(waist_x, waist_y, waist_z)

    ax.view_init(elev=300, azim=330, roll=300)   # 指定視角
    ax.set_box_aspect([1, 1, 1])                 # 指定x, y, z的比例
    # plt.savefig("pose_landmark.png") 
    plt.show()
```

```python
# main.py
from cvzone.PoseModule import PoseDetector
from Pose3D import plotPose3D
import cv2

detector = PoseDetector()

img = cv2.imread("./pose.jpg")
img = detector.findPose(img)
lmList, bboxInfo = detector.findPosition(img, draw=False, bboxWithHands=False)
if lmList:
    print("lmList =", lmList)
    for index, lm in enumerate(lmList):
        print(index, lm)
    plotPose3D(lmList) 
    
```



![upgit_20250424_1745424263.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250424_1745424263.png)


### 2.10. AI辨識猜拳
共兩個檔案

```python
# HandTrackingModule.py
"""
Hand Tracking Module
By: Computer Vision Zone
Website: https://www.computervision.zone/
"""

import math

import cv2
import mediapipe as mp


class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """

    def __init__(self, staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5):

        """
        :param mode: In static mode, detection is done on each image: slower
        :param maxHands: Maximum number of hands to detect
        :param modelComplexity: Complexity of the hand landmark model: 0 or 1.
        :param detectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """
        self.staticMode = staticMode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.staticMode,
                                        max_num_hands=self.maxHands,
                                        model_complexity=modelComplexity,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                ## lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                ## bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                ## draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2)
                    cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)

        return allHands, img

    def fingersUp(self, myHand):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        :return: List of which fingers are up
        """
        fingers = []
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:

            # Thumb
            if myHandType == "Right":
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img=None, color=(255, 0, 255), scale=5):
        """
        Find the distance between two landmarks input should be (x1,y1) (x2,y2)
        :param p1: Point1 (x1,y1)
        :param p2: Point2 (x2,y2)
        :param img: Image to draw output on. If no image input output img is None
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """
        if len(p1) == len(p2) == 3:
            # Get the landmarks
            x1, y1 = p1[0:2]
            x2, y2 = p2[0:2]
        else:
            x1, y1 = p1
            x2, y2 = p2

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), scale, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), scale, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, max(1, scale // 3))
            cv2.circle(img, (cx, cy), scale, color, cv2.FILLED)

        return length, img, info

    def findDistance3D(self, p1, p2, img=None, color=(255, 0, 255), scale=5):
        """
           Find the distance between two landmarks input should be (x1,y1,z1) (x2,y2,z2)
           :param p1: Point1 (x1,y1,z1)
           :param p2: Point2 (x2,y2,z2)
           :param img: Image to draw output on. If no image input output img is None
           :return: Distance between the points
                    Image with output drawn
                    Line information
           """
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        info = (x1, y1, x2, y2, cx, cy)

        if img is not None:
            cv2.line(img, (x1, y1), (x2, y2), color, max(1, scale // 3))
            cv2.circle(img, (x1, y1), scale, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), scale, color, cv2.FILLED)
            cv2.circle(img, (cx, cy), scale, color, cv2.FILLED)

        return length, img, info

    def findAngle(self,p1, p2, p3, img=None, color=(255, 0, 255), scale=5):
        """
        Finds angle between three points.

        :param p1: Point1 - (x1,y1,z1)
        :param p2: Point2 - (x2,y2,z2)
        :param p3: Point3 - (x3,y3,z3)
        :param img: Image to draw output on. If no image input output img is None
        :return:
        """
        angle, img = self.findAngle3D(p1[0:2], p2[0:2], p3[0:2],
                                      img=img,
                                      color=color,
                                      scale=scale)
        return angle, img

    def findAngle3D(self, point_a, point_b, point_c, img=None, color=(255, 0, 255), scale=5):
        """
        Finds angle between three points.

        :param point_a: Point1 - (x1,y1,z1)
        :param point_b: Point2 - (x2,y2,z2)
        :param point_c: Point3 - (x3,y3,z3)
        :param img: Image to draw output on. If no image input output img is None
        :return:   
        """
        a_x, b_x, c_x = point_a[0], point_b[0], point_c[0]  # a、b、c三個點的x座標
        a_y, b_y, c_y = point_a[1], point_b[1], point_c[1]  # a、b、c三個點的y座標

        if len(point_a) == len(point_b) == len(point_c) == 3:
            a_z, b_z, c_z = point_a[2], point_b[2], point_c[2]  # a、b、c三個點的z座標
        else:
            a_z, b_z, c_z = 0,0,0  # 因為是二維座標, 所以z軸都為0

        # 向量 m=(x1,y1,z1), n=(x2,y2,z2)
        x1,y1,z1 = (a_x-b_x),(a_y-b_y),(a_z-b_z)
        x2,y2,z2 = (c_x-b_x),(c_y-b_y),(c_z-b_z)

        # 計算角度
        cos_b = (x1*x2 + y1*y2 + z1*z2) / (math.sqrt(x1**2 + y1**2 + z1**2) *(math.sqrt(x2**2 + y2**2 + z2**2))) 
        angle = math.degrees(math.acos(cos_b))
        
        # Draw
        if img is not None:
            cv2.line(img, (a_x, a_y), (b_x, b_y), (255, 255, 255), max(1,scale//5))
            cv2.line(img, (c_x, c_y), (b_x, b_y), (255, 255, 255), max(1,scale//5))
            cv2.circle(img, (a_x, a_y), scale, color, cv2.FILLED)
            cv2.circle(img, (a_x, a_y), scale+5, color, max(1,scale//5))
            cv2.circle(img, (b_x, b_y), scale, color, cv2.FILLED)
            cv2.circle(img, (b_x, b_y), scale+5, color, max(1,scale//5))
            cv2.circle(img, (c_x, c_y), scale, color, cv2.FILLED)
            cv2.circle(img, (c_x, c_y), scale+5, color, max(1,scale//5))
            cv2.putText(img, str(int(angle)), (b_x - 50, b_y + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, color, max(1,scale//5))
        
        return angle, img

    def angleCheck(self, myAngle, targetAngle, offset=20):
        return targetAngle - offset < myAngle < targetAngle + offset


def main():
    # Initialize the webcam to capture video
    # The '2' indicates the third camera connected to your computer; '0' would usually refer to the built-in camera
    cap = cv2.VideoCapture(0)

    # Initialize the HandDetector class with the given parameters
    detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

    # Continuously get frames from the webcam
    while True:
        # Capture each frame from the webcam
        # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
        success, img = cap.read()

        # Find hands in the current frame
        # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
        # The 'flipType' parameter flips the image, making it easier for some detections
        hands, img = detector.findHands(img, draw=True, flipType=True)

        # Check if any hands are detected
        if hands:
            # Information for the first hand detected
            hand1 = hands[0]  # Get the first hand detected
            lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
            bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
            center1 = hand1['center']  # Center coordinates of the first hand
            handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

            # Count the number of fingers up for the first hand
            fingers1 = detector.fingersUp(hand1)
            print(f'H1 = {fingers1.count(1)}', end=" ")  # Print the count of fingers that are up

            # Calculate distance between specific landmarks on the first hand and draw it on the image
            length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),
                                                      scale=10)

            # Check if a second hand is detected
            if len(hands) == 2:
                # Information for the second hand
                hand2 = hands[1]
                lmList2 = hand2["lmList"]
                bbox2 = hand2["bbox"]
                center2 = hand2['center']
                handType2 = hand2["type"]

                # Count the number of fingers up for the second hand
                fingers2 = detector.fingersUp(hand2)
                print(f'H2 = {fingers2.count(1)}', end=" ")

                # Calculate distance between the index fingers of both hands and draw it on the image
                length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0),
                                                          scale=10)

            print(" ")  # New line for better readability of the printed output

        # Display the image in a window
        cv2.imshow("Image", img)

        # Keep the window open and update it for each frame; wait for 1 millisecond between frames
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
```

```python
# main.py
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.5, maxHands=1)

while cap.isOpened():
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        bbox = hand["bbox"]        
        fingers = detector.fingersUp(hand)
        totalFingers = fingers.count(1)
        print(totalFingers)
        msg = "None"
        if totalFingers == 5:
            msg = "Paper"
        if totalFingers == 0:
            msg = "Rock"
        if totalFingers == 2:
            if fingers[1] == 1 and fingers[2] == 1:
                msg = "Scissors"
        cv2.putText(img, msg, (bbox[0]+200,bbox[1]-30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.imshow("CVZone Hand Detector", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
        
cap.release()
cv2.destroyAllWindows()
```


![upgit_20250424_1745425150.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250424_1745425150.png)
