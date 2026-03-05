import time

import pandas as pd
import requests

# -------------------------- 配置參數（新手需修改這部分） --------------------------
# Imgur API配置（替換為你申請的CLIENT_ID）
CLIENT_ID = "你的Imgur Client ID"
# API請求頭（必須攜帶CLIENT_ID）
HEADERS = {
    "Authorization": f"Client-ID {CLIENT_ID}"
}
# Imgur API基礎地址
BASE_URL = "https://api.imgur.com/3"
# 請求延遲（避免過頻請求被封，單位：秒）
REQUEST_DELAY = 2
# 要抓取的圖片數量（建議新手先設小值，如10）
FETCH_LIMIT = 10

# -------------------------- 核心函數 --------------------------
def 獲取imgur_meme圖片數據(分類: str = "meme", 數量: int = 10) -> list[dict]:
    """
    用途：透過Imgur API抓取指定分類的圖片數據（優先抓取meme相關）
    參數：
        分類：要抓取的圖片分類（預設為meme）
        數量：要抓取的圖片數量（最大不超過50）
    返回：圖片原始數據列表（含標題、標籤、格式等）
    """
    # 🚨 核心：Imgur API的熱門meme圖片接口（無法抓取「所有庫存」，數據量過大）
    請求地址 = f"{BASE_URL}/gallery/search/time/all/0/?q={分類}&limit={數量}"

    try:
        # 發送GET請求（帶授權頭）
        回應 = requests.get(請求地址, headers=HEADERS)
        # 檢查請求是否成功
        回應.raise_for_status()
        # 解析JSON數據
        數據 = 回應.json()

        if 數據.get("success") and 數據.get("data"):
            print(f"成功抓取{len(數據['data'])}張{meme}相關圖片")
            return 數據["data"]
        else:
            print("未抓取到任何圖片數據")
            return []
    except requests.exceptions.RequestException as e:
        print(f"抓取圖片數據失敗：{e}")
        return []

def 分析圖片是否适配meme屬性(圖片數據: dict) -> bool:
    """
    用途：分析單張圖片是否具備meme屬性
    參數：
        圖片數據：單張圖片的原始數據字典
    返回：布爾值（True=适配meme，False=不適配）
    """
    # 🚨 核心：meme屬性判斷邏輯（多維度驗證）
    # 1. 提取圖片的標題、標籤、描述
    標題 = 圖片數據.get("title", "").lower()
    標籤列表 = [標籤.lower() for 標籤 in 圖片數據.get("tags", [])]
    描述 = 圖片數據.get("description", "").lower()

    # 2. 判斷是否包含meme相關關鍵字
    meme關鍵字 = ["meme", "梗圖", "迷因", "memes", "梗", "搞笑"]
    包含關鍵字 = any(關鍵字 in 標題 or 關鍵字 in 描述 for 關鍵字 in meme關鍵字)
    標籤包含meme = "meme" in 標籤列表

    # 3. 只要滿足任一條件，判定為适配meme屬性
    return 包含關鍵字 or 標籤包含meme

def 整理圖片數據(原始數據列表: list[dict]) -> list[dict]:
    """
    用途：將原始圖片數據整理為「圖源名稱-圖源標籤-圖源格式」的結構
    參數：
        原始數據列表：獲取imgur_meme圖片數據返回的列表
    返回：整理後的數據列表（含meme屬性標記）
    """
    整理後數據 = []

    for 圖片 in 原始數據列表:
        # 1. 提取核心字段
        圖源名稱 = 圖片.get("title", "無名稱")  # 圖片名稱（標題）
        圖源標籤 = ",".join([標籤.get("name", "") for 標籤 in 圖片.get("tags", [])]) or "無標籤"  # 標籤拼接為字串
        圖源格式 = 圖片.get("type", "").split("/")[-1] if 圖片.get("type") else "未知格式"  # 提取格式（如jpg/png）

        # 2. 分析meme屬性
        适配meme = 分析圖片是否适配meme屬性(圖片)

        # 3. 整理為指定格式
        整理後數據.append({
            "圖源名稱": 圖源名稱,
            "圖源標籤": 圖源標籤,
            "圖源格式": 圖源格式,
            "是否适配meme": 适配meme
        })

        # 請求延遲（避免觸發API限制）
        time.sleep(REQUEST_DELAY)

    return 整理後數據

def 保存整理後數據(整理後數據: list[dict], 保存路徑: str = "imgur_meme數據.csv"):
    """
    用途：將整理後的數據保存為CSV文件（便於查看/分析）
    參數：
        整理後數據：整理圖片數據返回的列表
        保存路徑：CSV文件保存路徑
    返回：無
    """
    if not 整理後數據:
        print("無數據可保存")
        return

    # 轉換為DataFrame並保存
    df = pd.DataFrame(整理後數據)
    df.to_csv(保存路徑, index=False, encoding="utf-8-sig")
    print(f"數據已保存至：{保存路徑}")

# -------------------------- 主程式執行 --------------------------
if __name__ == "__main__":
    print("開始執行Imgur Meme爬蟲...")

    # 1. 抓取meme相關圖片數據
    原始圖片數據 = 獲取imgur_meme圖片數據(分類="meme", 數量=FETCH_LIMIT)

    if 原始圖片數據:
        # 2. 整理數據並分析meme屬性
        整理後數據 = 整理圖片數據(原始圖片數據)

        # 3. 列印整理後的數據（便於查看）
        print("\n=== 整理後的圖片數據 ===")
        for 索引, 數據 in enumerate(整理後數據, 1):
            print(f"{索引}. 圖源名稱：{數據['圖源名稱']}")
            print(f"   圖源標籤：{數據['圖源標籤']}")
            print(f"   圖源格式：{數據['圖源格式']}")
            print(f"   是否适配meme：{數據['是否适配meme']}\n")

        # 4. 保存數據至CSV
        保存整理後數據(整理後數據)

    print("爬蟲執行完畢！")
