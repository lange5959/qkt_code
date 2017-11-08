class duck():
    def walk(self):
        print('I walk like a duck')

    def swim(self):
        print('i swim like a duck')


class person():
    def walk(self):
        print('this one walk like a duck')

    def swim(self):
        print('this man swim like a duck')


def watch_duck(animal):
    animal.walk()
    animal.swim()


# small_duck = duck()
# watch_duck(small_duck)

# duck_like_man = person()
# watch_duck(duck_like_man)

class Lame_Foot_Duck():
    def swim(self):
        print('i am lame but i can swim')


lame_duck = Lame_Foot_Duck()
watch_duck(lame_duck)