import copy

#Cart class
class apples:
    def __init__(self):
        self.data = []
        self.sizeLimit = 8.0

    def clearAll(self):
        self.data = []

    def findLowest(self):
        #Logic, serve first the "lowest" apple and than start going up
        if len(self.data) == 0:
            return None
        return min(self.data, key=lambda x:x['z'])

    def findHighest(self):
        #Logic, serve first the "lowest" apple and than start going up
        if len(self.data) == 0:
            return None
        return max(self.data, key=lambda x:x['z'])

    def removeElement(self,element):
        self.data.pop(self.index(element))

    def popLowest(self):
        el = self.findLowest()
        elcopy =  copy.deepcopy(el)
        if el != None:
            self.removeElement(el)
            return elcopy
        return None

    def popHighest(self):
        el = self.findHighest()     
        elcopy =  copy.deepcopy(el)
        if el != None:
            self.removeElement(el)
            return elcopy
        return None