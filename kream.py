from os.path import split

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
#클래스, 아이디 css_selector를 이용해 원하는 값을 가져 오기 위한 패키지
from selenium.webdriver.common.by import By
#키보드의 입력 형태를 코드로 작성하기 위해 사용하는 패키지
from selenium.webdriver.common.keys import Keys
import pymysql
from selenium.webdriver.support.expected_conditions import none_of

base_url = "https://kream.co.kr"

header_user = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}

option_ = Options() #인스턴스 화
option_.add_experimental_option("detach", True) #자동으로 브라우저가 종료되지 않게 설정
#selenium 공식 깃허브 참조
option_.add_argument(f"User-Agent={header_user}")

driver = webdriver.Chrome(options=option_)
driver.get(base_url)

driver.find_element(By.CSS_SELECTOR, ".btn_search.header-search-button.search-button-margin").click()
driver.find_element(By.CSS_SELECTOR, ".input_search.show_placeholder_on_focus").send_keys(input("상품명 입력 : ") + Keys.ENTER)
time.sleep(1)

# 사용자 에게 입력 받고 싶어서 만들었는데 실용성 별로
# view_ = input("[50건 보기는 1, 100건 보기는 2를 입력 해 주세요] : ")
#
# if view_ == 1:
#     for i in range(50):
#         driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END + Keys.PAGE_UP)
#         time.sleep(0.3)
# else:
#     for i in range(100):
#         driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END + Keys.PAGE_UP)
#         time.sleep(0.3)

#스크롤 기능########################################################################################
for i in range(10):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END + Keys.PAGE_UP)
    time.sleep(0.3)
##################################################################################################

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

items = soup.select(".product_card")
keyword = input("검색할 키워드 를 입력해 주세요 : ")

product_list = []
for item in items:
    item_brand = item.select_one(".brand-name").text
    item_name = item.select_one(".name").text
    item_name2 = item.select_one(".translated_name").text
    item_price = item.select_one(".text-lookup.bold.display_paragraph.line_break_by_truncating_tail").text
    link = item.select_one(".item_inner")["href"]
    href_link = base_url + link

    product = [item_brand, item_name, item_name2, item_price, href_link]
    product_list.append(product)

    # if keyword in item_name2:
    #     print(f"[{item_brand}]")
    #     print(f"{item_name}")
    #     print(f"{item_name2}")
    #     print(f"[금액] : {item_price}")
    #     print(f"[링크] : {href_link}")
    #     print("="*100)

driver.quit()

connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    db="kream",
    charset="utf8"
)

def execute_query(connection, query, args=None):
    with connection.cursor() as cursor:
        cursor.execute(query, args or ())
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            connection.commit()
            return None


for product in product_list:
    execute_query(
        connection,
        'INSERT INTO kream (item_brand, item_name, item_name2, item_price, href_link) VALUES (%s, %s, %s, %s, %s)',
        (product[0], product[1], product[2], product[3], product[4])
    )




