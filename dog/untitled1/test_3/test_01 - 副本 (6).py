# coding=utf-8
# bisect排序模块
import bisect
data = [4,8,1,0]
data.sort()
# print data
# 插入
bisect.insort(data, 3)

# print data
# 其目的在于查找该数值将会插入的位置并返回，而不会插入。
# print bisect.bisect(data, 7)
print data

data = [4]
# 该函数用入处理将会插入重复数值的情况，返回将会插入的位置：
print ">>>bisect_left"
print bisect.bisect_left(data, 4)
print data
print bisect.bisect_right(data, 4)



# print ">>>insort_left"
# print bisect.insort_left(data, 4)
# print data
