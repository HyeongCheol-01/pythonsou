import sys

# 최대공약수(GCD) 함수: 유클리드 호제법 사용
def get_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return int(a)

a, b = map(int, sys.stdin.readline().split())
c, d = map(int, sys.stdin.readline().split())
e = a*d+c*b
f = b*d


print(int(e/get_gcd(e,f)), int(f/get_gcd(e,f)))
