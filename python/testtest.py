import math

x = 997
y = 0

len1 = 497.0
len2 = 500.0

dist = math.sqrt(x**2+y**2)

a = (2.0 * dist * len1)

b = (dist**2 + len1**2 - len2**2)

D2 = math.acos(b / a)

print(b)
print(a)
print(dist)
print(D2)

