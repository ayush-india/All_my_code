import time
from pygame import mixer

mixer.init()

def alarm(k):
    global n
    # TODO: Play a sound to drink water
    while k != 0:
        k -= 1
        print(f"Drink water FAST !!!!!! \n Timer will reset in {k} sec ")
        mixer.music.load('alarm.mp3')
        mixer.music.play()
        time.sleep(1)
    timer(n)
    
def timer(n):
    global k
    while n != 0:
        print(f"Drink water in {n} sec")
        n -= 1
        time.sleep(1)

    alarm(k)


# TODO Give the input in hr min and sec format 
n = int(input("Enter the time for timer to run in sec \n :"))
k = int(input("Enter the time for alarm in sec \n :"))

timer(n)

