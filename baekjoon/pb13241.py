import sys

# 최대공약수(GCD) 함수: 유클리드 호제법 사용
def get_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# 입력을 빠르게 받기 (큰 수 처리에 유리)
line = sys.stdin.readline().split()

if line:
    a, b = map(int, line)
    
    # 최소공배수(LCM) 공식: (A * B) // GCD
    # 파이썬은 내부적으로 64비트 이상의 큰 정수도 자동으로 처리합니다.
    lcm = (a * b) // get_gcd(a, b)
    
    print(lcm)