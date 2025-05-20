import requests
from bs4 import BeautifulSoup


header_user = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}
base_url = "https://barracks.sa.nexon.com/clan/ircutopia/clanMatch"
referrer = "https://login.nexon.com/"

try:
    response = requests.get(base_url, headers=header_user) # timeout 설정
    response.raise_for_status() # 403 에러 발생 시 예외 발생
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")