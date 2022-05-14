from random import randint
from time import sleep

no_of_tries = 0
time = 0
while True:
    no_of_tries += 1
    time  = time + 0.1
    firstDice = randint(1, 6)
    secondDice = randint(1, 6)

    if firstDice + secondDice == 11 or firstDice + secondDice == 12:
        print(f"It took {no_of_tries} to get the sum to either 11 or 12 and time taken is {time}")
        print(str(firstDice) + " \n" + str(secondDice))
    sleep(0.1)
