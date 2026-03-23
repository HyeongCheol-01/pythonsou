import requests
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd
# 1. 파일 열기 (mode='w' 사용)
filename = "market_cap.csv"
with open(filename, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    # 2. 1페이지와 2페이지 반복
    for page in range(1, 3):
        url = f"https://finance.naver.com/sise/sise_market_sum.naver?page={page}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 테이블 전체 찾기
        table = soup.select_one("table.type_2")

        # 3. 1페이지일 때만 헤더(컬럼명) 추출해서 파일에 첫 줄로 쓰기
        if page == 1:
            thead = table.select_one("thead")
            # th 태그들의 텍스트를 리스트로 만들기
            header_cols = [th.get_text(strip=True) for th in thead.select("th")]
            writer.writerow(header_cols)
        
        # 4. 데이터 행 추출하기
        rows = table.select("tbody tr")
        
        for row in rows:
            cols = row.select("td")
            if len(cols) <= 1:
                continue
            
            # 각 td 안의 텍스트를 깔끔하게 뽑아서 리스트로 만들기
            data = [col.get_text(strip=True) for col in cols]
            # 추출한 리스트를 csv 파일의 한 줄로 기록
            writer.writerow(data)

df = pd.read_csv(filename)
# 2. 위에서부터 3개 행(시가총액 1~3위)만 추출
top3_df = df.head(3)
# 전체 컬럼을 다 보면 너무 길 수 있으니, 핵심 컬럼만 골라서 출력해보겠습니다.
print(top3_df)


# import requests
# import pandas as pd
# from bs4 import BeautifulSoup

# urls = [
#     "https://finance.naver.com/sise/sise_market_sum.naver?&page=1",
#     "https://finance.naver.com/sise/sise_market_sum.naver?&page=2"
# ]

# headers = {"User-Agent": "Mozilla/5.0"}
# file_name = "market_cap.csv"


# with open(file_name, mode='w', encoding='utf-8') as f:
#     f.write("종목명,시가총액\n")
    
#     for url in urls:
#         res = requests.get(url=url, headers=headers)
#         soup = BeautifulSoup(res.text, 'html.parser')

#         rows = soup.select("table.type_2 > tbody > tr")
#         for row in rows:
#             if not row.select_one("a.tltle"): continue

#             name = row.select_one("a.tltle").get_text(strip=True)
#             price = row.select(".number")[4].get_text(strip=True).replace(',', '')
            
#             f.write(f"{name},{price}\n")

# df = pd.read_csv(file_name)
# df['시가총액'] = pd.to_numeric(df['시가총액'])
# df.index = df.index + 1
# print(df[['종목명', '시가총액']].head(5))