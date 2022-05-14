second_last_number = 0
last_number = 1
next_number = 0

num = []
for i in range(1_000_000):
    next_number = second_last_number + last_number
    last_number = next_number
    second_last_number = last_number
    num.append(next_number)

file = open("number.txt", "w")

file.writelines(str(num))
file.close()
