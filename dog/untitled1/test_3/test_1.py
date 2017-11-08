# coding=utf-8
def main():
    name = '1'
    # name = name.encode('utf-8')
    for i in range(10,11):
        with open("test_%s.py" % i, "wb") as f:
            f.write(name)

main()