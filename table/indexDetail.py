
from sqlalchemy import Column, Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class indexDetail(Base):
    __tablename__ = 'index_detail'
    index_id = Column(Integer, primary_key=True)
    index_name = Column(String(50))
    vectorizing_result = Column(TEXT)
    description_all = Column(TEXT)
    display_1 = Column(TEXT)
    display_2 = Column(TEXT)
    display_3 = Column(TEXT)
    display_4 = Column(TEXT)
    display_5 = Column(TEXT)
    display_6 = Column(TEXT)
    display_7 = Column(TEXT)
    display_8 = Column(TEXT)
    display_9 = Column(TEXT)
    display_10 = Column(TEXT)