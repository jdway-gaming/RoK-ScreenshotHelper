# Screenshot helper

## 使用前確認

| 步驟 | 說明 |
|:----:| :-------- |
| 1 | 確認將模擬器的解析度改為 `1280x720` (視窗大小跟解析度無關，確保解析度即可)   ![](https://i.imgur.com/rV1gng7.png)  |
| 2 | 使用 `nox_adb.exe devices` 來確認你的裝置 port 號 <ul><li> 可到 https://www.yeshen.com/faqs/H15tDZ6YW 參考如何使用 </li><li>確認後到 `screenshot_helper_v2.py`檔案修改第 `12` 行的 `NOX_PORT` 參數</li></ul> |
| 3 | 確認 `NOX_ADB_PATH` 以及 `NOX_SHARE_PATH` 兩個參數設置都正確 |
| 4 | 確認將 `PATH_TO_CHECK_IMAGE` 設置為你想要的路徑 (注意此處為模擬器內之路徑) |
| 5 | 確認 `sample/helper/*` 的圖片跟你的截圖相同，或者利用第 39~40 行的座標來自行 crop 出 template |
| 6 | **請根據你是否為官員到程式第`11`行修改 `IS_R4` 參數**, 是的話填 `True`, 不是的話填 `False` |

## 使用說明

| 步驟 | 說明 |
|:----:| :-------- |
| 1 | 將模擬器打開到會員的畫面，並對齊上方 <br> ![](https://i.imgur.com/KMUEkIB.png) |
| 2 | 執行程式，截圖會存到共享資料夾下 (根據 `PATH_TO_CHECK_IMAGE` 參數) |

## 使用限制

1. 僅能記錄 R1 ~ R3, R4 及 R5 的畫面不適用
2. 若你是 R4 以上(R4需有聯盟職位), 人員順序會依照上線狀態排序，因此上下線造成的順序改變可能會導致漏掉人或重複截圖，建議沒有聯盟職位時使用
3. 每次紀錄完 12 筆後會需要人為調整畫面，對齊下個 12 筆
4. 若過程中有自己出現，程式會卡住，需手動結束程式並跳過