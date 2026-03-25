from flask import Flask, render_template, request
import pymysql
import pandas as pd
import numpy as np
from markupsafe import escape
import matplotlib.pyplot as plt
import os
app= Flask(__name__)

db_config = {
    'host':'127.0.0.1','user':'root','password':'123',
    'database':'test','port':3306,'charset':'utf8mb4'
}

def get_connection():
    return pymysql.connect(**db_config)

@app.route("/", methods=["GET", 'POST'])
def dbshow():
    dept = request.args.get("dept", "").strip()
    
    sql = """
        select j.jikwonno 직원번호, j.jikwonname 직원명, j.jikwongen 성별, 
        b.busername 부서명, b.busertel 부서전화, j.jikwonpay 연봉, j.jikwonjik 직급, 
        TIMESTAMPDIFF(YEAR, j.jikwonibsail, CURDATE()) 근무년수
        from jikwon j
        inner join buser b on j.busernum=b.buserno
        order by j.busernum asc, j.jikwonname asc
    """
    params = []
    # SQL 실행
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]  # description: 컬럼등 정보 열기
            
    df = pd.DataFrame(rows, columns=cols)
    print(df)
    # 직원정보 html로 전송
    if not df.empty:
        jikwondata = df[['직원번호','직원명','부서명','직급','연봉','근무년수']].to_html(index=False)
    else:
        jikwondata = "직원 정보가 없어요"
    
    # 부서별 연봉 통계
    if not df.empty:
        stats_df = (
            df.groupby("부서명")['연봉']
            .agg(
                연봉합 = "sum",
                연봉평균 = "mean",
            )
            .round(2)
            .reset_index()
            .sort_values(by='연봉평균', ascending=False)
        )
        print(stats_df)
        statsdata = stats_df.to_html(index=False)
    else:
        statsdata = "통계 대상 자료가 없어요"
    
    if not df.empty:
        # 한글 폰트 설정 (Windows 기준)
        plt.rc('font', family='Malgun Gothic')
        
        plt.figure(figsize=(8, 5))
        # 세로 막대 그래프 그리기 (부서명별 연봉합)
        plt.bar(stats_df['부서명'], stats_df['연봉합'], color='skyblue')
        plt.title('부서별 연봉 합계')
        plt.xlabel('부서명')
        plt.ylabel('연봉 합계')

        # 그래프를 static 폴더에 이미지로 저장
        graph_path = 'static/chart.png'
        plt.savefig(graph_path) 
        plt.close() # 메모리 닫기

        
    if not df.empty:
        freq_df = pd.crosstab(df['성별'], df['직급'], margins=True, margins_name="합계")
        # HTML 변환
        print(freq_df)
        freqdata = freq_df.to_html()
    else:
        freqdata = "데이터가 없어 빈도표를 만들 수 없습니다."
        
        
        
    if not df.empty:
        top_earners_df = df.loc[df.groupby('부서명')['연봉'].idxmax(), ['부서명', '직원명', '연봉']]
        top_data = top_earners_df.to_html(index=False)
        
    else:
        top_data = "데이터 없음"
    if not df.empty:
        total = len(df)
        dept_counts = df.groupby('부서명').size()
        dept_ratio = (dept_counts / total * 100).round(2)
        ratio_df = dept_ratio.reset_index()
        ratio_df.columns = ['부서명', '비율(%)'] # 컬럼명 지정
        
        total_msg = f"총 인원: {total}명"
        ratiodata = ratio_df.to_html(index=False)
    else:
        total_msg = "총 인원: 0명"
        ratiodata = "데이터가 없습니다."


        
    return render_template("index.html", 
                        dept=escape(dept),
                        jikwondata=jikwondata, 
                        statsdata=statsdata, 
                        freqdata=freqdata,
                        top_data=top_data,
                        total_msg=total_msg,
                        ratiodata=ratiodata)


if __name__ == '__main__':
    app.run(debug=True)

