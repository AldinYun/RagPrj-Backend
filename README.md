**이 프로젝트는 크롤링과 벡터검색을 통한 RAG에 대한 고객 설명용 예제로 작성 함**

--환경
1. 데이터베이스
   - RDBMS: MariaDB
   - Database 이름: ragsystem
   - Table 정보:
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

2. 파이썬 (Python 3.11)
   - 요구 라이브러리:
     - fastapi == 0.104.0
     - transformers == 4.33.1
     - torch == 2.1.0
     - SQLAlchemy == 2.0.22
     - uvicorn == 0.23.2
     - beautifulsoup4 == 4.12.2
     - openai == 0.28.1

--Local Test
```bash
uvicorn api:app --reload --host 0.0.0.0

--스웨거 접속
http://localhost:8000/docs#

--API 설명

/getNewsList (type: POST, keyword: str)

키워드로 네이버 최신뉴스를 가져옴
뉴스 헤더와 본문 내용을 결합한 원문 패시지와 SBERT로 임베딩 한 결과를 DB에 적재
/ra (type: POST, prompt: str)
프롬프트를 벡터 색인하여 가장 유사한 5개의 청크를 가져옴 (증강생성까지의 테스트 용도)

/generate
RAG 설명용 예제로 증강 생성된 내용을 지식으로 첨부하여 GPT-3.5를 통해 generate까지 실시 (구동을 위해서는 completion.py에 OpenAI에서 활용 가능한 key가 있어야 함.)
