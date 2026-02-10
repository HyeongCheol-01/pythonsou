
class CoinIn:

    def __init__(self):
        self.coin = 0
        self.cup = 0

    def culc(self, cup):
        total = cup * 200
        print(total, self.coin)
        change = self.coin - total
        if total > self.coin:
            return "요금 부족"
        else:
            return change

class Machine:
    
    def __init__(self):
        self.cup = 1
        self.coinin = CoinIn()

    def showData(self):
        self.coinin.coin = int(input("동전 입력: "))
        self.cup = int(input("잔 입력: "))
        result = self.coinin.culc(self.cup)

        if result == "요금 부족":
            print("요금이 부족합니다")
        else:
            print(f"커피 {self.cup}잔과 잔돈 {result}")

Machine().showData()