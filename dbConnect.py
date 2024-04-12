from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from table.indexDetail import indexDetail
import table.indexDetail as detail
import vectorizing
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ast
class dbConnect():

    def insertNews(self,index_name,json_results):
        session = self.getDbSession()
        for json in json_results:
            try:
                for jsonDetail in json['description']:
                    # 문자열을 datetime 객체로 파싱
                    date_obj = datetime.strptime(json['date'], "%a, %d %b %Y %H:%M:%S %z")
                    # 원하는 형식으로 포맷팅
                    formatted_date = date_obj.strftime("%Y년 %m월 %d일 %H시 %M분")

                    desc_all = json['title'].replace('&quot;','"') + ' ' + jsonDetail.replace('&quot;','"') + ' ' + '이 기사의 날짜는 '+formatted_date+'입니다.'

                    indexDetail = detail.indexDetail(
                        index_name = index_name
                        , vectorizing_result = vectorizing.embed_sentence(desc_all)
                        , description_all = desc_all
                        , display_1 = json['title'].replace('&quot;','"')
                        , display_2 = jsonDetail.replace('&quot;','"')
                    )
                    session.add(indexDetail)
                    session.commit()
            except:
                pass
    #select all 후 -> 벡터

    def retrivalAugment(self, prompt):
        session = self.getDbSession()

        # prompt를 벡터로 변환
        prompt_vector = vectorizing.embed_sentence(prompt)
        print(prompt_vector)
        # indexDetail 테이블에서 description_all과 vectorizing_result 추출
        details = session.query(detail.indexDetail).all()
        #descriptions = [detail.description_all for detail in details]
        vectorizing_results = [detail.vectorizing_result for detail in details]

        # 각 벡터화된 결과를 올바른 형태의 배열로 구성
        detail_vectors = []
        for result in vectorizing_results:
            # 문자열을 파싱하여 부동 소수점 배열로 변환
            vector_elements = result.strip("[]").split()
            vector_float = [float(element) for element in vector_elements]
            detail_vectors.append(vector_float)
        detail_vectors = np.array(detail_vectors)

        #print(prompt_vector)
        #print(detail_vectors[0])
        # 코사인 유사도 계산
        similarities = cosine_similarity(prompt_vector, detail_vectors)

        # 유사도가 가장 높은 상위 5개 항목의 인덱스 찾기
        top_indices = similarities[0].argsort()[-5:][::-1]

        # 가장 유사한 5개 항목 반환
        top_details = [details[i] for i in top_indices]
        documents = '[document]\n'
        #print(top_details)
        for top_detail in top_details:
            print(top_detail)
            documents += top_detail.description_all+'\n'
        return documents

    def getDbSession(self):
        engine = create_engine("mysql+pymysql://root:root@127.0.0.1/ragsystem", echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session