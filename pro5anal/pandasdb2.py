import pymysql
import pandas as pd
import csv
import matplotlib.pyplot as plt  # 시각화를 위해 반드시 추가해야 합니다!

# --- 그래프 한글 깨짐 방지 폰트 설정 ---
plt.rc('font', family='Malgun Gothic') # 윈도우 환경 기준
plt.rcParams['axes.unicode_minus'] = False 

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123',
    'database': 'test',
    'charset': 'utf8'
}

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql = """
        select jikwonno, jikwonname,busername,jikwonjik,jikwongen,jikwonpay
        from jikwon inner join buser on jikwon.busernum=buser.buserno
    """
    cursor.execute(sql)
    
    # [핵심 수정] DB에서 가져온 데이터를 변수(db_data)에 미리 담아둡니다.
    db_data = cursor.fetchall()
    
    # 커서 대신 저장해둔 db_data를 사용하여 데이터프레임을 만듭니다.
    df1 = pd.DataFrame(db_data,
                columns=['jikwonno','jikwonname','busername','jikwonjik','jikwongen','jikwonpay'])
    print(df1.head(3))
    print('연봉의 총합 : ', df1['jikwonpay'].sum())
    
    print()
    # csv file i/o
    # 빈 줄 생김 방지를 위해 newline='' 추가
    with open('pandasdb2.csv', mode ='w', encoding='utf-8', newline='') as fobj:
        writer = csv.writer(fobj)
        # [핵심 수정] cursor() 에러 해결 -> db_data를 반복문으로 돌립니다.
        for row in db_data:
            writer.writerow(row)
            
    # [핵심 수정] name -> names 로 스펠링 수정
    df2 = pd.read_csv('pandasdb2.csv', header=None,
                    names=['번호','이름','부서','직급','성별','연봉'])
    print(df2.head(3))
    
    print("\n\npandas의 sql 처리 함수 이용 ----------")
    df = pd.read_sql(sql,conn)
    df.columns = ['번호','이름','부서','직급','성별','연봉']
    print(df.head(2))
    print(df[:2])
    print(df[:-28])
    print(df['이름'].count(), ' ', len(df))
    print('부서별 인원수:\n', df['부서'].value_counts())
    print('연봉 7000 이상 :\n', df.loc[df['연봉'] >= 7000])
    ctab = pd.crosstab(df['성별'], df['직급'], margins=True)
    print('교차표\n', ctab)
    
    # 시각화: 직급별 '연봉'의 '평균(mean)'을 구합니다.
    jik_ypay = df.groupby(['직급'])['연봉'].mean()
    print("\n직급별 평균 연봉:\n", jik_ypay)
    
    # 바 차트(Bar chart) 그리기
    jik_ypay.plot(kind='bar', color='skyblue', title='직급별 평균 연봉', rot=0)
    plt.xlabel('직급')
    plt.ylabel('평균 연봉')
    plt.show()  # 그래프 창 띄우기
    
except Exception as e:
    print('처리 오류: ', e)
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()