**이 프로젝트는 크롤링과 벡터검색을 통한 RAG에 대한 고객 설명용 예제로 작성 함**<br>

--환경<br>
1.데이터베이스<br>
  rdbms : mariadb<br>
  database이름 : ragsystem<br>
  table 정보 :<br>
      CREATE TABLE index_detail (<br>
          index_id INT,<br>
          index_name VARCHAR(50),<br>
          vectorizing_result TEXT,<br>
          description_all TEXT,<br>
          display_1 TEXT,<br>
          display_2 TEXT,<br>
          display_3 TEXT,<br>
          display_4 TEXT,<br>
          display_5 TEXT,<br>
          display_6 TEXT,<br>
          display_7 TEXT,<br>
          display_8 TEXT,<br>
          display_9 TEXT,<br>
          display_10 TEXT<br>
      );<br>
2.파이썬(python 3.11)<br>
  -- 요구 라이브러리<br>
  fastapi == 0.104.0<br>
  transformers == 4.33.1<br>
  torch == 2.1.0<br>
  SQLAlchemy == 2.0.22<br>
  uvicorn == 0.23.2<br>
  beautifulsoup4 == 4.12.2<br>
  openai == 0.28.1<br>
  <br>
--local test<br>
uvicorn api:app --reload --host 0.0.0.0<br>
--스웨거 접속<br>
http://localhost:8000/docs#<br>

--api 설명<br>
/getNewsList(type:post , keyword : str)<br>
  1. 키워드로 네이버 최신뉴스를 가져옴<br>
  2. 뉴스 헤더와 본문 내용을 결합한 원문 패시지와 sbert로 임베딩 한 결과를 db에 적재<br>
<br>
/ra(type:post, prompt : str)<br>
  프롬프트를 벡터 색인하여 가장 유사한 5개의 청크를 가져옴(증강생성까지의 테스트 용도)<br>
<br>
/generate<br>
  rag 설명용 예제로 증강 생성된 내용을 지식으로 첨부하여 gpt3.5를 통해 generate까지 실시(구동을 위해서는 completion.py에 openai에서 활용가능한 key가 있어야 함.)<br>
