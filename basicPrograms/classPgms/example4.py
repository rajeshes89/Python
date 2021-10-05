class sample:
    def __sety(self,i):
        self.__i = i
        print(self.__i)
    def setyy(self,i):
        self.__sety(i)
    def printy(self):
        print(self.__i)

s = sample()

s.setyy(34)
s.printy()
