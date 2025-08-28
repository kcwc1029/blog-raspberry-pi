## 1. 在樹梅派上安裝opencv
建立虛擬環境
```
mkvirtualenv --system-site-packages opencv_env
```

安裝OPENCV
```
pip install opencv-python
sudo apt install -y qtwayland5 libqt5gui5 libqt5widgets5 libqt5core5a libegl1-mesa libgles2-mesa

```

補上路徑變數（後續使用imshow會需要用到pyQt5）
```
echo 'export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/arm-linux-gnueabihf/qt5/plugins/platforms' >> ~/.bashrc
source ~/.bashrc
```

查看是否安裝完成
```python
import cv2
print(cv2.__version__)
```

### 1.1. Lab：讀取圖片與顯示
要在VNC中去執行歐
```python
import cv2

img = cv2.imread("./cat_reach_deal.jpg")
cv2.imshow("image name", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
imread可以使用第2個參數來指定3種讀取格式

|模式名稱|說明|特點|
|---|---|---|
|`cv2.IMREAD_COLOR`|以**彩色模式**讀取圖片|預設值，不透明圖也會忽略透明通道|
|`cv2.IMREAD_GRAYSCALE`|以**灰階模式**讀取圖片|把圖片變成單一通道（黑白影像）|
|`cv2.IMREAD_UNCHANGED`|**完整讀取**圖片|包含透明通道（例如PNG的Alpha通道）|

### 1.2. Lab：讀取圖片與顯示
```python
import cv2

img = cv2.imread("./cat_reach_deal.jpg")
img1 = cv2.imread("./cat_reach_deal.jpg", cv2.IMREAD_GRAYSCALE)
print(img.shape)
print(img1.shape)
height, weight, color = img.shape
cv2.destroyAllWindows()
```

### 1.3. Lab：調整圖片尺寸
opencv內建的ewsize()會更改圖片本身比例，因此可以透過imutils模組
```
安裝
pip install imutils
```
```python
import cv2
import imutils

