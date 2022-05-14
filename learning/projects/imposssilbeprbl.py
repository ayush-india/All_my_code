list = {}
real = {}
for i in range(5, 107):
    n = i
    var = []
    while n != 1:

        if n % 2 == 0:
            n = n / 2
        else:
            n = 3 * n + 1

        var.append(n)
        list[i] = len(var)
        real[i] = var

for key, value in list.items():
    if value == max(list.values()):
        print(f"And the winner is {key} by a weigth of {value}")
        print("\n And its values are ")
        print(real[key])
