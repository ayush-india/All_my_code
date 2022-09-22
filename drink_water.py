import time as t
from pygame import mixer

mixer.init()

# Play the alarm sound and the again start the timer
def alarm(timer):
    global time
    while timer != 0:
        timer -= 1
        print(f"Drink water FAST !!!!!! \n Timer will reset in {timer} sec ")
        mixer.music.load("alarm.mp3")
        mixer.music.play()
        t.sleep(1)
    play_timer(time)


# Run the timer for the given amt of time and the call the alarm func
def play_timer(time):
    global timer
    while time != 0:
        print(f"Drink water in {time} sec")
        time -= 1
        t.sleep(1)

    alarm(timer)


# TODO Give the input in hr min and sec format
# Input the required variables
time = int(input("Enter the time for timer to run in sec \n :"))
timer = int(input("Enter the time for alarm in sec \n :"))

# Call the main method
play_timer(time)
