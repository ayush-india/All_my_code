import random as rn
import string

lower_alphabets = list(string.ascii_lowercase)
uppper_alphabets = list(string.ascii_uppercase)

numbers = []

for k in range(0, 10):
    numbers.append(k)

password = []
for i in range(10):
    if rn.randint(1, 3) == 1:
        password.append(uppper_alphabets[(rn.randint(0, 25))])
    if rn.randint(1, 3) == 2:
        password.append(str(numbers[(rn.randint(1, 8))]))
    if rn.randint(1, 3) == 3:
        password.append(lower_alphabets[(rn.randint(0, 25))])


password_key = ""
print(password_key.join(password))
