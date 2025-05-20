import requests
from bs4 import BeautifulSoup

keyword = input()
base_url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=" +  keyword

req = requests.get(base_url)
html = req.text

soup = BeautifulSoup(html, "html.parser")

results = soup.select(".view_wrap") #결과는 리스트와 동일한 테이터 타입으로 가져옴

for i in results:
    title = i.select_one(".title_link").text
    link = i.select_one(".title_link")["href"]
    writer = i.select_one(".info_group .name").text
    print(f"제목 : {title} : {link}")
    print("="*100)






