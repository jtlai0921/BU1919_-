# -*- coding: utf-8 -*-
# This is a typical sub-class example.
class Fruit(object):
    """This is the super class"""
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
class Apple(Fruit):
    """This is a child-class from class Fruit"""
    def __init__ (self, weight=None, owner=None, onTree=True):
        self.onTree = onTree
        super(Apple, self).__init__('apple', weight, owner)
    def pickDown ():
        onTree = False
a1 = Apple(100, 'Jinghe')
print a1.toString()
print 'End of programm'