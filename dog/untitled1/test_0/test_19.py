def isPrime(n):
    import math
    if n == 1:
        return False
    elif n<4:
        return True
    elif n & 1 == 0:
        return False
    elif n < 9:
        return True
    elif n % 3 == 0:
        return False
    else:
        r = math.floor(math.sqrt(n))
        # print r 
        f = 5
        while f <= r:
            if n % f == 0:
                return False
            if n % (f+2) == 0:
                return False
            f += 6
        return True
list_a = []
for i in xrange(1, 10000*200):
    if isPrime(i):
        # print int(i)
        list_a.append(i)
print len(list_a),'<<<num'