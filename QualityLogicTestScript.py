
"""
stuff = (1,2,3,4,5,6,7,8,9,10)
def funfun(n):
  a, b = 0, 1
  for _ in range(n):
    yield a
    a, b = b, a + b


print(list(funfun(1)))
c = 0
for x in stuff:
    #stuff[c] = list(funfun(x))
    print(c)
    c += 1

print("Test 2")
"""

#explain the code


count=0
for ch in open("C:\\Users\\ravreeland\\PycharmProjects\\DDR_PlottingTool\\Testing\\testme.txt", encoding="latin-1", errors="surrogateescape").read():
    if ch.isupper():
        count += 1
print("Caps: ", count)

capList = [char for char in open("C:\\Users\\ravreeland\\PycharmProjects\\DDR_PlottingTool\\Testing\\testme.txt", encoding="latin-1", errors="surrogateescape").read() if char.isupper()]
print(len(capList))
# condense and rewrite test 2 in 2 lines of functional code: