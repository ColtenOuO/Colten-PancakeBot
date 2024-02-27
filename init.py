import random

fish = []

def init():
    f = open('fish.txt','r',encoding="utf-8")
    for i in f.readlines():
        fish.append(i)
    return

def fishing():
    return random.choice(fish)