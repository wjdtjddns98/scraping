from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = "https://kream.co.kr"

# Selenium 옵션 설정
header_user = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}
option_ = Options()
option_.add_argument(f"User-Agent={header_user}")
option_.add_argument("--headless") #헤드리스모드 ( 크롬창을 안띄우고 백그라운드에서만 작업 할수 있음)
option_.add_argument("--window-size=1920,1080")

driver = None  # 드라이버 전역 변수로 초기화

#헤드리스모드 ( 크롬창을 안띄우고 백그라운드에서만 작업 할수 있음)

def initialize_driver():
    """WebDriver를 초기화하고 반환합니다."""
    global driver
    if driver is None:
        print("\nplease wait...")
        try:
            driver = webdriver.Chrome(options=option_)
            driver.get(base_url)
            # 페이지가 완전히 로드될 때까지 최대 10초 대기
            # 'body' 태그가 존재하면 페이지가 로드되었다고 간주
            WebDriverWait(driver, 0).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("웹 드라이버 초기화 완료!")
        except Exception as e:
            print(f"웹 드라이버 초기화 중 오류 발생: {e}")
            driver = None
    return driver


def search_products():
    """상품 검색 기능을 처리합니다."""
    global driver
    driver = initialize_driver()
    if driver is None:
        print("웹 드라이버 초기화에 실패하여 상품 검색을 진행할 수 없습니다.")
        return

    try:
        search_query = input("\n[상품 검색]\n검색할 상품명을 입력해 주세요 (예: 슈프림): ")

        # 검색 버튼이 클릭 가능해질 때까지 대기
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_search.header-search-button.search-button-margin"))
        )
        search_button.click()

        # 검색 입력 필드가 나타날 때까지 대기
        search_input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".input_search.show_placeholder_on_focus"))
        )
        search_input_field.send_keys(search_query + Keys.ENTER)

        # 검색 결과가 로드될 때까지 대기 (예: 특정 상품 카드가 나타날 때까지)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product_card"))
        )

        print("\n[스크롤 중]\n더 많은 상품 정보를 로드하기 위해 페이지를 스크롤 중입니다. 잠시만 기다려 주세요...")
        for _ in range(30):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END + Keys.PAGE_UP)
            time.sleep(0.5)  # 스크롤 후 콘텐츠 로드를 위한 짧은 대기

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        items = soup.select(".product_card")
        if not items:
            print("\n[결과 없음]\n입력하신 상품에 대한 검색 결과가 없습니다.")
            return

        filter_keyword = input(
            "\n[결과 필터링]\n검색 결과 중 출력할 상품명을 필터링할 키워드를 입력해 주세요 (예: 후드, 블랙). \n(비워두면 모든 검색 결과가 출력됩니다): ")

        print("\n--- [검색 결과] ---")
        found_items = False
        for item in items:
            try:
                item_brand = item.select_one(".brand-name").text.strip()
                item_name = item.select_one(".name").text.strip()
                item_name2 = item.select_one(".translated_name").text.strip()

                # 가격 정보는 없을 수도 있으므로 예외 처리
                item_price_element = item.select_one(
                    ".text-lookup.bold.display_paragraph.line_break_by_truncating_tail")
                item_price = item_price_element.text.strip() if item_price_element else "가격 정보 없음"

                # 링크 정보 추출 (href 속성 존재 여부 확인)
                link_element = item.select_one(".item_inner")
                link = link_element["href"] if link_element and "href" in link_element.attrs else ""
                href_link = base_url + link if link else "링크 정보 없음"

                # 필터링 키워드 검사 (대소문자 구분 없이)
                if not filter_keyword or \
                        filter_keyword.lower() in item_name.lower() or \
                        filter_keyword.lower() in item_name2.lower() or \
                        filter_keyword.lower() in item_brand.lower():
                    found_items = True
                    print(f"[{item_brand}]")
                    print(f"상품명: {item_name}")
                    print(f"번역 상품명: {item_name2}")
                    print(f"금액: {item_price}")
                    print(f"링크: {href_link}")
                    print("=" * 150)  # 가독성을 위한 구분선

            except AttributeError:
                # 특정 항목의 요소가 없을 경우 건너뛰기
                continue
            except KeyError:
                # 'href' 속성이 없을 경우 건너뛰기
                continue

        if not found_items:
            if filter_keyword:
                print(f"'{filter_keyword}'키워드를 포함하는 상품을 찾을 수 없습니다.")
            else:
                print("표시할 상품이 없습니다.")  # 필터링 키워드 없이도 결과가 없는 경우

        print("\n--- [검색 종료] ---\n")

    except Exception as e:
        print(f"상품 검색 중 오류 발생: {e}")


def main_menu():
    while True:
        print("\n" + "=" * 50)
        print("             KREAM 상품 정보 스크래퍼️")
        print("=" * 50)
        print("\n   [메인 메뉴]")
        print("   1. 상품 검색")
        print("   2. 종료")
        print("\n" + "=" * 50)

        choice = input("원하는 기능의 번호를 입력해 주세요: ").strip()

        if choice == '1':
            search_products()
        elif choice == '2':
            print("\nKREAM 스크래퍼를 이용해 주셔서 감사합니다. 프로그램을 종료합니다.")
            if driver:
                driver.quit()  # 브라우저 닫기
            break
        else:
            print("\n잘못된 입력입니다. 1 또는 2를 입력해 주세요.")

if __name__ == "__main__":
    main_menu()