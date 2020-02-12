# -*- coding: utf-8 -*-
# This is a typical class example.
class Fruit(object):
    """This is my first class"""
    category = 'Apple?Orange?pear?'
    number = 0
    def __init__ (self, category, weight=None, owner=None):
        self.category = category
        self.ripe = False
        self.weight = weight
        self.owner = owner
        Fruit.number +=1
    def changeOwner (self, owner):
        self.formerowner = self.owner
        self.owner = owner
    def changeState (self):
        self.ripe = True
    def growWeight (self, weight):
        self.weight = weight
    def toString (self):
        return self.owner+'\'s '+self.category+', weight:'+str(self.weight)+\
            (', and' if self.ripe else ', but not') + 'ripe'
                
a1 = Fruit('apple', 100, 'Jinghe')
p1 = Fruit('pear', 100, 'Su')
p1.changeOwner('NaNa')
print p1.owner, p1.formerowner
print a1.category, Fruit.category
print Fruit.number, a1.number, p1.number
print 'End of programm'