# bmi: 체중(kg)/키(m)^2


import random
random.seed(12)

def calc_bmiFunc(h,w):
    bmi = w/(h/100)**2
    if bmi < 18.5: return 'thin'
    if bmi < 25.0: return 'normal'
    return 'fat'

print(calc_bmiFunc(170,68))

fp = open('bmi.csv', mode='w')
fp.write('height,weight,label\n')

#무작위 데이터 생성
cnt = {'thin':0, 'normal':0, 'fat':0}
for i in range(50):
    h = random.randint(150,200)
    w = random.randint(35,100)
    label = calc_bmiFunc(h,w)
    cnt[label] += 1
    fp.write('{0},{1},{2}\n'.format(h,w,label))
fp.close()
print(cnt)

