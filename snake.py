#!/usr/bin/env python

import time, os, random
from msvcrt import kbhit, getch

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

#zufall
rand = random.Random()
rand.seed(None)

class WordMap(object):
    def __init__(self, x = 20, y = 10):
        self.map = ["*" * x,]
        for i in range(0, y - 2):
            self.map.append("*" + " " * (x - 2) + "*")
        self.map.append("*" * x)

        self.x = x
        self.y = y

        self.SpanFood()
        self.counter = 0

    def printWord(self):
        for line in self.map:
            print(line)

    def MapReplace(self, y, x, newChar):
        self.map[y] = self.map[y][0:x] + newChar + self.map[y][x + 1:self.x]

    def CharAt(self,y,x):
        return self.map[y][x]

    def SpanFood(self):
        x = rand.randint(1,self.x -1)
        y = rand.randint(1,self.y -3)
        while(self.map[y][x] != " "):
            x = rand.randint(1,self.x -1)
            y = rand.randint(1,self.y -3)
        self.MapReplace(y,x, "x")


class SnakeNode(object):
    def __init__(self, y, x, next = None):
        self.next = next
        self.x = x
        self.y = y

class snake(object):
    def __init__(self, wordMap):
        self.wordMap = wordMap
        self.tail = SnakeNode(1,1,SnakeNode(1,2, SnakeNode(1,3)))
        self.head = self.tail.next.next

        self.direction = RIGHT

        self.wordMap.MapReplace(1,1,"o")
        self.wordMap.MapReplace(1,2,"o")
        self.wordMap.MapReplace(1,3,"o")

    def turnRight(self):
            self.direction = (self.direction+1) % 4

    def turnLeft(self):
            self.direction = (self.direction+3) % 4

    def move(self):
        x = self.head.x
        y = self.head.y

        if self.direction == UP:
            y = y -1
        if self.direction == LEFT:
            x = x - 1
        if self.direction == DOWN:
            y = y + 1
        if self.direction == RIGHT:
            x = x +1

        nextHead = self.wordMap.CharAt(y,x)
        if nextHead == " ":
                self.wordMap.MapReplace(self.tail.y, self.tail.x, " ")
                self.tail = self.tail.next
                self.head.next = SnakeNode(y, x)
                self.head = self.head.next
                self.wordMap.MapReplace(self.head.y, self.head.x, "o")
                return True
        if nextHead == "x":
                self.head.next = SnakeNode(y, x)
                self.head = self.head.next
                self.wordMap.MapReplace(self.head.y, self.head.x, "o")
                self.wordMap.SpanFood()
                self.wordMap.counter += 1
                return True
        else:
            return False


if __name__ == '__main__':

    m = WordMap(x = 50, y = 20)
    s = snake(m)

    while s.move():
        os.system('CLS')

        m.printWord()
        if kbhit():
            code = ord(getch())
            if code == ord('a'):
                s.turnLeft()
            if code == ord('d'):
                s.turnRight()

        time.sleep(0.1)
    print("Du bist gestorben, erreichte Punkte ", m.counter)
