# coding=utf-8
# python duck type ??
class CollectionClass():
    lists = [1, 2, 3, 4]

    def __getitem__(self, index):
        return self.lists[index]


iter_able_object = CollectionClass()


class Another_iterAbleClass():
    lists = [1, 2, 3, 4]
    list_position = -1

    def __iter__(self):
        return self

    def next(self):  # 还有更简单的实现，使用生成器或迭代器什么的:)
        self.list_position += 1
        if self.list_position > 3:
            raise StopIteration
        return self.lists[self.list_position]


another_iterable_object = Another_iterAbleClass()

print(iter_able_object[1])
print(iter_able_object[1:3])


# another_iterable_object[2]

print(next(another_iterable_object))

print(next(another_iterable_object))

# print(next(iter_able_object))