## 1. 檔案系統指令

`pwd`：顯示目前工作目錄

-   用法：`pwd`
-   範例輸出：`/home/pi

`ls`：列出目錄內容

-   用法：`ls` ➝ 顯示目前目錄檔案/資料夾
-   `ls -l` ➝ 顯示詳細資訊（權限、擁有者、檔案大小等）
-   `ls -l /home/pi` ➝ 顯示指定目錄下的內容

`cd`：切換目錄

-   用法：`cd 目錄名稱`
-   特殊符號：
    -   `cd ..` ➝ 回上層
    -   `cd ~` ➝ 回家目錄
    -   `cd /` ➝ 回根目錄

`mkdir`：建立新目錄

-   用法：`mkdir 資料夾名稱`
-   範例：`mkdir Joe`

`rm`：刪除檔案

-   用法：`rm 檔名`
-   範例：`rm test.txt`
-   補充：務必小心！`rm` 不會詢問確認，且永久刪除。

`rmdir`：刪除空資料夾

-   用法：`rmdir 資料夾名稱`
-   注意：只能刪空的資料夾。

`cp`：複製檔案

-   用法：`cp 原檔名 目的地`
-   範例：`cp file.txt file2.txt`（複製成新檔案）
-   複製到子資料夾：`cp file.txt Documents/file2.txt`

`mv`：移動檔案或重新命名

-   用法：`mv 原檔名 新路徑` 或 `mv 舊檔名 新檔名`
-   範例：`mv file.txt /home/pi/Documents`

`find`：搜尋檔案

-   用法：
    -   搜尋副檔名為 `.txt`：`find /home/pi -name '*.txt'`
    -   精準搜尋：`find . -name 'file2.txt'`
    -   加上 `sudo` 提升權限：`sudo find / -name 'file2.txt'`

`df`：查看磁碟使用狀況

-   用法：`df`
-   顯示各個掛載點的容量與使用百分比

`clear`：清除畫面

## 2. 網路與系統資訊指令

`ping`：檢查連線狀態

-   用法：`ping 網址或IP`
-   結束測試按 `Ctrl + C`

`hostname`：顯示主機名稱與 IP

-   用法：
    -   `hostname` ➝ 顯示名稱
    -   `hostname -I` ➝ 顯示 IP

`ifconfig`：網路介面設定

-   用法：`ifconfig` ➝ 顯示所有介面設定
-   例：`ifconfig wlan0` 顯示 WiFi 狀態與 IP

`lsusb`：顯示 USB 裝置

-   用法：`lsusb`
    `lsmod`：顯示已載入的核心模組
-   用法：`lsmod`

## 3. 檔案下載與壓縮

`wget`：下載檔案

-   用法：`wget [網址]`
-   範例：`wget https://.../koala.png`

`unzip`：解壓縮 ZIP

-   用法：`unzip test.zip`

`tar`：壓縮與解壓 .tar.gz

-   壓縮：`tar -czvf file.tar.gz file1.txt file2.txt`
-   解壓：`tar -xzvf file.tar.gz`
-   建議解壓前建個資料夾：`mkdir Tmp && cp file.tar.gz Tmp`

`sudo`：超級使用者指令

-   `sudo` 全名是 Super-user Do
-   必須要 root 權限時才可執行指令
-   範例：
    -   `sudo find / -name 'firefox-bin'`
    -   `sudo shutdown -h now` ➝ 關機

## 4. Linux 的使用者與檔案權限指令

who：顯示登入使用者
useradd：新增使用者

```
sudo useradd -m -G adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,netdev,gpio,i2c,spi joe

# -m 建立 home 資料夾
# -G 加入多個群組
# 建立新使用者 joe 並分配權限與家目錄。

# 查看是否新增使用者
ls /home
```

passwd：設定或變更密碼

```
sudo passwd joe
```

chmod：改變檔案權限

```
chmod u+x file.txt # 給予使用者（u）執行（x）權限。
chmod u=rw file.txt # 明確指定使用者擁有讀寫權限。
```

chown：改變檔案擁有者

```
sudo chown joe:root file.txt
# 將 file.txt 的擁有者設為 joe，群組設為 root。
```

## 5. 使用命令列安裝與解除安裝應用程式

Raspberry Pi OS 採用的是 Debian 系列的 apt 指令。

```
# 更新套件清單
sudo apt update

# 升級所有已安裝套件(更新所有已安裝的套件到最新版（-y 自動同意))
sudo apt -y upgrade

# 安裝新套件(安裝遊戲 nethack-console)
sudo apt -y install nethack-console

# 移除應用程式
sudo apt -y remove gnome-screenshot # 移除指定套件但保留設定檔。
sudo apt -y autoremove gnome-screenshot # 自動移除不再需要的相依套件
sudo apt -y purge nethack-console # 徹底移除套件與設定

# 清除暫存檔案
sudo apt -y clean # 清除下載後的安裝套件暫存檔
sudo apt -y autoremove --purge # 自動移除多餘的相依檔案與設定。
sudo reboot # 重啟系統，讓更新生效。

```
