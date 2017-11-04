def fn(n):
    if n is 1:
        return 1
    return n*fn(n-1)

print fn(5)