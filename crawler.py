import requests
from bs4 import BeautifulSoup
import json

# 기본 URL
url = "https://www.moleg.go.kr/lawinfo/nwLwAnList.mo?mid=a10106020000"

# HTTP GET 요청

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

response = requests.get(url, headers=headers)
print(response.status_code)  # 200이면 성공적으로 로드된 것입니다.
print(f"응답 상태 코드: {response.status_code}")


# 데이터를 담을 리스트
data_list = []

# 안건 번호와 안건명을 추출하기 위해 테이블에서 각 행을 찾음
rows = soup.select('#content_detail > div.table_wrap > div > table > thead > tr')

# 각 행에서 안건번호와 안건명 추출
for row in rows:
    # 안건번호와 안건명 추출
    case_number = row.select_one('th:nth-child(2)').text.strip()
    case_title = row.select_one('th:nth-child(3)').text.strip()

    # 개별 안건에 대한 세부사항 (질의요지, 회답, 이유) 추출
    case_url = f"https://www.moleg.go.kr{row.a['href']}"  # 안건 상세 페이지 URL

    # 상세 페이지로 이동하여 질의요지, 회답, 이유를 추출
    case_response = requests.get(case_url)
    case_soup = BeautifulSoup(case_response.text, 'html.parser')

    # 질의요지, 회답, 이유 추출
    query = case_soup.select_one('#listForm > div > div:nth-child(3) > strong')
    answer = case_soup.select_one('#listForm > div > div:nth-child(4) > strong')
    reason = case_soup.select_one('#listForm > div > div:nth-child(5) > strong')

    # 데이터를 딕셔너리 형식으로 저장
    case_data = {
        "안건번호": case_number,
        "안건명": case_title,
        "질의요지": query.text.strip() if query else None,
        "회답": answer.text.strip() if answer else None,
        "이유": reason.text.strip() if reason else None
    }

    # 데이터 리스트에 추가
    data_list.append(case_data)

# 결과를 JSON 파일로 저장
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)

print("크롤링이 완료되었습니다. output.json 파일에 저장되었습니다.")
