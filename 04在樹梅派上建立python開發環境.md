## 1. 在樹梅派上建立 python 虛擬環境

查看 python

```
raspberrypi@raspberrypi:~ $ python3 --version
Python 3.11.2
```

確認 Python 安裝路徑

```
raspberrypi@raspberrypi:~ $ which python3.11
/usr/bin/python3.11
```

如果需要設定環境變數

```
# 範例：設定環境變數VIRTUALENVWRAPPER_PYTHON = /usr/bin/python3.11
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.11" >> ~/.bashrc
source ~/.bashrc
```

### 1.1. 建立虛擬環境

```
# 安裝虛擬環境套件：安裝 virtualenv 與 virtualenvwrapper 套件
sudo apt install -y python3-virtualenv
sudo apt install -y python3-virtualenvwrapper

# 設定相關變數

# 設定 環境變數WORKON_HOME（虛擬環境資料夾路徑）
echo "export WORKON_HOME=\$HOME/.virtualenvs" >> ~/.bashrc

# 設定每次啟動自動載入 virtualenvwrapper
echo "source /usr/share/virtualenvwrapper/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc

# 建立虛擬環境(並依照樹梅派預設系統安裝python預設環境)
mkvirtualenv --system-site-packages test_env 

# 建立完成後會自動進入該環境，提示會變成
# (test_env) raspberrypi@raspberrypi:~ $

# 離開虛擬環境
deactivate

# 列出所有虛擬環境
workon

# 重新進入虛擬環境
workon test_env

# 刪除虛擬環境
rmvirtualenv myenv
```

## 2. 在樹梅派上安裝cscode
```
sudo apt upgrade code
```




## 3. 在樹梅派上建立 jupyter notebook + gradio

### 3.1. 安裝與啟動 Jupyter Notebook 開發環境

```
# 進入虛擬環境
workon ai

# 安裝 Jupyter Notebook
pip install notebook
# （若遇錯誤）重新安裝 jupyterlab 避免錯誤
pip install --force-reinstall jupyterlab

# 啟動 Jupyter Notebook 伺服器
# --ip='*' 表示允許任何裝置連線（可改成內網 IP 如 192.168.1.110）
# --no-browser 表示不自動開啟瀏覽器（通常用 SSH 時這樣設）
jupyter notebook --ip='*' --port=8888 --no-browser
```

### 3.2. 在 Notebook 開發環境安裝 Gradio

#### 3.2.1. 第一種情況：未使用 --system-site-packages 建立虛擬環境

```
安裝 Gradio 指定版本（推薦使用 4.38）
pip install --no-cache-dir gradio==4.38
# 加上 --no-cache-dir 可避免安裝舊版快取套件

# 若安裝出現錯誤，使用強制重裝
pip install --force-reinstall --no-cache-dir gradio==4.38
```

#### 3.2.2. 第一種情況：未使用 --system-site-packages 建立虛擬環境

```
pip install gradio
pip install --upgrade ipywidgets
```

### 3.3. Lab：建立 gradio 文字視窗

```python
import gradio as gr

def greet(name):
    return "你好: " + name + "!"

app = gr.Interface(fn=greet,inputs="text",outputs="text")
app.launch(share=True, inline=True, server_name="raspberrypi.local")
```

![upgit_20250414_1744618628.png](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250414_1744618628.png)

### 3.4. Lab：可製化輸入元件

```python
import gradio as gr

def greet(name):
    return "Hello " + name + "!"

inputs = gr.Textbox(lines=2, placeholder="請輸入姓名...", label="請輸入使用者姓名")
outputs = gr.Label()
examples = ["TA01", "TA02"]
app = gr.Interface(fn=greet,
                   inputs=inputs,
                   outputs=outputs,
                   examples=examples,
                   title = "歡迎使用者",
                   description = "輸入姓名顯示歡迎訊息")
app.launch(server_name="raspberrypi.local")
```

![upgit_20250414_1744618961.png|1070x377](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250414_1744618961.png)

### 3.5. Lab：在介面使用圖片元件

```python
import numpy as np
from PIL import Image
import gradio as gr

def rgb2gray(input):
    img = Image.fromarray(input)
    img = img.convert('L')
    return np.array(img)

app = gr.Interface(rgb2gray,gr.Image(image_mode="RGB"), "image")
app.launch(server_name="raspberrypi.local")
```

![upgit_20250414_1744621856.png|741x353](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250414_1744621856.png)

### 3.6. Lab：在 python 上使用 chatgpt API

![upgit_20250414_1744624960.png|639x126](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250414_1744624960.png)

安裝套件

```python
!pip install openai
```

```python
from openai import OpenAI

api_key = "<填入你的API KEY>"
reply_msg = "客戶你好..."
client = OpenAI(api_key=api_key)

while True:
    input_msg = input("情輸入文字")  # 顯示使用者輸入欄位
    print(input_msg)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一位客服機器人"},
            {"role": "assistant", "content": reply_msg},
            {"role": "user", "content": input_msg}
        ],
        max_tokens=100,
        temperature=0.4
    )
    reply_msg = response.choices[0].message.content
    print(f"GPT：{reply_msg}")  # 顯示回覆文字

```
