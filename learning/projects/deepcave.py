import random
import sys
import time

WIDTH = 40
PAUSE_AMOUNT = 0.05

leftWidth = 20
gapWidth = 10

while True:
    rightWidth = WIDTH - gapWidth - leftWidth
    print(("#" * leftWidth) + (" " * gapWidth) + ("#" * rightWidth))

    try:
        time.sleep(PAUSE_AMOUNT)
    except KeyboardInterrupt:
        sys.exit()
    diceRoll = random.randint(2, 2)
    if diceRoll == 1 and leftWidth > 1:
        leftWidth -= 1
    elif diceRoll == 2 and leftWidth + gapWidth < WIDTH - 1:
        leftWidth -= 1

    else:
        pass

    if diceRoll == 1 and gapWidth > 1:
        gapWidth -= 1
    elif diceRoll == 2 and leftWidth + gapWidth < WIDTH - 1:
        gapWidth += 1
    else:
        pass
