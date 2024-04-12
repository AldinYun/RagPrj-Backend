import urllib.request
import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
#import dbConnect
from dbConnect import dbConnect


limit_token = 700
def process_news(news):
    try:
        response = requests.get(news['link'])
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            news_content_div = soup.find('div', {'id': 'newsct_article'})
            if news_content_div:
                content_texts = news_content_div.stripped_strings
                article = ''
                for text in content_texts:
                    article += text.replace('<b>', '').replace('</b>', '')

                chunk_count = (len(article) // limit_token) + 1
                chunk_limit_token = len(article) // chunk_count
                start_idx = 0
                chunks = []
                for num in range(chunk_count):
                    chunk = article[start_idx:start_idx + chunk_limit_token]
                    # 토큰이 지정된 길이를 초과하는 경우, 해당 인덱스부터 가장 가까운 온점까지의 문자열로 잘라줌
                    if len(chunk) == chunk_limit_token:
                        period_idx = chunk.rfind('.')  # 가장 가까운 온점의 인덱스 찾기
                        if period_idx != -1:
                            chunk = chunk[:period_idx + 1]  # 온점까지의 문자열로 자르기
                    chunks.append(chunk)
                    start_idx += len(chunk)
                return {"title": news['title'].replace('<b>', '').replace('</b>', ''), "description": chunks,
                        "date": news['pubDate']}
    except Exception as e:
        print(f"Error processing news: {e}")

def scrabNews(prompt):
    client_id = "nM5fFO97OdGT70OwVXdA"
    client_secret = "VyLKXxzziq"
    encText = urllib.parse.quote(prompt)
    url = "https://openapi.naver.com/v1/search/news?sort=date&display=100&query=" + encText  # JSON 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    results = list()
    if rescode == 200:
        response_body = response.read()
        news_json = json.loads(response_body.decode('utf-8'))['items']

        filtered_news = [news for news in news_json if 'naver' in news['link']]

        with ThreadPoolExecutor(max_workers=10) as executor:
            processed_results = list(executor.map(process_news, filtered_news))
            results.extend(processed_results)
    else:
        pass
    # 결과를 JSON 형식으로 변환
    json_results = json.dumps(results, ensure_ascii=False, indent=4)

    #print(json_results)
    # dbConnect 인스턴스 생성
    db_connector = dbConnect()
    # insertNews 메서드 호출
    db_connector.insertNews(prompt, results)
    #dbConnect.insertNews(prompt,json_results)