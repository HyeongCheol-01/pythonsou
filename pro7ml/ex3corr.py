import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib




#산점도 그리기
def setScatterGraph(tour_table, all_table, tourpoint):
    merge_table = pd.merge
    fig = plt.figure()
    fig.suptitle(tourpoint + '상관관계분석')
    plt.subplot(1,3,1)
    plt.xlabel('중국인 방문수')
    plt.ylabel('외국인 입장객 수')
    lamb1 = lambda p:merge_table['china'].corr(merge_table['ForNum'])
    r1 = lamb1(merge_table)


def processFunc():
    # 서울시 관광지 정보 파일
    fname="서울특별시_관광지입장정보_2011_2016.json"
    jsonTP = json.loads(open(fname, 'r', encoding='utf-8').read())
    tour_table = pd.DataFrame(jsonTP, columns=('yyyymm', 'resNm', 'ForNum'))
    tour_table = tour_table.set_index('yyyymm')
    # print(tour_table)
    # yyyymm      resNm  ForNum
    # 201101        창덕궁   14137
    # 201101        운현궁       0
    resNm = tour_table.resNm.unique()
    
    
    # 중국인 관광지 정보 파일 DataFrame에 저장
    cdf = '중국인방문객.json'
    jdata = json.loads(open(cdf, 'r', encoding='utf-8').read())
    china_table = pd.DataFrame(jdata, columns=('yyyymm', 'visit_cnt'))
    china_table = china_table.rename(columns={'visit_cnt':'china'})
    china_table = china_table.set_index('yyyymm')
    print(china_table[:2])
    
    # 중국인 관광지 정보 파일 DataFrame에 저장
    cdf = '일본인방문객.json'
    jdata2 = json.loads(open(cdf, 'r', encoding='utf-8').read())
    japan_table = pd.DataFrame(jdata2, columns=('yyyymm', 'visit_cnt'))
    japan_table = japan_table.rename(columns={'visit_cnt':'japan'})
    japan_table = japan_table.set_index('yyyymm')
    
    
    # 중국인 관광지 정보 파일 DataFrame에 저장
    cdf = '미국인방문객.json'
    jdata3 = json.loads(open(cdf, 'r', encoding='utf-8').read())
    usa_table = pd.DataFrame(jdata3, columns=('yyyymm', 'visit_cnt'))
    usa_table = usa_table.rename(columns={'visit_cnt':'usa'})
    usa_table = usa_table.set_index('yyyymm')
    
    
    all_table=pd.merge(china_table, japan_table, left_index=True, right_index=True)
    all_table=pd.merge(all_table, usa_table, left_index=True, right_index=True)
    print(all_table)    # [72 rows x 3 columns]
    
    r_list= []
    for tourpoint in resNm[:5]:
        r_list.append(setScatterGraph(tour_table, all_table, tourpoint))
        
    
    
if __name__ =="__main__":
    processFunc()