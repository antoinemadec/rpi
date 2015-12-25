#!/usr/bin/python3

import random as rdm
from math import *

money=100
rdm.seed() # use time for seed

while True:
    print("Vous avez", money, "$")
    try:
        assert money > 0
    except:
        print("VOUS AVEZ PERDU !!!!!!!");
        break
    mise=input("Mise ? : ")    
    number=input("Nombre [0:49] ? : ")
    try:
        mise    = int(mise)
        number  = int(number)
        assert mise <= money
        assert number < 50
        assert number >= 0
    except:
        print("Entrées invalid")
        continue
    tirage=rdm.randint(0,49)
    print("La roue tourne..................")
    exec(sleep 1)
    print(tirage, "!");
    if (tirage==number):
        print("Bon nombre: vous empochez 3x la mise !")
        money += 3*mise
    elif (tirage%2) == (number%2):
        print("Bonne couleur: vous empochez une demi mise.")
        money += ceil(mise/2)
    else:
        print("Vous perdez votre mise.")
        money -= mise
