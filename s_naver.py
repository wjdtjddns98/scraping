from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

keyword = input("검색 하고싶은 키워드 : ")
base_url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=" +  keyword

option_ = Options() #인스턴스화
option_.add_experimental_option("detach", True) #자동으로 브라우저가 종료되지 않게 설정

driver = webdriver.Chrome(options=option_)
driver.get(base_url)

# while 문을 사용 하면 최초 last_height을 return 으로 받아 오고 last_height와 new_height가 같을시 break로 탈출
# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(0.05)
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height

#for 문을 사용하면 range를 이용해 스크롤할 횟수 정함
for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.3)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

results = soup.select(".view_wrap") #결과는 리스트와 동일한 테이터 타입으로 가져옴
print(len(results))
for i in results:
    title = i.select_one(".title_link").text
    link = i.select_one(".title_link")["href"]
    writer = i.select_one(".name").text
    dsc = i.select_one(".dsc_link").text
    print(f"제목 : {title} : {link} 작성자 : {writer}")
    print(f"{dsc}")
    print("="*100)

driver.quit()
