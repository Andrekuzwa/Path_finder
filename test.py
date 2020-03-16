class XD:
    def __init__(self,beka,meh):
        self.beka = beka
        self.meh = meh

    def __eq__(self, other):
        return self.beka == other.beka

k = XD(10,20)
c = XD(10,30)

print(k.beka,k.meh)
print(c.beka,c.meh)

print(k==c)


