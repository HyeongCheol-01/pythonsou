# 문1) 1 ~ 100 사이의 정수 중 3의 배수이나 2의 배수가 아닌 수를 출력하고, 합을 출력
""" i=0
sum=0
while i<100:
    i+=1
    if i%2==0:continue
    if i%3==0:continue
    print(i)
    sum=sum+i

else:
    print(sum) """

i = 0
total = 0
while i <= 100:
    if i % 3 == 0 and i % 2 != 0:
        print(i, end = ' ')
        total = total + i
    i += 1
print(total)

# 문2) 2 ~ 5 까지의 구구단 출력

i = 2
while i <=5 :
    j = 1
    while j <= 9:
        print(f'{i} * {j} = {i * j}', end =' ')
        j += 1
    print()
    i += 1





# 문3) 1 ~ 100 사이의 정수 중 “짝수는 더하고, 홀수는 빼서” 최종 결과 출력

i = 1
sum = 0
while i <= 100:
    if i%2==0:
        sum=sum+i
    else:
        sum=sum-i
    i+=1
print(f'최종결과 = {sum}')

# 문4) -1, 3, -5, 7, -9, 11 ~ 99 까지의 모두에 대한 합을 출력
i = -1
sum = 0
while abs(i)<=99:
    sum=sum+i
    if i<0:
        i-=2
    else:
        i+=2
    i*=-1
print(sum)



#문5) 1 ~ 100 사이의 숫자 중 각 자리 수의 합이 10 이상인 수만 출력
#예) 29 → 2 + 9 = 11 (출력)

""" k=10
while k <= 100:
    str_i = str(k)
    hap = sum((int(str_i[0]),int(str_i[1])))
    if hap>=10:
        print(f'{str_i}일 때 {hap}')
    k+=1 """

num = 1
while num <= 100:
    temp = num
    digit_sum = 0

    while temp > 0:
        digit_sum += temp % 10
        temp //= 10 
         
    if digit_sum >= 10:
        print(num)
    num += 1

#문6) 1부터 시작해서 누적합이 처음으로 1000을 넘는 순간의 숫자와 그때의 합을 출력
#힌트: 언제 멈출지 미리 모름 → while 적합

""" i=1
s=0
while s<=1000:
    s=s+i
    i+=1
print(s) """

#문7) 구구단을 출력하되 결과가 30을 넘으면 해당 단 중단하고 다음 단으로 이동

""" i=2
while i<=9:
    j=1
    while j<=9:
        if i*j>30: break
        print(f'{i} * {j} = {i*j}',end=' ')
        j+=1
    i+=1
    print() """


#문8) 1 ~ 1000 사이의 소수(1보다 크며 1과 자신의 수 이외에는 나눌 수 없는 수)와 그 갯수를 출력
# 힌트: 이 문제는 반복이 두 단계다. 2부터 1000까지 하나씩 검사한다. 각 숫자마다 소수인지 확인한다.
# 그래서 while 안에 while 구조가 필요하다.

""" i=3
count=0
while i<=1000:
    j=2
    while j <= i-1:
        a=True
        if i%j==0:
            a=False
            break
        j+=1
    if a==True:
        print(i, end= ' ')
        count+=1
    i+=1 """


# 문제1) 1부터 50까지의 숫자 중 3의 배수는 건너뛰고 나머지 수만 출력하라

""" for i in range(1,50):
    if i%3==0: continue
    print(i) """

#문제2) 1부터 100까지 출력하되 4의 배수, 6의 배수는 건너뛴다. 그 외의 수 중 5의 배수만 출력하고 그들의 합도 출력하라
""" sum=0
for i in range(1,100):
    if i%4==0: continue
    if i%6==0: continue
    if i%5==0:
        print(f'5의 배수 {i}')
        sum=sum+i
        print(f'합 {sum}')
 """