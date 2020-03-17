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


lista = [XD(10,20) for i in range(10)]
print(lista)
print((0,0) + (1,1))

lista1 = [7]
lista = lista1
print(lista)
print([1,2] in lista1)

for i in [j for j in range(10)]:
    print(i)
    if i in lista1:
        continue
print('elo')

