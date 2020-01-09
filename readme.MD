# Screenshot helper

## 使用前確認

| 步驟 | 說明 |
|:----:| :-------- |
| 1 | 確認將模擬器的解析度改為 `1280x720` (視窗大小跟解析度無關，確保解析度即可)   ![](https://i.imgur.com/rV1gng7.png)  |
| 2 | 使用 `nox_adb.exe devices` 來確認你的裝置 port 號 <ul><li> 可到 https://www.yeshen.com/faqs/H15tDZ6YW 參考如何使用 </li><li>確認後到 `screenshot_helper_v2.py`檔案修改第 `15` 行的 `default`, 或者用執行時加入 `--nox_port` 帶入</li></ul> |
| 3 | 確認 `NOX_ADB_PATH` (13行) 以及 `NOX_SHARE_PATH` (16行) 兩個參數設置都正確 |
| 4 | 確認將 `PATH_TO_CHECK_IMAGE` 設置為你想要的路徑 <i>(注意此處為模擬器和電腦共享之路徑)</i> |
| 5 | 確認 `sample/helper/*` 的圖片跟你的截圖相同，或者利用第 44~49 行的座標來自行 crop 出 template |

## 參數列表
* 程式執行可帶入不同參數來修正行為
* 範例:
```bash
python screenshot_helper_v2.py \
    --nox_port 62001 \
    --is_member \
    --start_num 3 \
    --last_num 11
```

| 參數名稱 | 說明 |
| --- | ---- |
| `nox_adb_path` | 到夜神模擬器 `adb.exe` 的路徑 |
| `nox_port` | 欲執行程式的模擬器編號 |
| `nox_share_path` | 夜神模擬器下的資料夾位置 (需設定到跟主機共享的位置) |
| `path_check_image` | 會將程式過程需要的截圖存放到此位置，程式執行完成後將刪除 <br> 注意：<b>此路徑必須與 `nox_share_path` 呼應，否則將讀取不到</b> |
| `is_r4` | 如果該帳號是對象聯盟的 R4, 則需加入此參數 |
| `is_member` | 如果該帳號是對象聯盟的成員，則須加入此參數 |
| `last_num` | 截圖程式執行到這個數字之位置後會停止 (注意該數字會被執行) |
| `start_num` | 截圖程式會跳過此數字前的位置 (注意該數字會被執行) |


## 使用說明

| 步驟 | 說明 |
|:----:| :-------- |
| 1 | 將模擬器打開到會員的畫面，並對齊上方 <br> ![](https://i.imgur.com/KMUEkIB.png) |
| 2 | 執行程式，截圖會存到共享資料夾下 |


### 參數設置範例
* 注意編號是從 0 開始，程式每次只會最多抓當前畫面的 12 筆資料

![](https://i.imgur.com/bUGxksD.jpg)


## 使用限制

1. 僅能記錄目標聯盟的 R1 ~ R3, R4 及 R5 的畫面不適用
2. 若你是 R4 以上(R4需有聯盟職位), 人員順序會依照上線狀態排序，因此上下線造成的順序改變可能會導致漏掉人或重複截圖，建議沒有聯盟職位時使用
3. 每次紀錄完 12 筆後會需要人為調整畫面，對齊下個 12 筆
4. 若過程中有自己出現，程式會卡住，需手動結束程式並跳過，或透過設定 `start_num` 及 `last_num` 參數來跳過自己
