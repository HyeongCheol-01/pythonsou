# pandas의 DataFrame의 자료를 원격 DB의 테이블에 저장
# pip install sqlalchemy

import pandas as pd
from sqlalchemy import create_engine
import pymysql
import os
from dotenv import load_dotenv
load_dotenv
data = {
    'code':[10,11,12],
    'sang':['사이다','맥주','와인'],
    'su':[20,22,5],
    'dan':[5000,3000,70000]
}
try:
    frame = pd.DataFrame(data)
    print(frame)

    engine = create_engine(f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@127.0.0.1:3306/test?charset=utf8mb4")

    # 저장
    frame.to_sql(name="sangdata", con=engine, if_exists='append', index=False)
    
    #읽기
    df = pd.read_sql("select * from sangdata", engine)
    print(df)

except Exception as e:
    print('처리 오류 : ', e)