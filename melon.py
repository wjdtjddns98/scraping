import requests
from bs4 import BeautifulSoup

header_user = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}
base_url = "https://www.melon.com/chart/index.htm"

req = requests.get(base_url, headers=header_user)
html = req.text

soup = BeautifulSoup(html, "html.parser")
# print(req)

lst50 = soup.select(".lst50") # 1위부터 50위까지의 정보
lst100 = soup.select(".lst100") #50위부터 100위까지의 정보
lst_all = lst50 + lst100

for i in lst_all:
    rank = i.select_one(".rank").text
    title = i.select_one(".ellipsis.rank01 a").text
    artist = i.select_one(".checkEllipsis a").text
    album = i.select_one(".ellipsis.rank03 a").text
    print("="*100)
    print(f"{rank} 위")
    print(f"[{album}] {title} - {artist}")
print("="*100)


