import requests

# 必備：模擬瀏覽器的請求頭
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
# 發送GET請求
url = "https://www.baidu.com"

resp = requests.get(url, headers=headers)

print(resp)

if resp.status_code == 200:
    html = resp.text
    data = resp.json
    print(data)
