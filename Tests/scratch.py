#ehn the year is divisible by 4 but not 100 but it is when divisible by 400

def leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

y1 = 1582
y2 = 1584
y3 = 1600
y4 = 1700

print(leap_year(y1))
print(leap_year(y2))
print(leap_year(y3))
print(leap_year(y4))

print(1700/4)