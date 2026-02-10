# 연습문제1) 리스트를 통해 직원 자료를 입력받아 가공 후 출력하기

# 함수를 두 개 작성

# 입력 함수 :  [사번, 이름, 기본급, 입사년도]
def inputfunc():
    datas = [
        [1, "강나루", 1500000, 2010],
        [2, "이바다", 2200000, 2018],
        [3, "박하늘", 3200000, 2005],
    ]
    return datas

def processfunc(datas):
    data = datas
    for j in range(0,3):
        data[j][3]= 2026-data[j][3]
        if data[j][3] < 3: datas[j].append(150000)
        elif data[j][3] < 8: datas[j].append(450000)
        else: datas[j].append(1000000)

        if data[j][2]+data[j][4] >= 3000000:
            datas[j].append((data[j][2]+data[j][4])*0.5)
        elif data[j][2]+data[j][4] >= 2000000:
            datas[j].append((data[j][2]+data[j][4])*0.3)
        else:
            datas[j].append((data[j][2]+data[j][4])*0.15)

        datas[j].append(data[j][2] +data[j][4] - data[j][5])
    for d in datas:
        print(f"{d[0]:<6} {d[1]:<8} {d[2]:<8} {d[3]:<8} {d[4]:<8} {d[5]:<8} {d[6]:<8}")
        # print(f"{datas[i][0]}  {datas[i][1]}  {datas[i][2]}  {datas[i][3]}  {datas[i][4]}  {datas[i][5]}  {datas[i][6]}")

print('사번  이름  기본급  근무년수  근속수당  공제액  수령액')
print('---------------------------------------------------')

processfunc(inputfunc())

#연습문제2) 리스트를 통해 상품 자료를 입력받아 가공 후 출력하기

# 처리 조건 :  
#   1) 한 개의 상품명과 가격은 문자열로 입력됨. 문자열 나누기 필요.
#   2) 취급 상품 예는 아래와 같다.
#  * 취급상품표
#   상품명   단가
#   새우깡    450
#   감자깡    300
#   양파깡,   450

""" def inputfunc():
    datas = [
        "새우깡,15",
        "감자깡,20",
        "양파깡,10",
        "새우깡,30",
        "감자깡,25",
        "양파깡,40",
        "새우깡,40",
        "감자깡,10",
        "양파깡,35",
        "새우깡,50",
        "감자깡,60",
        "양파깡,20",
    ]
    return datas

def processfunc(datas):
    prices = {"새우깡" : 450, "감자깡" : 300, "양파깡" : 350}
    summary = {"새우깡" : [0,0], "감자깡" : [0,0], "양파깡" : [0,0]}
    total_qty=0
    total_amount=0

    for item in datas:
        name, qty_str = item.split(",")
        qty=int(qty_str)
        price=prices[name]
        amount=qty*price
        print(f"{name:<6} {qty:<5} {price:<5} {amount}")
        summary[name][0] +=qty
        summary[name][1] +=amount
        total_qty += qty
        total_amount += amount
    print("\n소계")
    for name in ["새우깡", "감자깡", "양파깡"]:
        print(f"{name} : {summary[name][0]}건   소계액 : {summary[name][1]}원")

    print("총계")
    print(f"총 건수 : {total_qty}")
    print(f"총 액  : {total_amount}원")


processfunc(inputfunc())

"""