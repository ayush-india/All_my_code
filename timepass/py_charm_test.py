sln = 0
ln = 1
nn = 0
fiboo_series = []
for i in range(100000):
    nn = sln + ln
    sln = ln
    ln = nn
    fiboo_series.append(nn)
    # print(nn)

filename = "fibbo_series.txt"

with open(filename, "w") as file_objext:
    file_objext.write(str(fiboo_series))
