class ElecProduct:
    volume=0
    def volumeControl(self,volume):
        print('ElecP Volume :', self.volume)

class ElecTv(ElecProduct):
    def volumeControl(self,volume):
        print('ElecTv Vol:', volume)

class ElecRadio(ElecProduct):

    def volumeControl(self,volume):
        print('ElecRadio Vol:', volume)

elec = [ElecTv(), ElecRadio()]

for p in elec:
    p.volumeControl(20)