i = int(input("Enter and no and i will convert it to roman nos"))

list = []
while i >= 1:
    if i >= 1000:
        list.append("M")
        i -= 1000
        continue
    if i >= 500:
        list.append("D")
        i -= 500
        continue
    if i >= 100:
        list.append("C")
        i -= 100
        continue
    if i >= 50:
        list.append("L")
        i -= 50
        continue
    if i >= 10:
        list.append("X")
        i -= 10
        continue
    if i >= 5:
        list.append("V")
        i -= 10
        continue
    if i >= 1:
        list.append("I")
        i -= 1
        continue
list.reverse()
print(list)
