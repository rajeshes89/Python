class Learning(object):
    def __topic1(self,sub1):
        self.sub1 = sub1
        print(self.sub1)
    def calltopic1(self):
        self.__topic1("mat")

l = Learning()
l.calltopic1()
