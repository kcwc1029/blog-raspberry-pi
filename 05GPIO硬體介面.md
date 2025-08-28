## 1. 樹莓派 GPIO 與 GPIO Zero 教學筆記

## 2. GPIO 是什麼？

**GPIO**（General Purpose Input/Output）是樹莓派上用來連接感測器或控制外部裝置的「通用輸入輸出接腳」。

樹莓派共有 **40 根排針**（2 排 × 20 個），可進行電子控制與輸入偵測。
GPIO 可用於：

-   控制 LED 燈
-   偵測按鍵
-   測量溫度、光線強度
-   驅動馬達、蜂鳴器等

### 2.1. 2️⃣ GPIO 接腳圖說明

![upgit_20250417_1744819313.png|365x482](https://raw.githubusercontent.com/kcwc1029/obsidian-upgit-image/main/2025/04/upgit_20250417_1744819313.png)

接腳分為不同類型，例如：

-   **3.3V / 5V 電源**
-   **GND（接地）**
-   **SDA/SCL（I²C 傳輸）**
-   **TXD/RXD（UART 串列）**
-   **MOSI/MISO/SCLK/CE（SPI 傳輸）**

### 2.2. 常用通訊協定對應腳位

-   **UART（串列傳輸）**：TX=8，RX=10
-   **SPI**：MOSI=19，MISO=21，SCLK=23，CE=24/26
-   **I²C**：SDA=3，SCL=5
-   **HAT 擴充模組**：腳位 27、28 用來辨識 EEPROM

### 2.3. 4️ 使用 GPIO 時注意事項

-   **電流限制**：每根腳最多輸出 16mA，全機最多 100mA。
-   **非熱插拔**：插拔裝置前必須關機！
-   **沒有保護電路**：GPIO 電壓最多只能是 3.3V，**不能接 5V**，否則可能燒掉！
-   若需接更多元件：建議改用 **擴充板、Pico、Arduino**

## 3. GPIO Zero 模組（Python 控制）

控制方式

-   樹莓派 GPIO 可用 Python、Java、C 等語言控制。
-   最常見的是透過 Python 使用 GPIO Zero 模組。

優點

-   GPIO Zero 是高階模組，適合初學者快速上手。
-   可以透過簡單指令，控制 LED、按鈕、蜂鳴器、馬達等。

### 3.1. Lab：數位輸出：閃爍 LED 燈