img = cv2.imread("./cat_reach_deal.jpg")
print(img.shape)
resized_img = imutils.resize(img, width=300)
print(resized_img.shape)
cv2.imshow("Koala", img)
cv2.imshow("Koala:resized", resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

![upgit_20250417_1744877026.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250417_1744877026.png)


### 1.4. Lab：旋轉、翻轉、位移圖片
opencv內建的ewsize()會更改圖片本身比例，因此可以透過imutils模組
```python
import cv2
import imutils

img = cv2.imread("./cat_reach_deal.jpg")
img = imutils.resize(img, width=200)

# 選轉
rotated_img = imutils.rotate(img, angle=90)
cv2.imshow("Koala:rotated", rotated_img)

# 翻轉
fliped_img = cv2.flip(img, -1)
cv2.imshow("Koala:fliped", fliped_img)

# 平移
translated_img = imutils.translate(img, 25, -75)
cv2.imshow("Koala:translated", translated_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
```


![upgit_20250421_1745221850.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250421_1745221850.png)


### 1.5. Lab：將圖片轉灰階、或RGB/BGR圖片
OpenCV 讀取圖片後，可以使用 cvtColor() 方法來轉換圖片色彩格式。
轉成灰階圖片：使用 cv2.COLOR_BGR2GRAY 參數。
imread() 預設讀進來是 BGR 格式（藍綠紅順序），如果要得到 RGB 格式（紅綠藍順序）
- 需要用 cv2.COLOR_BGR2RGB 做轉換。
- 相反地，cv2.COLOR_RGB2BGR 是將 RGB 轉回 BGR。

```python
import cv2
import imutils

img = cv2.imread("./cat_reach_deal.jpg")
img = imutils.resize(img, width=200)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.imshow("Koala:gray", gray_img)
cv2.imshow("Koala:rgb", rgb_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

![upgit_20250421_1745222078.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250421_1745222078.png)



### 1.6. Lab：從url中讀取圖片
```python
import cv2
import imutils


url = "https://i.pinimg.com/236x/e2/f1/88/e2f1885490d77b56201ef3ceb5220328.jpg"
img = imutils.url_to_image(url)
img = imutils.resize(img, width=200)

print(img.shape)
cv2.imshow("Koala:rgb", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

![upgit_20250421_1745222356.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250421_1745222356.png)


### 1.7. Lab：註記圖片
|函式|功能|參數簡介|
|---|---|---|
|`cv2.line()`|畫線|起點座標、終點座標、顏色、線寬|
|`cv2.rectangle()`|畫矩形|左上角座標、右下角座標、顏色、線寬|
|`cv2.circle()`|畫圓|圓心座標、半徑、顏色、線寬|
|`cv2.ellipse()`|畫橢圓|圓心、長短軸長度、旋轉角度、起始角、結束角、顏色、線寬|
|`cv2.putText()`|加文字|文字內容、起點座標、字型、大小、顏色、線寬、線條種類|
```python
cv2.line(img, (0, 0), (200, 200), (0, 255, 255), 5)  # 畫一條黃色粗線
cv2.rectangle(img, (20, 20), (120, 100), (0, 255, 0), 2)  # 畫綠色矩形框
cv2.rectangle(img, (140, 40), (180, 100), (255, 0, 0), -1)  # 畫藍色填滿矩形
cv2.circle(img, (300, 100), 40, (0, 0, 255), -1)  # 畫紅色填滿圓形
cv2.putText(img, "Koala", (10, 40), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 5, cv2.LINE_AA)  # 加黃色文字
```

```python
import cv2
import imutils


url = "https://i.pinimg.com/236x/e2/f1/88/e2f1885490d77b56201ef3ceb5220328.jpg"
img = imutils.url_to_image(url)
img = imutils.resize(img, width=300)

# 標記
cv2.line(img, (0,0), (200,200), (0,0,255), 5)
cv2.rectangle(img, (20,70), (120,160), (0,255,0), 2)
cv2.rectangle(img, (40,80), (100,140), (255,0,0), -1)
cv2.circle(img,(90,210), 30, (0,255,255), 3)
cv2.circle(img,(140,170), 15, (255,0,0), -1)
cv2.putText(img, 'OpenCV', (10, 40),cv2.FONT_HERSHEY_SIMPLEX,1, (0,255,255), 5, cv2.LINE_AA)

# 寫入圖檔
cv2.imwrite("結果圖片.jpg", img)
```
![upgit_20250421_1745222685.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250421_1745222685.png)


### 1.8. Lab：讀取影片/webcam
```python
import cv2

cap = cv2.VideoCapture('../download')

while(cap.isOpened()):
  ret, frame = cap.read()
  if ret:
      cv2.imshow('frame',frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
```

## 2. OpenCV 哈爾特徵／層級式分類器
哈爾特徵層級式分類器屬於電腦視覺物體偵測技術的一種。本質屬於物體偵測（Object Detection）的一種特例（專門偵測特定物件）。

基本概念
- 哈爾特徵（Haar Features）：使用直線邊界、中心區域等局部特徵來判斷區域內是否有特定物體。
- 特徵提取：在滑動窗口中計算特徵值，用來檢查該區域是否含有目標物體。

層級式分類器（Cascade Classifier）
- 偵測特徵很多，假設每個窗格要比對 6000 個特徵，太慢且效率低。
- 解決方法：  
  ➔ 把大量特徵分組成多層次的弱分類器，每層專注不同特徵。
  ➔ 只有通過第一層，才進到第二層……一路過濾到最後，才能確定偵測到目標（例如一張臉）。
- 層級式分類器的運作流程
	- 每一層是弱分類器，即判斷力弱但速度快。
	- 採用 boosting 技術（提升方法）：
		- 把一層一層的弱分類器組合起來，增強整體判斷效果。
		- 錯誤率會逐層下降，最後有效偵測出物體（如臉）。


### 2.1. openCV 分類器模型(網路上以訓練好)
連結：https://github.com/opencv/opencv/tree/master/data

|名稱|作用|說明|
|---|---|---|
|`haarcascades/`|Haar 特徵分類器（一般版）|裡面有很多 `.xml` 檔，像是 `haarcascade_frontalface_default.xml`，拿來做人臉偵測。|
|`haarcascades_cuda/`|Haar 特徵分類器（CUDA加速版）|給有支援 CUDA（NVIDIA GPU）的人用，加速偵測。|
|`hogcascades/`|HOG 特徵分類器|用 HOG（Histogram of Oriented Gradients）特徵來做物體偵測，適合偵測人或車子。|
|`lbpcascades/`|LBP 特徵分類器|使用 LBP（Local Binary Pattern）特徵，比 Haar 快，常拿來做人臉偵測，速度快但稍微沒那麼準。|
|`vec_files/`|訓練資料樣本（.vec 檔）|是拿來自己訓練 cascade 分類器的資料，不是模型。進階才會用。|
|`CMakeLists.txt`|CMake 設定檔|讓 OpenCV 編譯時能找到這些資料（不用管它，開發者用的）。|
|`readme.txt`|說明文件|簡單介紹這個資料夾的用途。|


### 2.2. Lab：圖片內容人臉偵測
```python
import requests
import cv2

def download_xml(url, save_path):
    response = requests.get(url)
    # 確認下載成功
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"檔案已經下載並儲存到：{save_path}")
    else:
        print(f"下載失敗，錯誤代碼：{response.status_code}")


def main():
    url = "https://raw.githubusercontent.com/opencv/opencv/refs/heads/master/data/haarcascades_cuda/haarcascade_frontalface_alt.xml" # GitHub 上的檔案 "Raw" 連結
    save_path = "haarcascade_frontalface_alt.xml" # 儲存到本機的檔案路徑

    download_xml(url, save_path)
    faceCascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml")

    image = cv2.imread("./image02.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 從圖片偵測人臉
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(30, 30)
    )

    print("人臉數:", len(faces))

    # 在偵測出的人臉繪出長方形外框
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 寫入圖檔
    cv2.imwrite("結果圖片.jpg", image)
    # cv2.imshow("preview", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
```
![upgit_20250421_1745231230.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250421_1745231230.png)


### 2.3. Lab：即時影像人臉偵測

```python
import requests
import cv2

def download_xml(url, save_path):
    response = requests.get(url)
    # 確認下載成功
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"檔案已經下載並儲存到：{save_path}")
    else:
        print(f"下載失敗，錯誤代碼：{response.status_code}")


def main():
    url = "https://raw.githubusercontent.com/opencv/opencv/refs/heads/master/data/haarcascades_cuda/haarcascade_frontalface_alt.xml" # GitHub 上的檔案 "Raw" 連結
    save_path = "haarcascade_frontalface_alt.xml" # 儲存到本機的檔案路徑
    download_xml(url, save_path)

    faceCascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml")

    cap = cv2.VideoCapture(0) 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        print("人臉數:", len(faces))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("preview", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
```

## 3. YOLO物體偵測

### 3.1. 深度學習（Deep Learning）

深度學習是一種機器學習技術，模仿人類大腦神經元（Neuron）傳輸訊息的方式，建立神經網路架構（Neural Network Architectures）。
    
神經網路基本結構：
- 輸入層（Input Layer）：負責接收輸入資料。
- 隱藏層（Hidden Layers）：中間層，負責進行特徵提取與學習。
- 輸出層（Output Layer）：輸出最終結果。

多層神經網路（Deep Neural Networks, DNN）：
- 特點：有很多層隱藏層（可以超過150層），稱為「深度」。
- 深度神經網路使得模型能夠學習更複雜的資料特徵。
### 3.2. 物體偵測（Object Detection）
- **定義**：物體偵測是在數位影像中找出物體的位置和類型。
- **典型應用**：偵測人、車輛、椅子、石頭、建築物、動物等。
- **物體偵測要回答的兩個問題**：
    1. 這是什麼東西？（分類）
    2. 東西在哪裡？（定位）
- 其他常見物體偵測技術（YOLO以外）：Fast R-CNN、Retina-Net、SSD（Single-Shot MultiBox Detector）

### 3.3. YOLO（You Only Look Once）：物體偵測的深度學習演算法
官方網站：https://pjreddie.com/darknet/yolo/
是一種**快速且準確**的物體偵測（Object Detection）演算法。
屬於**深度學習演算法**的一種。
特性：
- 使用**深度學習**的**卷積神經網路（Convolutional Neural Networks, CNN）**架構。
- 只需一次**前向傳播（Forward Propagation）**就可以偵測出影像中的多個物體。
- 相較於傳統方法，YOLO極大提升了偵測速度與效率。

 YOLO 常見的框架

| 框架           | 說明                                                                               |
| ------------ | -------------------------------------------------------------------------------- |
| **Darknet**  | 原開發者推出的深度學習框架，效率高，支援 CPU 和 GPU，但**僅支援 Linux 系統**。                                |
| **Darkflow** | 將 Darknet 改寫成 TensorFlow 版本（Google開發的深度學習框架），支援 Linux / Windows（新版已不支援GPU）和 Mac。 |
| **OpenCV**   | OpenCV 提供執行 YOLO 的深度學習模組，可直接在 OpenCV 上執行，不需額外安裝框架，但目前僅支援 CPU，不支援 GPU 運算。         |

### 3.4. Lab：在openCV上使用YOLOv8n
```
pip install torch torchvision
pip install ultralytics
```
```python
from ultralytics import YOLO
import cv2

# 載入 yolov8n 模型
model = YOLO('yolov8n.pt')

# 用 webcam 做即時偵測
model.predict(source=1, show=True)
```


### 3.5. Lab：使用YOLOv11n物體偵測
官網：https://docs.ultralytics.com/zh/models/yolo11/#supported-tasks-and-modes（他有五種可以玩玩看）

![upgit_20250422_1745253053.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250422_1745253053.png)



```
pip install torch torchvision
pip install ultralytics
```

```python
from ultralytics import YOLO

# 載入官方訓練好的 YOLOv11n
model = YOLO("yolo11n.pt")

# 使用 webcam
model.predict(source=1, show=True)
```

### 3.6. Lab：使用YOLOv11n影像分割
```
pip install torch torchvision
pip install ultralytics
```

```python
from ultralytics import YOLO

# 載入官方訓練好的 YOLOv11n
model = YOLO("yolo11n.pt")

# 使用 webcam
model.predict(source=1, show=True)
```
### 3.7. Lab：使用YOLOv11n姿態評估
```
pip install torch torchvision
pip install ultralytics
```



















