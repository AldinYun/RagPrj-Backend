# 프로젝트 설명

이 프로젝트는 크롤링과 벡터 검색을 통한 RAG에 대한 고객 설명용 예제로 작성되었습니다.

# 지원 모델
- GPT3.5-turbo
- Gemini
현재 RAG 성능평가 결과 Gemini가 할루시네이션이 발생하지 않으며 GPT는 다수 발생..(prompt instruct fitting이 좀 더 필요해 보임...)

## 기본 동작

사용자가 입력한 키워드를 기반으로 네이버 뉴스를 크롤링하여 가져오는 API인 `/getNewsList`가 있습니다. 이후 사용자의 다음 질의에는 가져온 뉴스 내용이 반영됩니다. 사용자는 `/ra` 또는 `/generate` 엔드포인트를 통해 텍스트를 생성할 수 있습니다.

### 변경 예정 사항

- front와 연동되도록 chatbot UI를 추가할 예정입니다. 또한 프롬프트 의도를 분류하는 few-shot 의도분류를 추가하여 크롤링을 할 것인지 generate를 진행할 것인지를 분기 처리할 예정입니다.
- 크롤링할 수 있는 플랫폼을 네이버 뉴스 이외에도 추가할 예정입니다.
- rerank 기능을 고려 중에 있습니다.

## 환경

### 데이터베이스

- RDBMS: MariaDB
- Database 이름: ragsystem

#### 테이블 정보

```sql
CREATE TABLE index_detail (
    index_id INT,
    index_name VARCHAR(50),
    vectorizing_result TEXT,
    description_all TEXT,
    display_1 TEXT,
    display_2 TEXT,
    display_3 TEXT,
    display_4 TEXT,
    display_5 TEXT,
    display_6 TEXT,
    display_7 TEXT,
    display_8 TEXT,
    display_9 TEXT,
    display_10 TEXT
);
```
##### 파이썬 (Python 3.11)
요구 라이브러리:
- fastapi == 0.104.0
- transformers == 4.33.1
- torch == 2.1.0
- SQLAlchemy == 2.0.22
- uvicorn == 0.23.2
- beautifulsoup4 == 4.12.2
- openai == 0.28.1

### 로컬테스트
uvicorn api:app --reload --host 0.0.0.0  

### 스웨거접속  
http://127.0.0.1:8000/docs#

### API 설명  
/getNewsList (type: POST, keyword: str)  
키워드로 네이버 최신 뉴스를 가져옵니다. 뉴스 헤더와 본문 내용을 결합한 원문 패시지와 SBERT로 임베딩 한 결과를 DB에 적재합니다.

/ra (type: POST, prompt: str)  
프롬프트를 벡터 색인하여 가장 유사한 5개의 청크를 가져옵니다 (증강생성까지의 테스트 용도).  

/generate(type: POST, prompt: str, modelNum: int)  
RAG 설명용 예제로 증강 생성된 내용을 지식으로 첨부하여 GPT-3.5를 통해 generate까지 실시합니다 (구동을 위해서는 completion.py에 OpenAI에서 활용 가능한 key가 있어야 함).  
