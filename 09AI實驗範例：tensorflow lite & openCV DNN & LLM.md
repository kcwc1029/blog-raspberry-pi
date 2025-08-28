### 0.1. Lab：在數枚派上安裝ollama
```
curl -fsSL https://ollama.com/install.sh  | sh
ollama --version

# 使用tinyLlama(4GB樹梅派)
ollama run tinyllama

# 使用gemms2:2B(4GB樹梅派)
ollama run gemma2:2b

# 使用phi3(8GB樹梅派)
ollama run phi3

# 使用llama3(8GB樹梅派)
ollama run llama3
```
### 0.2. EasyOCR 的車牌辨識（基於 PyTorch）
EasyOCR 是什麼？
- 一套基於深度學習的文字偵測與辨識工具
- 支援超過 70 種語言
- 內建模型支援常見語言與場景，使用 PyTorch 架構

```python
# 建立虛擬環境
mkvirtualenv --system-site-packages ocr

# 安裝 EasyOCR（包含依賴）
pip install easyocr
# 這會同時安裝 opencv-python-headless，但若你需要使用 OpenCV 的 GUI 功能（如 cv2.imshow()），需另外安裝完整版本。

#  若需完整 GUI OpenCV 顯示介面：替換 opencv-python-headless
pip uninstall opencv-python-headless
pip install opencv-python
```

```python
import easyocr
import numpy as np
import cv2
 
img = cv2.imread("images/car.jpg")
reader = easyocr.Reader(["en"])
result = reader.readtext(img)
y = 0
for box in result:
    points = box[0]
    points = np.array(points, np.int32)
    print(points)
    print(box[1])
    cv2.polylines(img, pts=[points], isClosed=True,
                  color=(0, 0, 255), thickness=3)
    y = y + 30
    cv2.putText(img, box[1], (10, y),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    
cv2.imshow("Car", img) 
cv2.waitKey(0)
cv2.destroyAllWindows()
```








