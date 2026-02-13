import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def connect_mongodb():
    pass


def html_to_contect(imageurl):
    result = ""

    try:
    result = soup.find_one(
        {"page_url": imageurl},
        {"html_content": 1, "_id": 0}
        )
        if result:
            return result["html_content"]
        else:
            return "undefined HTML"

    except Exception as e:
        print(f"fail check: {e}")
        return ""





def init_soup():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    # 發送GET請求
    url = "https://www.imgur.com"

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")

    title_tag = soup.find("title")
    print("網頁標題：", title_tag.text)



# -------------------------- 主程式執行 --------------------------
if __name__ == "__main__":
    htmltar = connect_mongodb()

    if htmltar:
        
        elements = html_to_contect(imageurl)



'''
    words_tags = soup.find_all("png")
    print("\n前5個鏈接")
    for word in words_tags[:5]:
        link = word.get("href", "No Links")
        text = word.text.strip()
        print(f"Text: {text} -> Link:{link}")
    =====
'''